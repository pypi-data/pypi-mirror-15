#!/usr/bin/env python3
#
# This file is part of Script of Scripts (sos), a workflow system
# for the execution of commands and scripts in different languages.
# Please visit https://github.com/bpeng2000/SOS for more information.
#
# Copyright (C) 2016 Bo Peng (bpeng@mdanderson.org)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import base64
import imghdr
import fnmatch
import contextlib
import subprocess

import zipfile
import tarfile
import gzip

from .utils import env, WorkflowDict, short_repr, pretty_size, dehtml
from ._version import __sos_version__, __version__
from .sos_eval import SoS_exec, interpolate
from .sos_executor import Interactive_Executor
from .sos_syntax import SOS_SECTION_HEADER

from IPython.core.interactiveshell import InteractiveShell
from IPython.lib.clipboard import ClipboardEmpty, osx_clipboard_get, tkinter_clipboard_get
from IPython.core.error import UsageError
from IPython.core.display import HTML
from ipykernel.kernelbase import Kernel
from jupyter_client import manager, find_connection_file

from textwrap import dedent
from io import StringIO

from nbconvert.exporters import Exporter

class FlushableStringIO(StringIO):
    def __init__(self, kernel, name, *args, **kwargs):
        StringIO.__init__(self, *args, **kwargs)
        self.kernel = kernel
        self.name = name

    def flush(self):
        value = self.getvalue()
        self.kernel.send_response(self.kernel.iopub_socket, 'stream',
            {'name': self.name, 'text': value})
        self.truncate(0)
        self.seek(0)
        return len(value.strip())


__all__ = ['SoS_Exporter', 'SoS_Kernel']

def clipboard_get():
    """ Get text from the clipboard.
    """
    if sys.platform == 'darwin':
        try:
            return osx_clipboard_get()
        except:
            return tkinter_clipboard_get()
    else:
        return tkinter_clipboard_get()

class SoS_FilePreviewer():
    def __init__(self):
        pass

    def display_data_for_image(self, filename):
        with open(filename, 'rb') as f:
            image = f.read()

        image_type = imghdr.what(None, image)
        image_data = base64.b64encode(image).decode('ascii')
        if image_type != 'png':
            try:
                from wand.image import Image
                img = Image(filename=filename)
                return { 'image/' + image_type: image_data,
                    'image/png': base64.b64encode(img._repr_png_()).decode('ascii') }
            except Exception:
                return { 'image/' + image_type: image_data }
        else:
            return { 'image/' + image_type: image_data }

    def preview(self, filename):
        if imghdr.what(filename) is not None:
            # image
            return 'display_data', self.display_data_for_image(filename)
        elif filename.lower().endswith('.pdf'):
            try:
                # this import will fail even if wand is installed
                # if imagemagick is not installed properly.
                from wand.image import Image
                img = Image(filename=filename)
                return 'display_data', {
                    'text/html': HTML('<iframe src={0} width="100%"></iframe>'.format(filename)).data,
                    'image/png': base64.b64encode(img._repr_png_()).decode('ascii') }
            except Exception as e:
                env.logger.error(e)
                return 'display_data', { 'text/html':
                    HTML('<iframe src={0} width="100%"></iframe>'.format(filename)).data}
        elif filename.lower().endswith('.html'):
            with open(filename) as html:
                content = html.read()
            return 'display_data', { 'text/html': content,
                'text/plain': dehtml(content) }
        elif filename.lower().endswith('.csv') or filename.lower().endswith('.tsv'):
            try:
                import pandas
                data = pandas.read_csv(filename, nrows=10)
                html = data.to_html()
                return 'display_data', { 'text/html': HTML(html).data}
            except Exception:
                pass
        # is it a compressed file?
        if zipfile.is_zipfile(filename):
            zip = zipfile.ZipFile(filename)
            names = zip.namelist()
            return '{} files\n'.format(len(names)) + '\n'.join(names[:5]) + ('\n...' if len(names) > 5 else '')
        elif tarfile.is_tarfile(filename):
            with tarfile.open(filename, 'r:*') as tar:
                # only extract files
                names = [x.name for x in tar.getmembers() if x.isfile()]
            return '{} files\n'.format(len(names)) + '\n'.join(names[:5]) + ('\n...' if len(names) > 5 else '')
        elif filename.endswith('.gz'):
            content = b''
            with gzip.open(filename, 'rb') as fin:
                for line in range(5):
                    content += fin.readline()
            try:
                return content.decode()
            except:
                return 'binary data'
        else:
            content = b''
            with open(filename, 'rb') as fin:
                for line in range(5):
                    content += fin.readline()
            try:
                return content.decode()
            except:
                pass
        return 'binary data'

class BioPreviewer(SoS_FilePreviewer):
    def  __init__(self):
        SoS_FilePreviewer.__init__(self)

    def previewBam(self, filename):
        try:
            import pysam
        except ImportError:
            return 'pysam is needed to preview bam format'
        try:
            res = ''
            with pysam.AlignmentFile(filename, 'rb') as bam:
                headers = bam.header
                for record_type in ('RG', 'PG', 'SQ'):
                    if record_type not in headers:
                        continue
                    else:
                        records = headers[record_type]
                    res += record_type + ':\n'
                    for i, record in enumerate(records):
                        if type(record) == str:
                            res += '  ' + short_repr(record) + '\n'
                        elif type(record) == dict:
                            res += '  '
                            for idx, (k, v) in enumerate(record.items()):
                                if idx < 4:
                                    res += '{}: {}    '.format(k, short_repr(v))
                                elif idx == 4:
                                    res += '...'
                                    break
                        if i > 4:
                            res += '\n  ...\n'
                            break
                        else:
                            res += '\n'
            return res
        except Exception as e:
            return 'failed to preview {}'.format(e)

    def preview(self, filename):
        if filename.lower().endswith('.bam'):
            return self.previewBam(filename)
        else:
            return SoS_FilePreviewer.preview(filename)

class SoS_Exporter(Exporter):
    def __init__(self, config=None, reorder=False, reset_index=False, add_header=False,
            no_index=False, remove_magic=False, md_to_report=False,
            **kwargs):
        self.reorder = reorder
        self.reset_index = reset_index
        self.add_header = add_header
        self.no_index = no_index
        self.remove_magic = remove_magic
        self.md_to_report = md_to_report
        self.output_extension = '.sos'
        self.output_mimetype = 'text/x-sos'
        Exporter.__init__(self, config, **kwargs)

    def from_notebook_cell(self, cell, fh, idx = 0):
        if not hasattr(cell, 'execution_count') or cell.execution_count is None or self.no_index:
            fh.write('\n#%% {}\n'.format(cell.cell_type))
        else:
            idx += 1
            fh.write('\n#%% {} {}\n'.format(cell.cell_type,
                                              idx if self.reset_index else cell.execution_count))
        if cell.cell_type == 'code':
            if any(cell.source.startswith(x) for x in ('%run', '%restart', '%dict', '%use', '%with', '%set', '%paste')):
                if self.remove_magic:
                    cell.source = '\n'.join(cell.source.split('\n')[1:])
                else:
                    env.logger.warning('SoS magic "{}" has to remove them before executing the script with sos command.'.format(cell.source.split('\n')[0]))
            if self.add_header and not any([SOS_SECTION_HEADER.match(x) for x in cell.source.split('\n')]):
                cell.source = '[{}]\n'.format(idx if self.reset_index else cell.execution_count) + cell.source
            fh.write(cell.source.strip() + '\n')
        elif cell.cell_type == "markdown":
            fh.write('\n'.join('#! ' + x for x in cell.source.split('\n') if x.strip()) + '\n')
        return idx

    def from_notebook_node(self, nb, resources, **kwargs):
        #
        if self.reorder:
            unnumbered_cells = {x: y for x, y in enumerate(nb.cells)
                              if not hasattr(y, 'execution_count') or y.execution_count is None}
            numbered_cells = [y for y in nb.cells
                              if hasattr(y, 'execution_count') and y.execution_count is not None]
            numbered_cells = sorted(numbered_cells, key = lambda x: x.execution_count)
            cells = []
            for idx in range(len(nb.cells)):
                if idx in unnumbered_cells:
                    cells.append(unnumbered_cells[idx])
                else:
                    cells.append(numbered_cells.pop(0))
        else:
            cells = nb.cells
        with StringIO() as fh:
            fh.write('#!/usr/bin/env sos-runner\n')
            fh.write('#fileformat=SOSNB1.0\n')
            idx = 0
            for cell in cells:
                idx = self.from_notebook_cell(cell, fh, idx)
            content = fh.getvalue()
        resources['output_extension'] = '.sos'
        return content, resources


class SoS_Kernel(Kernel):
    implementation = 'SOS'
    implementation_version = __version__
    language = 'sos'
    language_version = __sos_version__
    language_info = {
        'mimetype': 'text/x-sos',
        'name': 'sos',
        'file_extension': '.sos',
        'pygments_lexer': 'sos',
        'codemirror_mode': 'sos',
        'nbconvert_exporter': 'pysos.kernel.SoS_Exporter',
    }
    banner = "SoS kernel - script of scripts"
    shell = InteractiveShell.instance()

    def __init__(self, **kwargs):
        super(SoS_Kernel, self).__init__(**kwargs)
        self._start_sos()

    def _start_sos(self):
        env.sos_dict = WorkflowDict()
        SoS_exec('from pysos import *')
        env.sos_dict.set('__interactive__', True)
        self.executor = Interactive_Executor()
        self.original_keys = set(env.sos_dict._dict.keys())
        self.original_keys.add('__builtins__')
        self.options = ''
        self.kernel = 'sos'
        self.banner = self.banner + '\nConnection file {}'.format(os.path.basename(find_connection_file()))
        # FIXME: this should in theory be a MultiKernelManager...
        self.kernels = {}
        self.original_kernel = None
        self.format_obj = self.shell.display_formatter.format
        self.shell.enable_gui = lambda x: False
        self.previewer = {'*': SoS_FilePreviewer().preview, '*.bam': BioPreviewer().preview }
        self.report_file = os.path.join(env.exec_dir, 'summary_report.md')
        env.sos_dict.set('__summary_report__', self.report_file)
        if os.path.isfile(self.report_file):
            os.remove(self.report_file)
        # touch the file
        with open(self.report_file, 'w'):
            pass

    @contextlib.contextmanager
    def redirect_sos_io(self):
        save_stdout = sys.stdout
        save_stderr = sys.stderr
        sys.stdout = FlushableStringIO(self, 'stdout')
        sys.stderr = FlushableStringIO(self, 'stderr')
        yield
        sys.stdout = save_stdout
        sys.stderr = save_stderr

    def do_inspect(self, code, cursor_pos, detail_level=0):
        'Inspect code'
        return {
            'status': 'ok',
            'found': 'true',
            'data': {x:y for x,y in env.sos_dict._dict.items() if x not in self.original_keys and not x.startswith('__')},
            'metadata':''}

    def sosdict(self, line):
        'Magic that displays content of the dictionary'
        # do not return __builtins__ beacuse it is too long...
        actions = line.strip().split()
        for action in actions:
            if action not in ['reset', 'all', 'keys']:
                raise RuntimeError('Unrecognized sosdict option {}'.format(action))
        if 'reset' in actions:
            return self._reset()
        if 'keys' in actions:
            if 'all' in actions:
                return env.sos_dict._dict.keys()
            else:
                return {x for x in env.sos_dict._dict.keys() if not x.startswith('__')} - self.original_keys
        else:
            if 'all' in actions:
                return env.sos_dict._dict
            else:
                return {x:y for x,y in env.sos_dict._dict.items() if x not in self.original_keys and not x.startswith('__')}

    def do_is_complete(self, code):
        '''check if new line is in order'''
        code = code.strip()
        if not code:
            return {'status': 'complete', 'indent': ''}
        if any(code.startswith(x) for x in ['%dict', '%paste']):
            return {'status': 'complete', 'indent': ''}
        if code.endswith(':') or code.endswith(','):
            return {'status': 'incomplete', 'indent': '  '}
        lines = code.split('\n')
        if lines[-1].startswith(' ') or lines[-1].startswith('\t'):
            # if it is a new line, complte
            empty = [idx for idx,x in enumerate(lines[-1]) if x not in (' ', '\t')][0]
            return {'status': 'incomplete', 'indent': lines[-1][:empty]}
        #
        if SOS_SECTION_HEADER.match(lines[-1]):
            return {'status': 'incomplete', 'indent': ''}
        # check syntax??
        try:
            compile(code, '<string>', 'exec')
            return {'status': 'complete', 'indent': ''}
        except:
            try:
                self.executor.parse_script(code)
                return {'status': 'complete', 'indent': ''}
            except:
                return {'status': 'unknown', 'indent': ''}

    def get_magic_option(self, code):
        lines = code.split('\n')
        pieces = lines[0].strip().split(None, 1)
        if len(pieces) == 2:
            command_line = pieces[1]
        else:
            command_line = ''
        return command_line

    def run_cell(self, code, store_history):
        #
        if not self.KM.is_alive():
            self.send_response(self.iopub_socket, 'stream',
                {'name': 'stdout', 'text': 'Restarting kernel "{}"\n'.format(self.kernel)})
            self.KM.restart_kernel(now=False)
            self.KC = self.KM.client()
        # flush stale replies, which could have been ignored, due to missed heartbeats
        while self.KC.shell_channel.msg_ready():
            self.KC.shell_channel.get_msg()
        # executing code in another kernel
        self.KC.execute(code, silent=False, store_history=not store_history)

        # first thing is wait for any side effects (output, stdin, etc.)
        _execution_state = "busy"
        while _execution_state != 'idle':
            # display intermediate print statements, etc.
            while self.KC.iopub_channel.msg_ready():
                sub_msg = self.KC.iopub_channel.get_msg()
                msg_type = sub_msg['header']['msg_type']
                if msg_type == 'status':
                    _execution_state = sub_msg["content"]["execution_state"]
                elif msg_type in ('execute_input', 'execute_result'):
                    # override execution count with the master count,
                    # not sure if it is needed
                    sub_msg['content']['execution_count'] = self.execution_count
                self.send_response(self.iopub_socket, msg_type, sub_msg['content'])
        # now get the real result
        reply = self.KC.get_shell_msg(timeout=10)
        reply['content']['execution_count'] = self.execution_count
        return reply['content']

    def switch_kernel(self, kernel):
        if kernel and kernel != 'sos':
            if kernel != self.kernel:
                if kernel in self.kernels:
                    #self.send_response(self.iopub_socket, 'stream',
                    #    {'name': 'stdout', 'text': 'Using kernel "{}"\n'.format(kernel)})
                    self.KM, self.KC = self.kernels[kernel]
                    self.kernel = kernel
                else:
                    try:
                        self.kernels[kernel] = manager.start_new_kernel(startup_timeout=60, kernel_name=kernel)
                        #self.send_response(self.iopub_socket, 'stream',
                        #    {'name': 'stdout', 'text': 'Kernel "{}" started\n'.format(kernel)})
                        self.KM, self.KC = self.kernels[kernel]
                        self.kernel = kernel
                    except Exception as e:
                        self.send_response(self.iopub_socket, 'stream',
                            {'name': 'stdout', 'text': 'Failed to start kernel "{}". Use "jupyter kernelspec list" to check if it is installed: {}\n'.format(kernel, e)})
        else:
            # kernel == '' or kernel == 'sos'
            if kernel == '':
                self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stdout', 'text': 'Kernel "{}" is used.\n'.format(self.kernel)})
            elif kernel == 'sos':
                #self.send_response(self.iopub_socket, 'stream',
                #    {'name': 'stdout', 'text': 'Switching back to sos kernel\n'})
                self.kernel = 'sos'

    def restart_kernel(self, kernel):
        if kernel == 'sos':
            # cannot restart myself ...
            self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stderr', 'text': 'Cannot restart sos kernel from within sos.'})
        elif kernel:
            if kernel in self.kernels:
                try:
                    self.kernels[kernel][0].shutdown_kernel(restart=False)
                except Exception as e:
                    env.logger.warning('Failed to shutdown kernel {}: {}'.format(kernel, e))
            #
            try:
                self.kernels[kernel] = manager.start_new_kernel(startup_timeout=60, kernel_name=kernel)
                self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stdout', 'text': 'Kernel {} {}started\n'.format(kernel, 're' if kernel in self.kernels else '')})
                #self.send_response(self.iopub_socket, 'stream',
                #    {'name': 'stdout', 'text': 'Kernel "{}" started\n'.format(kernel)})
                if kernel == self.kernel:
                    self.KM, self.KC = self.kernels[kernel]
            except Exception as e:
                self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stdout', 'text': 'Failed to start kernel "{}". Use "jupyter kernelspec list" to check if it is installed: {}\n'.format(kernel, e)})
        else:
            self.send_response(self.iopub_socket, 'stream',
                {'name': 'stdout', 'text': 'Specify one of the kernels to restart: sos{}\n'
                    .format(''.join(', {}'.format(x) for x in self.kernels))})

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if code == 'import os\n_pid = os.getpid()':
            # this is a special probing command from vim-ipython. Let us handle it specially
            # so that vim-python can get the pid.
            return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': None,
                'payload': [],
                'user_expressions': {'_pid': {'data': {'text/plain': os.getpid()}}}
               }
        mode = 'code'
        if code.startswith('%dict'):
            mode = 'dict'
            command_line = self.get_magic_option(code)
        elif code.startswith('%connect_info'):
            cfile = find_connection_file()
            with open(cfile) as conn:
                conn_info = conn.read()
            self.send_response(self.iopub_socket, 'stream',
                  {'name': 'stdout', 'text': 'Connection file: {}\n{}'.format(cfile, conn_info)})
            return {'status': 'ok',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                   }
        elif code.startswith('%set'):
            options = self.get_magic_option(code)
            if options.strip():
                #self.send_response(self.iopub_socket, 'stream',
                #    {'name': 'stdout', 'text': 'sos options set to "{}"\n'.format(options)})
                self.options = options.strip()
            else:
                if self.options:
                    self.send_response(self.iopub_socket, 'stream',
                        {'name': 'stdout', 'text': 'sos options "{}" reset to ""\n'.format(self.options)})
                    self.options = ''
                else:
                    self.send_response(self.iopub_socket, 'stream',
                        {'name': 'stdout', 'text': 'Usage: set persistent sos options such as -v 3 (debug output) -p (prepare) and -t (transcribe)\n'})
            lines = code.split('\n')
            code = '\n'.join(lines[1:])
            command_line = self.options
        elif code.startswith('%restart'):
            options = self.get_magic_option(code)
            if options == 'R':
                options = 'ir'
            self.restart_kernel(options)
            return {'status': 'ok',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                   }
        elif code.startswith('%with') or code.startswith('%use'):
            options = self.get_magic_option(code)
            if options == 'R':
                options = 'ir'
            #
            if code.startswith('%with'):
                self.original_kernel = self.kernel
            self.switch_kernel(options)
            lines = code.split('\n')
            code = '\n'.join(lines[1:])
            command_line = self.options
        elif code.startswith('%paste'):
            command_line = (self.options + ' ' + self.get_magic_option(code)).strip()
            try:
                code = clipboard_get()
            except ClipboardEmpty:
                raise UsageError("The clipboard appears to be empty")
            except Exception as e:
                env.logger.error('Could not get text from the clipboard: {}'.format(e))
                return
            #
            self.send_response(self.iopub_socket, 'stream',
                {'name': 'stdout', 'text': code.strip() + '\n## -- End pasted text --\n'})
        elif code.startswith('%run'):
            lines = code.split('\n')
            code = '\n'.join(lines[1:])
            command_line = self.options + ' ' + self.get_magic_option(code)
        elif code.startswith('%'):
            # treat as arbitrary shell command
            lines = [x for x in code.split('\n') if x.strip()]
            if len(lines) > 1:
                self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stderr', 'text': 'extra lines ignored in temporary shell mode\n'})
            #
            # interpolate command
            cmd = lines[0][1:]
            try:
                new_cmd = interpolate(cmd, sigil='${ }', local_dict=env.sos_dict._dict)
                if new_cmd != cmd:
                    cmd = new_cmd
                    if not cmd.startswith('cd ') and not cmd.startswith('cd\t'):
                        self.send_response(self.iopub_socket, 'stream',
                            {'name': 'stdout', 'text':
                            new_cmd.strip() + '\n## -- End interpolated command --\n'})
            except Exception as e:
                self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stdout', 'text': 'Failed to interpolate {}: {}'.format(short_repr(cmd), e)})
                return  {'status': 'error',
                        'ename': e.__class__.__name__,
                        'evalue': str(e),
                        'traceback': [],
                        'execution_count': self.execution_count,
                       }
            # command cd is handled differently because it is the only one that
            # has effect on sos.
            if cmd.startswith('cd ') or cmd.startswith('cd\t'):
                to_dir = cmd[3:].strip()
                try:
                    os.chdir(os.path.expanduser(os.path.expandvars(to_dir)))
                except Exception as e:
                    self.send_response(self.iopub_socket, 'stream',
                        {'name': 'stderr', 'text': repr(e)})
                    return  {'status': 'error',
                        'ename': e.__class__.__name__,
                        'evalue': str(e),
                        'traceback': [],
                        'execution_count': self.execution_count,
                       }
                self.send_response(self.iopub_socket, 'stream',
                    {'name': 'stdout', 'text': os.getcwd()})
                return {'status': 'ok',
                        # The base class increments the execution count
                        'execution_count': self.execution_count,
                        'payload': [],
                        'user_expressions': {},
                       }
            with self.redirect_sos_io():
                try:
                    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    out, err = p.communicate()
                    sys.stdout.write(out.decode())
                    sys.stderr.write(err.decode())
                    ret = p.returncode
                    sys.stderr.flush()
                    sys.stdout.flush()
                    return {'status': 'ok',
                        # The base class increments the execution count
                        'execution_count': self.execution_count,
                        'payload': [],
                        'user_expressions': {},
                       }
                except Exception as e:
                    sys.stderr.flush()
                    sys.stdout.flush()
                    return  {'status': 'error',
                        'ename': e.__class__.__name__,
                        'evalue': str(e),
                        'traceback': [],
                        'execution_count': self.execution_count,
                       }
        else:
            command_line = self.options
        #
        try:
            try:
                if mode == 'dict':
                    res = self.sosdict(command_line)
                elif self.kernel != 'sos':
                    # handle string interpolation before sending to the underlying kernel
                    try:
                        new_code = interpolate(code, sigil='${ }', local_dict=env.sos_dict._dict)
                        if new_code != code:
                            code = new_code
                            self.send_response(self.iopub_socket, 'stream',
                                {'name': 'stdout', 'text':
                                new_code.strip() + '\n## -- End interpolated text --\n'})
                    except Exception as e:
                        self.send_response(self.iopub_socket, 'stream',
                            {'name': 'stdout', 'text': 'Failed to interpolate {}: {}'.format(short_repr(code), e)})
                    return self.run_cell(code, store_history)
                else:
                    code = dedent(code)
                    with self.redirect_sos_io():
                        try:
                            res = self.executor.run_interactive(code, command_line)
                            sys.stderr.flush()
                            sys.stdout.flush()
                        except Exception:
                            sys.stderr.flush()
                            sys.stdout.flush()
                            self.send_response(self.iopub_socket, 'display_data',
                                {
                                    'source': 'SoS',
                                    'metadata': {},
                                    'data': { 'text/html': HTML('<hr color="black" width="60%">').data}
                                })
                            raise
                        except KeyboardInterrupt:
                            return {'status': 'abort', 'execution_count': self.execution_count}
                    #
                    if not silent:
                        start_output = True
                        # Send standard output
                        if '__step_report__' in env.sos_dict and os.path.isfile(env.sos_dict['__step_report__']):
                            with open(env.sos_dict['__step_report__']) as sr:
                                sos_report = sr.read()
                            with open(self.report_file, 'a') as summary_report:
                                summary_report.write(sos_report + '\n\n')
                            if sos_report.strip():
                                self.send_response(self.iopub_socket, 'display_data',
                                    {
                                        'source': 'SoS',
                                        'metadata': {},
                                        'data': {'text/markdown': sos_report}
                                    })
                                start_output = False
                        #
                        if '__step_input__' in env.sos_dict:
                            input_files = env.sos_dict['__step_input__']
                        else:
                            input_files = []
                        if '__step_output__' in env.sos_dict:
                            output_files = env.sos_dict['__step_output__']
                            if output_files is None:
                                output_files = []
                        else:
                            output_files = []
                        # use a table to list input and/or output file if exist
                        if input_files or output_files:
                            if not start_output:
                                self.send_response(self.iopub_socket, 'display_data',
                                    {
                                        'source': 'SoS',
                                        'metadata': {},
                                        'data': { 'text/html': HTML('<hr color="black" width="60%">').data}
                                    })
                            self.send_response(self.iopub_socket, 'display_data',
                                    {
                                        'source': 'SoS',
                                        'metadata': {},
                                        'data': { 'text/html':
                                            HTML('''<pre> input: {}\noutput: {}\n</pre>'''.format(
                                            ', '.join('<a target="_blank" href="{0}">{0}</a>'.format(x) for x in input_files),
                                            ', '.join('<a target="_blank" href="{0}">{0}</a>'.format(x) for x in output_files))).data
                                        }
                                    })
                        # Send images, if any
                        for filename in output_files:
                            self.send_response(self.iopub_socket, 'stream',
                                 {'name': 'stdout', 'text': '\n> ' + filename + ' ({})'.format(pretty_size(os.path.getsize(filename)))})
                            previewer = [x for x in self.previewer.keys() if fnmatch.fnmatch(os.path.basename(filename), x)]
                            if not previewer:
                                continue
                            else:
                                # choose the longest matching pattern (e.g. '*' and '*.pdf', choose '*.pdf')
                                previewer_name = max(previewer, key=len)
                                previewer_func = self.previewer[previewer_name]
                                if not previewer_func:
                                    continue
                                if not callable(previewer_func):
                                    raise RuntimeError('Previewer {} is not callable'.format(previewer_name))
                                try:
                                    result = previewer_func(filename)
                                    if not result:
                                        continue
                                    if isinstance(result, str):
                                        self.send_response(self.iopub_socket, 'stream',
                                            {'name': 'stdout', 'text': '\n'+result})
                                    else:
                                        msg_type, msg_data = result
                                        self.send_response(self.iopub_socket, msg_type,
                                            {'source': filename, 'data': msg_data, 'metadata': {}})
                                except Exception as e:
                                    self.send_response(self.iopub_socket, 'stream',
                                        {'name': 'stderr', 'text': 'Failed to preview {}: {}'.format(filename, e) })
            except Exception as e:
                stream_content = {'name': 'stderr', 'text': str(e)}
                self.send_response(self.iopub_socket, 'stream', stream_content)
                return  {'status': 'error',
                    'ename': e.__class__.__name__,
                    'evalue': str(e),
                    'traceback': [],
                    'execution_count': self.execution_count,
                   }

            # this is Ok, send result back
            if not silent and res is not None:
                format_dict, md_dict = self.format_obj(res)
                self.send_response(self.iopub_socket, 'execute_result',
                    {'execution_count': self.execution_count, 'data': format_dict,
                    'metadata': md_dict})
            #
            # update the underlying shell's namespace with the sos dict so that
            # spyder's object inspector can view the variable.
            self.shell.user_ns.update(env.sos_dict._dict)
            return {'status': 'ok',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                   }
        finally:
            if self.original_kernel is not None:
                self.switch_kernel(self.original_kernel)
                self.original_kernel = None

    def do_shutdown(self, restart):
        #
        for name, (km, kv) in self.kernels.items():
            try:
                km.shutdown_kernel(restart=restart)
            except Exception as e:
                env.logger.warning('Failed to shutdown kernel {}: {}'.format(name, e))

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SoS_Kernel)
