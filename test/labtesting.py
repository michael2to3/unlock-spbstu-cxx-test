import copy
import codecs
import collections
import inspect
import locale
import math
import os
import random
import re
import string
import sys
import subprocess
import tempfile
from time import time
import xml.etree.ElementTree as ET

OUTPUT_LIMIT = 20 * 1024

class Result(object):
    SUCCEEDED = 0
    FAILED    = 1
    VALGRIND  = 2
    TIMED_OUT = 3

    OUTPUT_AUTO   = "auto"
    OUTPUT_ALWAYS = "always"
    OUTPUT_NEVER  = "never"

    def __init__(self, name, status, args = None, exitCode = 0, input = None, output = None, error = None, expected = None, valgrind = None, elapsedTime = None):
        self.name = name
        if (valgrind == None):
            self.status = status
        else:
            self.status = self.VALGRIND
        self.args = args
        self.exitCode = exitCode
        self.input = input
        self.output = output
        self.error = error
        self.expected = expected
        self.valgrind = valgrind
        self.elapsedTime = elapsedTime
        self.showOutput = self.OUTPUT_AUTO

    @property
    def succeeded(self):
        return self.status == self.SUCCEEDED

    @succeeded.setter
    def succeeded(self, value):
        if (self.status == self.FAILED) and value:
            self.status = self.SUCCEEDED

    def formatXml(self, parent):
        def escape(s):
            start = time()
            begin = 0
            current = 0
            strings = []

            for c in s:
                if (c == '\n') or (c == '\r') or (c == '\t') or ((' ' <= c) and (ord(c) < 127)):
                    current += 1
                else:
                    strings.append(s[begin:current])
                    strings.append('\\' + hex(ord(c))[1:])
                    current += 1
                    begin = current
            if begin != current:
                strings.append(s[begin:current])

            result = ''.join(strings)

            return result

        statusString = 'unknown'
        if self.status == self.SUCCEEDED:
            statusString = 'succeeded'
        elif self.status == self.FAILED:
            statusString = 'failed'
        elif self.status == self.VALGRIND:
            statusString = 'valgrind'
        elif self.status == self.TIMED_OUT:
            statusString = 'timedOut'

        attrs = {
            'name': self.name,
            'status': statusString
        }

        if self.args:
            attrs['arguments'] = ' '.join(['"' + arg + '"' for arg in self.args])

        if self.exitCode != None:
            attrs['exitCode'] = str(self.exitCode)

        if self.elapsedTime != None:
            attrs['elapsedTime'] = str(self.elapsedTime)

        test = ET.SubElement(parent, 'test', attrib = attrs)

        if self.input != None:
            ET.SubElement(test, 'input', attrib = { 'omit' : str((self.input != None) and (len(self.input) > OUTPUT_LIMIT)) }).text = escape(self.input)

        if self.output != None:
            ET.SubElement(test, 'output', attrib = {
                'omit' : str((self.output != None) and (len(self.output) > OUTPUT_LIMIT)),
                'show' : self.showOutput
            }).text = escape(self.output)

        if self.error != None:
            ET.SubElement(test, 'error', attrib = { 'omit' : str((self.error != None) and (len(self.error) > OUTPUT_LIMIT)) }).text = escape(self.error)

        if self.expected != None:
            if isinstance(self.expected, collections.Sequence) and not isinstance(self.expected, str):
                node = ET.SubElement(test, 'expected')
                for item in self.expected:
                    ET.SubElement(node, 'option', attrib = { 'omit' : str((item != None) and (len(item) > OUTPUT_LIMIT)) }).text = escape(item)
            else:
                ET.SubElement(test, 'expected', attrib = { 'omit' : str((self.expected != None) and (len(self.expected) > OUTPUT_LIMIT)) }).text = escape(self.expected)

        if self.valgrind != None:
            test.append(self.valgrind)


def test(name):
    """Test decorator to override some test parameters like name which is
    derived from test function by default.
    """

    def construct(fn):
        def wrapped(*args, **kwargs):
            result = fn(*args, **kwargs)
            if result.name == None:
                result.name = name
            return result

        return wrapped

    return construct


def requires(lab):
    """Test decorator to check that required lab is enabled in course.
    """

    def construct(fn):
        def wrapped(*args, **kwargs):
            labs = os.environ.get('COURSE_LABS', lab).split()

            if lab in labs:
                return fn(*args, **kwargs)
            else:
                return None

        return wrapped

    return construct


class Lab(object):
    def __init__(self, student, lab, name = None):
        self.student = student
        self.lab = lab

        if name:
            self.name = name
        else:
            self.name = 'Lab ' + str(self.lab)

        self._home = os.path.abspath(os.path.dirname(sys.argv[0]))


    def _getTemplateFile(self, templateSuffix):
        file = self._home + "/templates/" + self.lab + templateSuffix

        if os.path.exists(file):
            return file

        return self._home + "/templates/" + self.lab.split('.', 1)[0] + templateSuffix

    def _getStudentFirstName(self):
        return self.student.split('.')[1]

    def _getStudentLastName(self):
        return self.student.split('.')[0]

    def _isclose(self, a, b, rel_tol=1e-4, abs_tol=0.0):
        '''
        Python 2 implementation of Python 3.5 math.isclose()
        https://hg.python.org/cpython/file/tip/Modules/mathmodule.c#l1993
        '''
        # sanity check on the inputs
        if rel_tol < 0 or abs_tol < 0:
            raise ValueError("tolerances must be non-negative")

        # short circuit exact equality -- needed to catch two infinities of
        # the same sign. And perhaps speeds things up a bit sometimes.
        if a == b:
            return True

        # This catches the case of two infinities of opposite sign, or
        # one infinity and one finite number. Two infinities of opposite
        # sign would otherwise have an infinite relative tolerance.
        # Two infinities of the same sign are caught by the equality check
        # above.
        if math.isinf(a) or math.isinf(b):
            return False

        # now do the regular computation
        # this is essentially the "weak" test from the Boost library
        diff = math.fabs(b - a)
        result = (((diff <= math.fabs(rel_tol * b)) or
                   (diff <= math.fabs(rel_tol * a))) or
                  (diff <= abs_tol))
        return result

    def _invokeExternal(self, command, args, input = None):
        env = copy.copy(os.environ)

        # Always invoke silent actions
        env['SILENT'] = 'yes'

        start = time()
        process = subprocess.Popen([command] + args,
                                   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                   env = env)

        status = Result.FAILED
        (out, err) = process.communicate(bytes(input, 'UTF-8') if input != None else None)
        out = out.decode('UTF-8')
        err = err.decode('UTF-8')
        elapsedTime = round(time() - start, 3)

        return Result(None, status, args = args, exitCode = process.returncode, input = input,
                      output = out, error = err, valgrind = None, elapsedTime = elapsedTime)

    def _fileExists(self, filename):
        result = self._invokeExternal("test", ["-f", filename])
        result.succeeded = (result.exitCode == 0)
        return result

    def _invoke(self, target, student, lab, args, input, faults):
        valgrindFile = None
        env = copy.deepcopy(os.environ)

        if 'VALGRIND' in env:
            valgrindFile = tempfile.NamedTemporaryFile()
            env['VALGRIND'] = env['VALGRIND'] + ' --xml=yes --xml-file="' + valgrindFile.name + '"'

        if faults and ('FAULT_INJECTION_LIB' in env):

            if sys.platform == 'darwin':
                print("Handling Darwin")
                env['FAULT_INJECTION_CONFIG'] = 'DYLD_FORCE_FLAT_NAMESPACE=1 DYLD_INSERT_LIBRARIES=' + env['FAULT_INJECTION_LIB']
            elif sys.platform.startswith('linux'):
                print("Handling Linux")
                env['FAULT_INJECTION_CONFIG'] = 'LD_PRELOAD=' + env['FAULT_INJECTION_LIB']
            else:
                print("Unknown platform", sys.platform)

        # Always invoke silent actions
        env['SILENT'] = 'yes'
        # Enforce current locale
        env['LANG'] = locale.setlocale(locale.LC_ALL, None);
        # But keep standard messages
        env['LC_MESSAGES'] = 'C';

        start = time()
        process = subprocess.Popen(['make', target + student + '/' + str(lab), 'ARGS=' + ' '.join(['"' + arg + '"' for arg in args])],
                                   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                   env = env)

        status = Result.FAILED
        out = None
        err = None
        if callable(input):
            try:
                input()
            except:
                pass
            out = process.stdout.read()
            err = process.stderr.read()
            process.wait()
        else:
            (out, err) = process.communicate(bytes(input, 'UTF-8') if input != None else None)

        try:
            out = out.decode('UTF-8')
        except Exception as e:
            out = '*** Output decoding failed with ' + str(e)

        try:
            err = err.decode('UTF-8')
        except Exception as e:
            err = '*** Error output decoding failed with ' + str(e)

        if process.returncode != 0:
            if re.search('^make:.*\[[^]]*\]\\s+Killed.*$', err, re.MULTILINE) \
               or re.search('^make:.*\[[^]]*\]\\s+Error 137.*$', err, re.MULTILINE):
                err += 'Program is timed out\n'
                status = Result.TIMED_OUT
        elapsedTime = round(time() - start, 3)

        if valgrindFile:
            try:
                valgrindOutput = ET.parse(valgrindFile).getroot()
                valgrindFile.close()
                if len(valgrindOutput.findall('.//error')) == 0:
                    # There is no errors in Valgrind so output is not required
                    valgrindOutput = None
            except:
                valgrindOutput = None
        else:
            valgrindOutput = None

        return Result(None, status, args = args, exitCode = process.returncode, input = input if not callable(input) else None,
                      output = out, error = err, valgrind = valgrindOutput, elapsedTime = elapsedTime)

    def runTests(self, report):
        report.set('name', self.name)

        succeeded = 0
        failed = 0
        for item in dir(self):
            attr = getattr(self, item)

            if inspect.ismethod(attr) and (item[0:4] == 'test'):
                result = attr()
                if result != None:
                    if result.name == None:
                        result.name = re.sub(r"([A-Z]|[0-9]+)", r" \1", item[4:]).strip()
                    result.formatXml(report)
                    if result.status == Result.SUCCEEDED:
                        sys.stdout.write('.')
                        succeeded += 1
                    elif result.status == Result.VALGRIND:
                        sys.stdout.write('V')
                        failed += 1
                    elif result.status == Result.TIMED_OUT:
                        sys.stdout.write('T')
                        failed += 1
                    else:
                        sys.stdout.write('F')
                        failed += 1
                    sys.stdout.flush()
            elif inspect.isclass(attr.__class__) and item[0:4] == 'test' and ('runTests' in dir(attr)):
                group = ET.SubElement(report, 'group')

                (subSucceeded, subFailed) = attr.runTests(group)
                succeeded += subSucceeded
                failed += subFailed

        return (succeeded, failed)

    def execute(self, args = [], input = None, faults = False):
        return self._invoke('run-', self.student, self.lab, args, input, faults)

    def executeUnitTests(self, args = [], input = None, lab = None, faults = False):
        return self._invoke('test-', self.student, self.lab if lab == None else lab, args, input, faults)

    def generateString(self, minLength, maxLength, chars, firstLastChars = None):
        length = minLength if minLength == maxLength else random.randint(minLength, maxLength) - 1
        result = random.choice(firstLastChars if firstLastChars else chars)
        for i in range(1, length):
            result += random.choice(chars)
        result += random.choice(firstLastChars if firstLastChars else chars)

        return result

    def generateRational(self, scale = 1000):
        return (random.random() - 0.5) * 2 * scale

    def randomObjectLimit(self, min, max):
        if os.getenv('TEST_MAX_OBJECTS', 'no') == 'yes':
            return max
        else:
            return min if min == max else random.randint(min, max)


class RequiredParameterValidation(Lab):
    def __init__(self, student, lab, name = None):
        super(RequiredParameterValidation, self).__init__(student, lab, name if name else 'Required Parameter Validation')

    def testMissingParameters(self):
        result = self.execute()

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code with a message in standard error'

        return result

class SingleIntegerParameterRangeValidation(RequiredParameterValidation):
    def __init__(self, student, lab, min, max, name = None):
        super(SingleIntegerParameterRangeValidation, self).__init__(student, lab,
                                                                    name if name else 'Required integer parameter in range [' + str(min) + ', ' + str(max) + ']')

        self.min = min
        self.max = max

    def testParameterValueTooSmall(self):
        args = [str(self.min - 1)]

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code with a message in standard error'

        return result

    def testParameterTooBig(self):
        args = [str(self.max + 1)]

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code with a message in standard error'

        return result


class IntegerSequenceMixin(object):
    def __init__(self, args):
        self._integerSequenceArgs = args

    def testInvalidNumber(self):
        input = self.generateString(5, 10, string.ascii_letters)

        result = self.execute(args = self._integerSequenceArgs, input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testInvalidNumberInAMiddle(self):
        input = str(random.randint(-1000, 1000)) + '\n' + self.generateString(5, 10, string.ascii_letters) + ' ' + str(random.randint(-1000, 1000))

        result = self.execute(args = self._integerSequenceArgs, input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testRationalNumber(self):
        input = str(self.generateRational())

        result = self.execute(args = self._integerSequenceArgs, input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testRationalNumberInAMiddle(self):
        input = str(random.randint(-1000, 1000)) + '\n' + str(self.generateRational()) + ' ' + str(random.randint(-1000, 1000))

        result = self.execute(args = self._integerSequenceArgs, input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result


def main(tests):
    if len(sys.argv) < 3:
        print("Not enough parameters", file=sys.stderr)
        sys.exit(1)

    # By default, "C" locale is enforced. Individual tests
    # can overwrite it
    locale.setlocale(locale.LC_ALL, "C")

    reportFile = sys.argv[2]

    random.seed()

    report = ET.Element('report')

    (succeeded, failed) = tests.runTests(report)

    if failed == 0:
        print(" SUCCEEDED")
    else:
        print(" FAILED")
    print("Succeeded:", succeeded)
    print("Failed:   ", failed)

    if reportFile == "-":
        ET.ElementTree(report).write(sys.stdout.buffer)
        sys.stdout.write('\n')
    else:
        with open(reportFile, "wb") as file:
            file.write(bytes('<?xml version="1.0" encoding="utf-8" ?>\n', 'ascii'))
            ET.ElementTree(report).write(file, xml_declaration = False)
            file.write(bytes('\n', 'ascii'))

    if failed == 0:
        sys.exit(0)
    else:
        sys.exit(2)
