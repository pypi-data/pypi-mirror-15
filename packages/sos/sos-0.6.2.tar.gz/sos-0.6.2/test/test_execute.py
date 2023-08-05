#!/usr/bin/env python3
#
# This file is part of Script of Scripts (SoS), a workflow system
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

# passing string as unicode to python 2 version of SoS
# to ensure compatibility
from __future__ import unicode_literals

import os
import time
import unittest
import shutil

from pysos import SoS_Script
from pysos import __version__
from pysos.utils import env
from pysos.sos_eval import Undetermined
from pysos.sos_executor import Sequential_Executor, ExecuteError
import subprocess

class TestExecute(unittest.TestCase):
    def setUp(self):
        env.reset()

    def testCommandLine(self):
        '''Test command line arguments'''
        result = subprocess.check_output('sos --version', stderr=subprocess.STDOUT, shell=True).decode()
        self.assertTrue(result.startswith('sos {}'.format(__version__)))
        self.assertEqual(subprocess.call('sos', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos -h', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos run -h', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos dryrun -h', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos dryrun scripts/master.sos', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 1)
        # a redirect bug related to blessing
        self.assertEqual(subprocess.call('sos run scripts/slave1.sos -v1 > /dev/null', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos dryrun file://{}/scripts/master.sos'.format(os.getcwd()), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 1)
        self.assertEqual(subprocess.call('sos dryrun scripts/master.sos L', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos show -h', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        #
        self.assertEqual(subprocess.call('sos config -h', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos config -g --get', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos config --get', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos config --set "a=5"', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos config --get a', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)
        self.assertEqual(subprocess.call('sos config --unset a', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True), 0)


    def testInterpolation(self):
        '''Test string interpolation during execution'''
        script = SoS_Script(r"""
[0]
res = ''
b = 200
res += '${b}'
""")
        wf = script.workflow()
        env.shared_vars = ['res']
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['res'], '200')
        #
        script = SoS_Script(r"""
[0]
res = ''
for b in range(5):
    res += '${b}'
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['res'], '01234')
        #
        env.run_mode='dryrun'
        script = SoS_Script(r"""
[0: alias='res']
input: 'a_1.txt', 'b_2.txt', 'c_2.txt', pattern='{name}_{model}.txt'
output: ['{}_{}_processed.txt'.format(x,y) for x,y in zip(name, model)]

""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['res'].output,  ['a_1_processed.txt', 'b_2_processed.txt', 'c_2_processed.txt'])
        #
        env.run_mode='dryrun'
        script = SoS_Script(r"""
[0: alias='res']
input: 'a_1.txt', 'b_2.txt', 'c_2.txt', pattern='{name}_{model}.txt'
output: ['${x}_${y}_process.txt' for x,y in zip(name, model)]

""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['res'].output,  ['a_1_process.txt', 'b_2_process.txt', 'c_2_process.txt'])
        #
        env.run_mode='dryrun'
        script = SoS_Script(r"""
[0: alias='res']
def add_a(x):
    return ['a'+_x for _x in x]

input: 'a_1.txt', 'b_2.txt', 'c_2.txt', pattern='{name}_{model}.txt'
output: add_a(['${x}_${y}_process.txt' for x,y in zip(name, model)])

""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['res'].output,  ['aa_1_process.txt', 'ab_2_process.txt', 'ac_2_process.txt'])

    def testGlobalVars(self):
        '''Test SoS defined variables'''
        script = SoS_Script(r"""
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['SOS_VERSION'], __version__)

    def testFuncDef(self):
        '''Test defintion of function that can be used by other steps'''
        script = SoS_Script(r"""
def myfunc(a):
    sum(range(5))
    return ['a' + x for x in a]

[0: alias='test']
input: myfunc(['a.txt', 'b.txt'])
""")
        wf = script.workflow()
        env.run_mode='dryrun'
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['test'].input, ['aa.txt', 'ab.txt'])
        # in nested workflow?
        script = SoS_Script(r"""
def myfunc(a):
    return ['a' + x for x in a]

[mse: alias='test']
input: myfunc(['a.txt', 'b.txt'])

[1]
sos_run('mse')
""")
        wf = script.workflow()
        env.run_mode='dryrun'
        Sequential_Executor(wf).run()
        #
        # Names defined in subworkflow is not returned to the master dict
        self.assertTrue('test' not in env.sos_dict)

    def testSignature(self):
        self._testSignature(r"""
import time
[*_0]
output: 'temp/a.txt', 'temp/b.txt'
task:
time.sleep(1)
run('''echo "a.txt" > 'temp/a.txt' ''')
run('''echo "b.txt" > 'temp/b.txt' ''')

[1: alias='oa']
dest = ['temp/c.txt', 'temp/d.txt']
input: group_by='single', paired_with='dest'
output: _dest

task:
time.sleep(0.5)
run(''' cp ${_input} ${_dest} ''')
""")
        #
        env.max_jobs = 4
        self._testSignature(r"""
import time
[*_0]
output: 'temp/a.txt', 'temp/b.txt'

task:
time.sleep(1)
run('''echo "a.txt" > 'temp/a.txt' ''')
run('''echo "b.txt" > 'temp/b.txt' ''')

[1: alias='oa']
dest = ['temp/c.txt', 'temp/d.txt']
input: group_by='single', paired_with='dest'
output: _dest

task:
time.sleep(0.5)
run(''' cp ${_input} ${_dest} ''')
""")
        # script format
        env.max_jobs = 4
        self._testSignature(r"""
import time
[*_0]
output: 'temp/a.txt', 'temp/b.txt'

run:
sleep 1
echo "a.txt" > 'temp/a.txt'

run:

echo "b.txt" > 'temp/b.txt'

[1: alias='oa']
dest = ['temp/c.txt', 'temp/d.txt']
input: group_by='single', paired_with='dest'
output: _dest

task:
time.sleep(0.5)
run:
cp ${_input} ${_dest}
""")
        # reset env mode
        env.sig_mode = 'default'
        shutil.rmtree('temp')


    def testSignatureWithoutOutput(self):
        # signature without output file
        self._testSignature(r"""
import time
[*_0]
output: []

run:
sleep 1
[ -d temp ] || mkdir temp
echo "a.txt" > 'temp/a.txt'

run:

echo "b.txt" > 'temp/b.txt'

[1: alias='oa']
dest = ['temp/c.txt', 'temp/d.txt']
input: 'temp/a.txt', 'temp/b.txt', group_by='single', paired_with='dest'
output: _dest

run:
sleep 0.5
cp ${_input} ${_dest}
""")
        # reset env mode
        env.sig_mode = 'default'
        shutil.rmtree('temp')



    def _testSignature(self, text):
        '''Test recognizing the format of SoS script'''
        env.run_mode = 'run'
        script = SoS_Script(text)
        #
        # only the first step
        wf = script.workflow('default_0')
        env.sig_mode = 'ignore'
        start = time.time()
        Sequential_Executor(wf).run()
        self.assertGreater(time.time() - start, 1)
        self.assertTrue(os.path.isfile('temp/a.txt'))
        self.assertTrue(os.path.isfile('temp/b.txt'))
        with open('temp/a.txt') as ta:
            self.assertTrue(ta.read(), 'a.txt')
        with open('temp/b.txt') as tb:
            self.assertTrue(tb.read(), 'b.txt')
        env.sig_mode = 'assert'
        Sequential_Executor(wf).run()
        #
        env.sig_mode = 'ignore'
        wf = script.workflow()
        start = time.time()
        Sequential_Executor(wf).run()
        self.assertGreater(time.time() - start, 1)
        #
        self.assertTrue(os.path.isfile('temp/c.txt'))
        self.assertTrue(os.path.isfile('temp/d.txt'))
        with open('temp/c.txt') as tc:
            self.assertTrue(tc.read(), 'a.txt')
        with open('temp/d.txt') as td:
            self.assertTrue(td.read(), 'b.txt')
        self.assertEqual(env.sos_dict['oa'].output, ['temp/c.txt', 'temp/d.txt'])
        #
        # now in assert mode, the signature should be there
        env.sig_mode = 'assert'
        Sequential_Executor(wf).run()
        #
        env.sig_mode = 'default'
        start = time.time()
        Sequential_Executor(wf).run()
        self.assertLess(time.time() - start, 1.5)
        #
        # change script a little bit
        script = SoS_Script('# comment\n' + text)
        wf = script.workflow()
        env.sig_mode = 'assert'
        Sequential_Executor(wf).run()
        # add some other variable?
        script = SoS_Script('comment = 1\n' + text)
        wf = script.workflow()
        env.sig_mode = 'assert'
        self.assertRaises(RuntimeError, Sequential_Executor(wf).run)

    def testReexecution(self):
        '''Test -f option of sos run'''
        script = SoS_Script('''
import time

[0]
output: 'a.txt'
task:
time.sleep(3)
run('touch ${output}')
''')
        wf = script.workflow()
        try:
            # remove existing output if exists
            os.remove('a.txt')
        except:
            pass
        start = time.time()
        Sequential_Executor(wf).run()
        # regularly take more than 5 seconds to execute
        self.assertGreater(time.time() - start, 2)
        # now, rerun should be much faster
        start = time.time()
        Sequential_Executor(wf).run()
        # rerun takes less than 1 second
        self.assertLess(time.time() - start, 1)
        #
        # force rerun mode
        env.sig_mode = 'ignore'
        start = time.time()
        Sequential_Executor(wf).run()
        # regularly take more than 5 seconds to execute
        self.assertGreater(time.time() - start, 2)
        env.sig_mode = 'default'
        try:
            # remove existing output if exists
            os.remove('a.txt')
        except:
            pass



    def testInput(self):
        '''Test input specification'''
        env.run_mode = 'dryrun'
        script = SoS_Script(r"""
[0:alias='res']
input: '*.py'
output: _input
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertTrue('test_execute.py' in env.sos_dict['res'].output)

    def testForEach(self):
        '''Test for_each option of input'''
        env.run_mode = 'dryrun'
        script = SoS_Script(r"""
[0]
files = ['a.txt', 'b.txt']
names = ['a', 'b', 'c']
c = ['1', '2']
counter = 0
all_names = ''
all_loop = ''

input: 'a.pdf', files, group_by='single', paired_with='names', for_each='c'

all_names += _names[0] + " "
all_loop += _c + " "

counter = counter + 1
""")
        wf = script.workflow()
        env.shared_vars = ['counter', 'all_names', 'all_loop', 'processed']
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['counter'], 6)
        self.assertEqual(env.sos_dict['all_names'], "a b c a b c ")
        self.assertEqual(env.sos_dict['all_loop'], "1 1 1 2 2 2 ")
        #
        # test same-level for loop and parameter with nested list
        script = SoS_Script(r"""
[0]
files = ['a.txt', 'b.txt']
par = [(1, 2), (1, 3), (2, 3)]
res = ['p1.txt', 'p2.txt', 'p3.txt']
processed = []

input: files, for_each='par,res'
output: res

processed.append((_par, _res))
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['processed'], [((1, 2), 'p1.txt'), ((1, 3), 'p2.txt'), ((2, 3), 'p3.txt')])


    def testPairedWith(self):
        '''Test option paired_with '''
        pass

    def testInputPattern(self):
        '''Test option pattern of step input '''
        env.run_mode = 'dryrun'
        #env.verbosity = 4
        script = SoS_Script(r"""
[0]

files = ['a-20.txt', 'b-10.txt']
input: files, pattern=['{name}-{par}.txt', '{base}.txt']
output: ['{}-{}-{}.txt'.format(x,y,z) for x,y,z in zip(_base, _name, _par)]

""")
        wf = script.workflow()
        env.shared_vars=['base', 'name', 'par', '_output']
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['base'], ["a-20", 'b-10'])
        self.assertEqual(env.sos_dict['name'], ["a", 'b'])
        self.assertEqual(env.sos_dict['par'], ["20", '10'])
        self.assertEqual(env.sos_dict['_output'], ["a-20-a-20.txt", 'b-10-b-10.txt'])

    def testOutputPattern(self):
        '''Test option pattern of step output'''
        env.run_mode = 'dryrun'
        #env.verbosity = 4
        script = SoS_Script(r"""
[0]

files = ['a-20.txt', 'b-10.txt']
input: files, pattern=['{name}-{par}.txt', '{base}.txt']
output: pattern=['{base}-{name}-{par}.txt', '{par}.txt']

""")
        wf = script.workflow()
        env.shared_vars = ['base', 'name', 'par', '_output']
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['base'], ["a-20", 'b-10'])
        self.assertEqual(env.sos_dict['name'], ["a", 'b'])
        self.assertEqual(env.sos_dict['par'], ["20", '10'])
        self.assertEqual(env.sos_dict['_output'], ['a-20-a-20.txt', 'b-10-b-10.txt', '20.txt', '10.txt'])


    def testAlias(self):
        '''Test option alias'''
        env.run_mode = 'dryrun'
        script = SoS_Script(r"""
[0: alias='oa']
files = ['a.txt', 'b.txt']
names = ['a', 'b', 'c']
c = ['1', '2']
counter = "0"

input: 'a.pdf', files, group_by='single', paired_with='names', for_each='c'

counter = str(int(counter) + 1)

[1: alias = 'ob']
input: oa.input
output: _input
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['oa'].input, ["a.pdf", 'a.txt', 'b.txt'])
        self.assertEqual(env.sos_dict['ob'].output, ["a.pdf", 'a.txt', 'b.txt'])

    def testFileType(self):
        '''Test input option filetype'''
        env.run_mode = 'dryrun'
        script = SoS_Script(r"""
[0: alias='res']
files = ['a.txt', 'b.txt']
counter = 0

input: 'a.pdf', files, filetype='*.txt', group_by='single'

output: _input

""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['res'].output, ['a.txt', 'b.txt'])
        #
        script = SoS_Script(r"""
[0]
files = ['a.txt', 'b.txt']
counter = 0

input: 'a.pdf', 'b.html', files, filetype=('*.txt', '*.pdf'), group_by='single'

counter += 1
""")
        wf = script.workflow()
        env.shared_vars=['counter']
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['counter'], 3)
        #
        script = SoS_Script(r"""
[0]
files = ['a.txt', 'b.txt']
counter = 0

input: 'a.pdf', 'b.html', files, filetype=lambda x: 'a' in x, group_by='single'

counter += 1
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['counter'], 2)

    def testSkip(self):
        '''Test input option skip'''
        env.run_mode = 'dryrun'
        env.shared_vars = ['counter']
        script = SoS_Script(r"""
[0]
files = ['a.txt', 'b.txt']
counter = 0

input: 'a.pdf', 'b.html', files, skip=counter == 0

counter += 1
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['counter'], 0)

    def testOutputFromInput(self):
        '''Test deriving output files from input files'''
        env.run_mode = 'dryrun'
        script = SoS_Script(r"""
[0: alias='step']
files = ['a.txt', 'b.txt']
counter = 0

input: files, group_by='single'
output: _input[0] + '.bak'

counter += 1
""")
        wf = script.workflow()
        env.shared_vars = ['counter']
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['counter'], 2)
        self.assertEqual(env.sos_dict['step'].output, ['a.txt.bak', 'b.txt.bak'])

    def testWorkdir(self):
        '''Test workdir option for runtime environment'''
        script =  SoS_Script(r"""
[0]

task: workdir='..'

with open('test/result.txt', 'w') as res:
   for file in os.listdir('test'):
       res.write(file + '\n')
""")
        wf = script.workflow()
        Sequential_Executor(wf).run()
        with open('result.txt') as res:
            content = [x.strip() for x in res.readlines()]
            self.assertTrue('test_execute.py' in content)
        os.remove('result.txt')

    def testConcurrency(self):
        '''Test workdir option for runtime environment'''
        env.max_jobs = 5
        script =  SoS_Script(r"""
[0]

repeat = range(4)
input: for_each='repeat'

task: concurrent=False

import time
time.sleep(_repeat + 1)
print('I am {}, waited {} seconds'.format(_index, _repeat + 1))
""")
        wf = script.workflow()
        start = time.time()
        Sequential_Executor(wf).run()
        self.assertGreater(time.time() - start, 9)
        #
        #
        script =  SoS_Script(r"""
[0]

repeat = range(4)
input: for_each='repeat'

task: concurrent=True

import time
time.sleep(_repeat + 1)
print('I am {}, waited {} seconds'.format(_index, _repeat + 1))
""")
        wf = script.workflow()
        start = time.time()
        Sequential_Executor(wf).run()
        self.assertLess(time.time() - start, 6)

    def testRunmode(self):
        '''Test the runmode decoration'''
        script = SoS_Script(r"""
from pysos import SoS_Action

@SoS_Action(run_mode='run')
def fail():
    return 1

[0]
a = fail()
""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        env.shared_vars=['a']
        Sequential_Executor(wf).run()
        # should return 0 in dryrun mode
        self.assertTrue(isinstance(env.sos_dict['a'], Undetermined))
        #

        env.run_mode = 'run'
        Sequential_Executor(wf).run()
        # shoulw return 1 in run mode
        self.assertEqual(env.sos_dict['a'], 1)

    def testReadonlyVarsInGalobal(self):
        '''Test vars defined in global section are readonly'''
        script = SoS_Script(r"""

a = 10

[0]

a += 1

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        self.assertRaises(RuntimeError, Sequential_Executor(wf).run)

    def testReadonlyVarsInParameters(self):
        '''Test vars defined in global section are readonly'''
        script = SoS_Script(r"""

a = 10
import random

[parameters]

b = random.randint(0, 100000)

[a_1]

[default]
sos_run('a+a')

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        self.assertRaises((ExecuteError, RuntimeError), Sequential_Executor(wf).run)

    def testPassingVarsToNestedWorkflow(self):
        '''Test if variables can be passed to nested workflows'''
        script = SoS_Script(r"""

import time
import random

[nested]
print('I am nested ${nested} with seed ${seed}')

[0]
reps = range(5)
input: for_each='reps'
task: concurrent=True
nested = _reps
seed = random.randint(1, 1000)
print('Passing ${seed} to ${nested}')
sos_run('nested')

""")
        env.max_jobs = 1
        wf = script.workflow()
        Sequential_Executor(wf).run()

    def testUserDefinedFunc(self):
        '''Test the use of user-defined functions in SoS script'''
        script = SoS_Script(r"""

def myfunc():
  return 'a'

[1: alias='test']
output: myfunc()

myfunc()

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['test'].output, ['a'])
        # User defined function should also work under nested workflows
        # This is difficult because the 'local namespace' is usually
        # not seen inside function definition. The solution now is to
        # use a single workspace.
        script = SoS_Script(r"""

def myfunc():
    # test if builtin functions (sum and range) can be used here.
    return 'a' + str(sum(range(10)))

[1: alias='test']
output: [myfunc() for i in range(10)][0]

myfunc()

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['test'].output, ['a45'])

    def testReadOnlyStepVars(self):
        '''Test if the step variables can be changed.'''
        #
        script = SoS_Script(r"""
[1: alias='test']
output: 'a.txt'

[2]
test.output=['ab.txt']

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        self.assertRaises((RuntimeError, ExecuteError), Sequential_Executor(wf).run)

    def testReadOnlyInputOutputVars(self):
        '''Test readonly input output vars'''
        script = SoS_Script(r"""
[1: alias='test']
output: 'a.txt'
_output = ['b.txt']

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        # I would like to disallow setting _output directly, but this is
        # not the case now.
        self.assertRaises(RuntimeError, Sequential_Executor(wf).run)

    def testLocalNamespace(self):
        '''Test if steps are well separated.'''
        script = SoS_Script(r"""
[1]
a = 1

[2]
# this should fail because a is defined in another step
print(a)

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        # I would like to disallow accessing variables defined
        # in other cases.
        self.assertRaises((RuntimeError, ExecuteError), Sequential_Executor(wf).run)
        # however, alias should be sent back
        script = SoS_Script(r"""
[1: alias='shared']
input: 'a.txt'
output: 'b.txt'

[2]
# this should fail because a is defined in another step
print(shared.input)

output: shared.input

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        # I would like to disallow accessing variables defined
        # in other cases.
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['shared'].output, ['b.txt'])
        #
        # this include other variables set in the step
        script = SoS_Script(r"""
[1: alias='shared']
input: 'a.txt'
output: 'b.txt'

c = 'c.txt'
d = 1

[2: alias='d']
# this should fail because a is defined in another step
print(shared.input)

output: shared.c

e = shared.d + 1

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        # I would like to disallow accessing variables defined
        # in other cases.
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['shared'].c, 'c.txt')
        self.assertEqual(env.sos_dict['d'].e, 2)
        #
        # aliased variables are readonly
        script = SoS_Script(r"""
[1: alias='shared']
input: 'a.txt'
output: 'b.txt'

c = 'c.txt'
d = 1

[2: alias='d']
# this should fail because a is defined in another step
print(shared.input)

output: shared.c

shared.d += 1

""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        # I would like to disallow accessing variables defined
        # in other cases.
        self.assertRaises((ExecuteError, RuntimeError), Sequential_Executor(wf).run)

    def testSklearnImportFailure(self):
        '''Test problem with Sklean when using Celery/multiprocessing'''
        script = SoS_Script('''
import sklearn

[run]
print(0)
''')
        wf = script.workflow()
        Sequential_Executor(wf).run()


    def testCollectionOfErrors(self):
        '''Test collection of errors when running in dryrun mode.'''
        script = SoS_Script('''
[0]
check_command('a1')
[1: skip=blah]

check_command('a2')
[2: alias=unrecognized]
check_command('a3')
[3]
check_command('a4')

''')
        wf = script.workflow()
        env.run_mode = 'dryrun'
        # we should see a single error with 4 messages.
        try:
            Sequential_Executor(wf).run()
        except Exception as e:
            self.assertEqual(len(e.errors), 6)


    def testDryrunTimeout(self):
        '''Test if any action should exit in five seconds in dryrun mode'''
        sos_config_file = os.path.expanduser('.sos/config.json')
        move_back = False
        if os.path.isfile(sos_config_file):
            move_back = True
            os.rename(sos_config_file, sos_config_file + '.bak')
        script = SoS_Script('''
[0]
import time
time.sleep(8)

''')
        wf = script.workflow()
        env.run_mode = 'run'
        # this should be ok
        Sequential_Executor(wf).run()
        #
        env.run_mode = 'dryrun'
        self.assertRaises(ExecuteError, Sequential_Executor(wf).run)
        #
        # now, if I have a configuration file, the default value can be changed
        if not os.path.isdir(os.path.expanduser('.sos')):
            os.mkdir(os.path.expanduser('.sos'))
        with open(sos_config_file, 'w') as sos_config:
            sos_config.write('''
#
# global sos configuration file
#
{
    "sos_dryrun_timeout": 10
}
''')
        # now we can rerun the script, and it should pass
        Sequential_Executor(wf).run()
        # clean up
        if move_back:
            os.rename(sos_config_file + '.bak', sos_config_file)
        else:
            os.remove(sos_config_file)



    def testSearchPath(self):
        '''Test if any action should exit in five seconds in dryrun mode'''
        sos_config_file = os.path.expanduser('.sos/config.json')
        move_back = False
        if os.path.isfile(sos_config_file):
            move_back = True
            os.rename(sos_config_file, sos_config_file + '.bak')
        #
        with open(sos_config_file, 'w') as sos_config:
            sos_config.write('''
#
# global sos configuration file
#
{{
    "sos_path": ["{0}/crazy_path", "{0}/crazy_path/more_crazy/"]
}}
'''.format(os.getcwd()))
        #
        if not os.path.isdir('crazy_path'):
            os.mkdir('crazy_path')
            os.mkdir('crazy_path/more_crazy')
        with open('crazy_path/crazy_master.sos', 'w') as crazy:
            crazy.write('''
[0]
sos_run('cc', source='crazy_slave.sos')

''')
        with open('crazy_path/more_crazy/crazy_slave.sos', 'w') as crazy:
            crazy.write('''
[cc_0]
print('hay, I am crazy')
''')

        script = SoS_Script(filename='crazy_master.sos')
        script.workflow()
        env.run_mode = 'run'
        #
        shutil.rmtree('crazy_path')
        if move_back:
            os.rename(sos_config_file + '.bak', sos_config_file)
        else:
            os.remove(sos_config_file)

    def testDynamicOutput(self):
        '''Testing dynamic output'''
        #
        if not os.path.isdir('temp'):
            os.mkdir('temp')
        #
        script = SoS_Script('''
[10: alias='test']
ofiles = []
output: ofiles, dynamic=True

for i in range(4):
    ff = 'temp/something{}.html'.format(i)
    ofiles.append(ff)
    with open(ff, 'w') as h:
       h.write('a')
''')
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['test'].output, ['temp/something{}.html'.format(x) for x in range(4)])
        #
        shutil.rmtree('temp')

    def testDynamicInput(self):
        '''Testing dynamic input'''
        #
        if os.path.isdir('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')
        #
        script = SoS_Script('''
[1]

for i in range(5):
    run('touch temp/test_${i}.txt')


[10: alias='test']
input: 'temp/*.txt', group_by='single', dynamic=True
output: 'temp/*.txt.bak', dynamic=True

run:
touch ${_input}.bak
''')
        wf = script.workflow()
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['test'].output, ['temp/test_{}.txt.bak'.format(x) for x in range(5)])
        # this time we use th existing signature
        Sequential_Executor(wf).run()
        self.assertEqual(env.sos_dict['test'].output, ['temp/test_{}.txt.bak'.format(x) for x in range(5)])
        #
        shutil.rmtree('temp')


    def testAssignmentAfterInput(self):
        '''Testing assignment after input should be usable inside step process.'''
        #
        if os.path.isdir('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')
        #
        env.sig_mode = 'ignore'
        script = SoS_Script('''
[1]
rep = range(5)
input:  for_each='rep'
output: 'temp/${_rep}.txt'

# ff should change and be usable inside run
ff = '${_rep}.txt'
run:
echo ${ff}
touch temp/${ff}
''')
        wf = script.workflow()
        Sequential_Executor(wf).run()
        #
        #shutil.rmtree('temp')


if __name__ == '__main__':
    unittest.main()
