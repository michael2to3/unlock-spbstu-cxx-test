#!/usr/bin/env python3

from socketserver import DatagramRequestHandler
from test.labtesting import Lab, main
import sys
import tempfile

def InvCmd():
    return '<INVALID COMMAND>'

class LabT3(Lab):
    def __init__(self, student):
        super(LabT3, self).__init__(student, 'T3')

    def _newlineSep(self, dataset):
        returnable = ''
        for data in dataset:
            returnable = returnable + data + '\n'
        return returnable

    def _clarify(self, dataset, expected):
        returnable = 'With data:\n'
        for data in dataset:
            returnable = returnable + '\t' + data + '\n'
        returnable = returnable + 'Expected result is:\n'
        for data in expected:
            returnable = returnable + '\t' + data + '\n'
        return returnable

    def _makeForFile(self, dataset):
        return bytes(self._newlineSep(dataset), 'utf-8')

    def _process(self, dataset, commands, expected):
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._makeForFile(dataset))
            source.flush()
            args = [source.name]

            result = self.execute(args = args, input = self._newlineSep(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._newlineSep(expected)) and (len(result.error) == 0)
            result.expected = self._clarify(dataset, expected)
            return result

    def testNotEnoughArgs(self):
        result = self.execute()
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testTooManyArgs(self):
        args = ['one', 'two']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testUnexpectedCommand(self):
        dataset = [
          '3 (0;0) (1;0) (0;1)'
        ]
        commands = [
          'UNEXPECTED COMMAND'
        ]
        expected = [
          InvCmd()
        ]
        return self._process(dataset, commands, expected)

    def testCommonEvenOddAreaCommadsWithoutShapes(self):
        dataset = [
          ''
        ]
        commands = [
          'AREA EVEN',
          'AREA ODD'
        ]
        expected = [
          '0.0',
          '0.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonEvenOddAreaCommadsWithEvenAndOddShapes(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '4 (0;0) (2;0) (2;2) (0;2)'
        ]
        commands = [
          'AREA EVEN',
          'AREA ODD'
        ]
        expected = [
          '4.0',
          '2.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonEvenOddAreaCommadsWithSeveralEvenAndOddShapes(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '4 (0;0) (2;0) (2;2) (0;2)',
          '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)',
          '4 (0;0) (2;0) (2;2) (0;2)'
        ]
        commands = [
          'AREA EVEN',
          'AREA ODD'
        ]
        expected = [
          '36.0',
          '32.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonMeanAreaCommandWithoutShapes(self):
        dataset = [
          ''
        ]
        commands = [
          'AREA MEAN'
        ]
        expected = [
          InvCmd()
        ]
        return self._process(dataset, commands, expected)

    def testCommonMeanAreaCommandWithShape(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)'
        ]
        commands = [
          'AREA MEAN'
        ]
        expected = [
          '2.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonMeanAreaCommandWithSeveralShapes(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '3 (0;0) (2;0) (0;2)',
          '3 (0;0) (4;0) (0;3)'
        ]
        commands = [
          'AREA MEAN'
        ]
        expected = [
          '3.3'
        ]
        return self._process(dataset, commands, expected)

    def testCommonVertexAreaCommadWithoutShapes(self):
        dataset = [
          ''
        ]
        commands = [
          'AREA 3',
        ]
        expected = [
          '0.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonVertexAreaCommadWithInvalidAmountsOfVertexesShapes(self):
        dataset = [
          ''
        ]
        commands = [
          'AREA 0',
          'AREA 1',
          'AREA 2'
        ]
        expected = [
          InvCmd(),
          InvCmd(),
          InvCmd()
        ]
        return self._process(dataset, commands, expected)

    def testCommonVertexAreaCommadWithShape(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)'
        ]
        commands = [
          'AREA 8'
        ]
        expected = [
          '28.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonVertexAreaCommadWithSeveralShapes(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '4 (0;0) (2;0) (2;2) (0;2)',
          '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)',
          '4 (0;0) (2;0) (2;2) (0;2)'
        ]
        commands = [
          'AREA 4'
        ]
        expected = [
          '8.0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonMaxAreaVertexesCommadWithoutShapes(self):
        dataset = [
          ''
        ]
        commands = [
          'MAX AREA',
          'MAX VERTEXES'
        ]
        expected = [
          InvCmd(),
          InvCmd()
        ]
        return self._process(dataset, commands, expected)

    def testCommonMaxAreaVertexesCommadWithShape(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)'
        ]
        commands = [
          'MAX AREA',
          'MAX VERTEXES'
        ]
        expected = [
          '28.0',
          '8'
        ]
        return self._process(dataset, commands, expected)

    def testCommonMaxAreaVertexesCommadWithSeveralShapes(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '4 (0;0) (2;0) (2;2) (0;2)',
          '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)',
          '4 (0;0) (2;0) (2;2) (0;2)'
        ]
        commands = [
          'MAX AREA',
          'MAX VERTEXES'
        ]
        expected = [
          '30.0',
          '8'
        ]
        return self._process(dataset, commands, expected)

    def testCommonCountEvenOddVertexesCommadWithoutShapes(self):
        dataset = [
          ''
        ]
        commands = [
          'COUNT EVEN',
          'COUNT ODD',
          'COUNT 3'
        ]
        expected = [
          '0',
          '0',
          '0'
        ]
        return self._process(dataset, commands, expected)

    def testCommonCountVertexesCommadWithIvalidAmountOfVertexes(self):
        dataset = [
          ''
        ]
        commands = [
          'COUNT 0',
          'COUNT 1',
          'COUNT 2'
        ]
        expected = [
          InvCmd(),
          InvCmd(),
          InvCmd()
        ]
        return self._process(dataset, commands, expected)

    def testCommonCountEvenOddVertexesAreaCommadWithShapes(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)',
          '3 (0;0) (2;0) (0;2)'
        ]
        commands = [
          'COUNT ODD',
          'COUNT EVEN',
          'COUNT 3'
        ]
        expected = [
          '2',
          '1',
          '2'
        ]
        return self._process(dataset, commands, expected)

    def testCommonCountEvenOddVertexesAreaCommadWithYetAnotherShapes(self):
        dataset = [
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)',
          '3 (0;0) (2;0) (0;2)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)'
        ]
        commands = [
          'COUNT ODD',
          'COUNT EVEN',
          'COUNT 3'
        ]
        expected = [
          '1',
          '2',
          '1'
        ]
        return self._process(dataset, commands, expected)
    def testUnexpectedDataset(self):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '',
          '0',
          '1 (5;6)',
          '2 (5;5) (5;6)',
          '',
          '4 (5;5) (6;5) (6;6) (;)',
          '8 (0;2) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0) (2;0)',
          '4 (5;5) (;) (6;5) (6;6)',
          '4 (5;5) ((;);(;)) (;) (6;6)',
          '3 (5;5) (6;5) (6;6) (6;6)',
          '3 (5;5) (6;5)',
          '',
          '3 (0;0) (2;0) (0;2)'

        ]
        commands = [
          'COUNT ODD',
          'COUNT EVEN',
          'COUNT 3'
        ]
        expected = [
          '2',
          '1',
          '2'
        ]
        return self._process(dataset, commands, expected)

    def _isSupported(self, command):
        dataset = [
          '3 (0;0) (2;0) (0;2)',
          '3 (0;0) (2;0) (0;2)'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._makeForFile(dataset))
            source.flush()
            args = [source.name]

            result = self.execute(args = args, input = self._newlineSep(command))
            return (result.output != '<INVALID COMMAND>\n') and (result.exitCode == 0) and (len(result.error) == 0)

    def testPermsCommand(self):
        tosupport = [
          'PERMS 3 (2;0) (0;0) (0;2)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (0;0) (2;0) (0;2)',
              '4 (-1;-1) (-1;1) (1;1) (1;-1)',
              '3 (2;0) (0;0) (0;2)',
              '4 (1;1) (1;-1) (-1;-1) (-1;1)',
              '3 (0;0) (-2;0) (0;-2)',
              '3 (0;2) (0;0) (2;0)',
            ]
            commands = [
              'PERMS 3 (2;0) (0;0) (0;2)',
              'PERMS 3 (0;0) (1;0) (0;1)',
              'PERMS 4 (-1;-1) (-1;1) (1;1) (1;-1)',
              'PERMS 2 (0;0) (0;2)'
            ]
            expected = [
              '3',
              '0',
              '2',
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testRectsCommand(self):
        tosupport = [
          'RECTS'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (0;0) (2;0) (0;2)',
              '4 (-1;-1) (-1;1) (2;1) (2;-1)',
              '4 (1;1) (1;-1) (-1;-1) (-1;1)',
              '3 (-1;2) (0;0) (2;0)'
            ]
            commands = [
              'RECTS',
            ]
            expected = [
              '2'
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testRightShapesCommand(self):
        tosupport = [
          'RIGHTSHAPES'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (0;0) (2;0) (0;2)',
              '4 (-1;-1) (-1;1) (2;1) (2;-1)',
              '4 (1;1) (1;-1) (-1;-1) (-1;1)',
              '3 (-1;2) (0;0) (2;0)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)'
            ]
            commands = [
              'RIGHTSHAPES'
            ]
            expected = [
              '4'
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testInframeCommand(self):
        tosupport = [
          'INFRAME 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '4 (2;2) (3;2) (3;3) (2;3)'
            ]
            commands = [
              'INFRAME 4 (-1;-1) (1;0) (1;1) (0;1)',
              'INFRAME 4 (0;0) (1;0) (1;1) (0;1)',
              'INFRAME 4 (1;1) (2;1) (2;2) (1;2)',
              'INFRAME 4 (5;5) (6;5) (6;6) (5;6)',

              'INFRAME 2 (5;5) (5;6)',
              'INFRAME 4 (5;5) (6;5) (6;6) (;)',
              'INFRAME 3 (5;5) (6;5) (6;6) (6;6)',
              'INFRAME 3 (5;5) (6;5)'
            ]
            expected = [
              '<FALSE>',
              '<TRUE>',
              '<TRUE>',
              '<TRUE>',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testSameCommand(self):
        tosupport = [
          'SAME 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '7 (1;1) (1;5) (3;7) (5;7) (7;5) (7;3) (5;1)',
              '7 (-1;-1) (-1;3) (1;5) (3;5) (5;3) (5;1) (3;-1)',
              '4 (2;2) (3;2) (3;3) (2;3)'
            ]
            commands = [
              'SAME 7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              'SAME 4 (0;0) (1;0) (1;1) (0;1)',
              'SAME 4 (1;1) (2;1) (3;3) (1;2)',

              'SAME 2 (5;5) (5;6)',
              'SAME 4 (5;5) (6;5) (6;6) (;)',
              'SAME 3 (5;5) (6;5) (6;6) (6;6)',
              'SAME 3 (5;5) (6;5)'
            ]
            expected = [
              '3',
              '1',
              '0',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testIntersectionsCommand(self):
        tosupport = [
          'INTERSECTIONS 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '4 (2;2) (3;2) (3;3) (2;3)'
            ]
            commands = [
              'INTERSECTIONS 4 (2;2) (3;2) (3;3) (2;3)',
              'INTERSECTIONS 4 (0;0) (2;0) (2;2) (0;2)',
              'INTERSECTIONS 4 (-1;-1) (1;-1) (1;1) (-1;1)',
              'INTERSECTIONS 4 (-2;-2) (-1;-2) (-1;-1) (-2;-1)',

              'INTERSECTIONS 2 (5;5) (5;6)',
              'INTERSECTIONS 4 (5;5) (6;5) (6;6) (;)',
              'INTERSECTIONS 3 (5;5) (6;5) (6;6) (6;6)',
              'INTERSECTIONS 3 (5;5) (6;5)'
            ]
            expected = [
              '2',
              '2',
              '1',
              '0',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testMaxseqCommand(self):
        tosupport = [
          'MAXSEQ 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (1;1) (2;2) (1;2)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '3 (0;0) (1;0) (0;1)',
              '3 (0;0) (1;0) (0;1)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '3 (0;0) (1;0) (0;1)',
              '3 (1;1) (2;2) (1;2)'
            ]
            commands = [
              'MAXSEQ 3 (1;1) (2;2) (1;2)',
              'MAXSEQ 7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              'MAXSEQ 3 (0;0) (1;0) (0;1)',

              'MAXSEQ 2 (5;5) (5;6)',
              'MAXSEQ 4 (5;5) (6;5) (6;6) (;)',
              'MAXSEQ 3 (5;5) (6;5) (6;6) (6;6)',
              'MAXSEQ 3 (5;5) (6;5)'
            ]
            expected = [
              '1',
              '1',
              '2',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])


    def testEchoCommand(self):
        tosupport = [
          'ECHO 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (1;1) (2;2) (1;2)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '3 (0;0) (1;0) (0;1)',
              '3 (0;0) (1;0) (0;1)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '3 (0;0) (0;1) (1;0)',
              '3 (1;1) (2;2) (1;2)'
            ]
            commands = [
              'ECHO 3 (1;1) (2;2) (1;2)',
              'COUNT 3',
              'AREA 3',

              'ECHO 7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              'COUNT 7',
              'AREA 7',

              'ECHO 3 (0;1) (0;0) (0;1)',
              'COUNT 3',
              'AREA 3',

              'ECHO 2 (5;5) (5;6)',
              'ECHO 4 (5;5) (6;5) (6;6) (;)',
              'ECHO 3 (5;5) (6;5) (6;6) (6;6)',
              'ECHO 3 (5;5) (6;5)'
            ]
            expected = [
              '2', '7', '3.5',
              '2', '4', '120.0',
              '0', '7', '3.5',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testRmechoCommand(self):
        tosupport = [
          'RMECHO 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (1;1) (2;2) (1;2)',
              '3 (1;1) (2;2) (1;2)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '3 (0;0) (1;0) (0;1)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              '3 (0;0) (0;1) (1;0)',
              '3 (0;0) (0;1) (1;0)',
              '3 (1;1) (2;2) (1;2)',
              '3 (1;1) (2;2) (1;2)'
            ]
            commands = [
              'RMECHO 3 (1;1) (2;2) (1;2)',
              'COUNT 3',
              'AREA 3'

              'RMECHO 7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              'COUNT 7',
              'AREA 7'

              'RMECHO 3 (0;0) (1;0) (0;1)',
              'COUNT 3',
              'AREA 3'

              'RMECHO 2 (5;5) (5;6)',
              'RMECHO 4 (5;5) (6;5) (6;6) (;)',
              'RMECHO 3 (5;5) (6;5) (6;6) (6;6)',
              'RMECHO 3 (5;5) (6;5)'
            ]
            expected = [
              '2', '5', '2.5',
              '1', '2', '60.0',
              '0', '7', '3.5',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testRmechoCommand(self):
        tosupport = [
          'LESSAREA 3 (0;0) (1;0) (0;1)'
        ]
        if self._isSupported(tosupport):
            dataset = [
              '3 (1;1) (2;2) (1;2)',
              '7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)'
            ]
            commands = [
              'LESSAREA 3 (1;1) (2;2) (1;2)',
              'LESSAREA 4 (1;1) (1;2) (2;2) (2;1)',
              'LESSAREA 7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;0)',
              'LESSAREA 7 (0;0) (0;4) (2;6) (4;6) (6;4) (6;2) (4;-1)',

              'LESSAREA 2 (5;5) (5;6)',
              'LESSAREA 4 (5;5) (6;5) (6;6) (;)',
              'LESSAREA 3 (5;5) (6;5) (6;6) (6;6)',
              'LESSAREA 3 (5;5) (6;5)'
            ]
            expected = [
              '0',
              '1',
              '1',
              '2',

              InvCmd(),
              InvCmd(),
              InvCmd(),
              InvCmd()
            ]
            return self._process(dataset, commands, expected)
        return self._process([''], tosupport, [InvCmd()])

    def testAtleastTwoOptionalCommandsSupported(self):
        tosupport = [
          'LESSAREA 3 (0;0) (1;0) (0;1)',
          'RMECHO 3 (0;0) (1;0) (0;1)',
          'ECHO 3 (0;0) (1;0) (0;1)',
          'MAXSEQ 3 (0;0) (1;0) (0;1)',
          'INTERSECTIONS 3 (0;0) (1;0) (0;1)',
          'SAME 3 (0;0) (1;0) (0;1)',
          'INFRAME 3 (0;0) (1;0) (0;1)',
          'RIGHTSHAPES',
          'RECTS',
          'PERMS 3 (2;0) (0;0) (0;2)'
        ]
        supported = 0
        for cmd in tosupport:
            if self._isSupported(cmd):
                supported = supported + 1
        result = self._process([''], [''], [''])
        result.succeeded = (supported >= 2)
        result.expected = 'Atleast 2 optional supported commands'
        return result

if __name__ == "__main__":
    main(LabT3(sys.argv[1]))
