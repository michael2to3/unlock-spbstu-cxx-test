#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path

class LabT1(Lab):
    def __init__(self, student):
        super(LabT1, self).__init__(student, 'T1')

    def _OXY(self, v):
        return str(v)

    def _getRectangleDesc(self, x1, y1, x2, y2):
        return 'RECTANGLE ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + '\n'

    def _getSquareDesc(self, x1, y1, a):
        return 'SQUARE ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(a) + '\n'

    def _getParallDesc(self, x1, y1, x2, y2, x3, y3):
        return 'PARALLELOGRAM ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + ' ' + self._OXY(x3) + ' ' + self._OXY(y3) + '\n'

    def _getDiamondDesc(self, x1, y1, x2, y2, x3, y3):
        return 'DIAMOND ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + ' ' + self._OXY(x3) + ' ' + self._OXY(y3) + '\n'

    def _getTriangleDesc(self, x1, y1, x2, y2, x3, y3):
        return 'TRIANGLE ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + ' ' + self._OXY(x3) + ' ' + self._OXY(y3) + '\n'

    def _getRegularDesc(self, x1, y1, x2, y2, x3, y3):
        return 'REGULAR ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + ' ' + self._OXY(x3) + ' ' + self._OXY(y3) + '\n'

    def _getPolygonDesc(self, coords):
        returnable = 'POLYGON'
        for coord in coords:
            returnable = returnable + ' ' + self._OXY(coord)
        return returnable + '\n'

    def _getConcaveDesc(self, x1, y1, x2, y2, x3, y3, x4, y4):
        return 'CONCAVE ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + ' ' + self._OXY(x3) + ' ' + self._OXY(y3) + ' ' + self._OXY(x4) + ' ' + self._OXY(y4) + '\n'

    def _getComplexquadDesc(self, x1, y1, x2, y2, x3, y3, x4, y4):
        return 'COMPLEXQUAD ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(x2) + ' ' + self._OXY(y2) + ' ' + self._OXY(x3) + ' ' + self._OXY(y3) + ' ' + self._OXY(x4) + ' ' + self._OXY(y4) + '\n'

    def _getCircleDesc(self, x1, y1, r):
        return 'CIRCLE ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(r) + '\n'

    def _getEllipseDesc(self, x1, y1, r1, r2):
        return 'ELLIPSE ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(r1) + ' ' + self._OXY(r2) + '\n'

    def _getRingDesc(self, x1, y1, r1, r2):
        return 'RING ' + self._OXY(x1) + ' ' + self._OXY(y1) + ' ' + self._OXY(r1) + ' ' + self._OXY(r2) + '\n'

    def _getScaleDesc(self, x, y, k):
        return 'SCALE ' + str(x) + ' ' + str(y) + ' ' + str(k) + '\n'

    def _getExpected(self, input, output):
        return output #'With input:\n' + input + 'Expected output:\n' + output

    def _getExpectedWithError(self, input, output):
        return self._getExpected(input = input, output = output) + 'And also zero exit code but with error message in standard error'

    def _tapTabs(self, descs):
        returnable = ''
        for desc in descs:
            returnable = returnable + '\t' + desc
        return returnable

    def testEmptyLinesSkip(self):
        rectangleDesc = self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0)
        scaleDesc = self._getScaleDesc(0.0, 0.0, 2.0)

        input = '\n' + rectangleDesc + '\n' + scaleDesc
        outputBefore = '4.0 -1.0 -1.0 1.0 1.0\n'
        outputAfter = '16.0 -2.0 -2.0 2.0 2.0\n'
        outputResult = outputBefore + outputAfter

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == outputResult)
        result.expected = self._getExpected(input = self._tapTabs([rectangleDesc, scaleDesc]), output = self._tapTabs([outputBefore, outputAfter]))
        return result

    def testNothingToScale(self):
        scaleDesc = self._getScaleDesc(0.0, 0.0, 2.0)

        input = scaleDesc

        result = self.execute(input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testNoScaleCommand(self):
        rectangleDesc = self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0)

        input = rectangleDesc

        result = self.execute(input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testNegativeCoeffScale(self):
        rectangleDesc = self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0)
        scaleDesc = self._getScaleDesc(0.0, 0.0, -2.0)

        input = rectangleDesc + scaleDesc

        result = self.execute(input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def _isShapeImplemented(self, testableShapeDesc):
        rectangleDesc = self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0)
        scaleDesc = self._getScaleDesc(0.0, 0.0, 2.0)
        input = rectangleDesc + testableShapeDesc + scaleDesc
        result = self.execute(input = input)
        outputByLine = result.output.split('\n')
        firstLine = outputByLine[0]
        areaString = firstLine.split(' ')[0]
        area = 0.0
        try:
            area = float(areaString)
        except:
            area = 0.0
        isImplemented = (area != 0.0) and (area > 4.0)
        return isImplemented

    def testAtleastThreeShapesImplemented(self):
        rectangleDesc = self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0)
        squareDesc = self._getSquareDesc(-1.0, -1.0, 2.0)
        parallDesc = self._getParallDesc(-1.0, -1.0, 1.0, 1.0, -1.0, 1.0)
        diamondDesc = self._getDiamondDesc(-1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        triangleDesc = self._getTriangleDesc(-1.0, -1.0, 1.0, 1.0, -1.0, 1.0)
        regularDesc = self._getRegularDesc(0.0, 0.0, -1.0, 0.0, -1.0, 1.0)
        polygonDesc = self._getPolygonDesc([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0])
        concaveDesc = self._getConcaveDesc(-1.0, -1.0, 1.0, -1.0, 0.0, 1.0, 0.0, 0.0)
        complexquadDesc = self._getComplexquadDesc(-1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0)
        circleDesc = self._getCircleDesc(0.0, 0.0, 1.0)
        ringDesc = self._getRingDesc(0.0, 0.0, 1.0, 0.5)
        ellipseDesc = self._getEllipseDesc(0.0, 0.0, 1.0, 1.0)

        scaleDesc = self._getScaleDesc(0.0, 0.0, 2.0)

        notRectangleDescs = [squareDesc, parallDesc, diamondDesc, triangleDesc, regularDesc, polygonDesc, concaveDesc, complexquadDesc, circleDesc, ringDesc, ellipseDesc]
        implementedShapes = 1
        for desc in notRectangleDescs:
            if self._isShapeImplemented(desc):
                implementedShapes = implementedShapes + 1

        input = rectangleDesc
        for desc in notRectangleDescs:
            input = input + desc
        input = input + scaleDesc
        result = self.execute(input = input)
        result.succeeded = implementedShapes >= 3
        result.expected = 'Rectangle and atleast two additional shapes must be implemented'
        return result

    def testBadRectangleScale(self):
        descs = [
          self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0),
          self._getRectangleDesc(1.0, 1.0, -1.0, -1.0),
          self._getScaleDesc(0.0, 0.0, 2.0)
        ]

        input = "".join(descs)
        outputBefore = '4.0 -1.0 -1.0 1.0 1.0\n'
        outputAfter = '16.0 -2.0 -2.0 2.0 2.0\n'
        outputResult = outputBefore + outputAfter

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)
        result.expected = self._getExpectedWithError(input = self._tapTabs(descs), output = self._tapTabs([outputBefore, outputAfter]))
        return result

    def testCenteredRectangleScale(self):
        descs = [
          self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0),
          self._getScaleDesc(0.0, 0.0, 2.0)
        ]

        input = "".join(descs)
        outputBefore = '4.0 -1.0 -1.0 1.0 1.0\n'
        outputAfter = '16.0 -2.0 -2.0 2.0 2.0\n'
        outputResult = outputBefore + outputAfter

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == outputResult)
        result.expected = self._getExpected(input = self._tapTabs(descs), output = self._tapTabs([outputBefore, outputAfter]))
        return result

    def testBorderedRectangleScale(self):
        descs = [
          self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0),
          self._getScaleDesc(-1.0, -1.0, 2.0)
        ]

        input = "".join(descs)
        outputBefore = '4.0 -1.0 -1.0 1.0 1.0\n'
        outputAfter = '16.0 -1.0 -1.0 3.0 3.0\n'
        outputResult = outputBefore + outputAfter

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == outputResult)
        result.expected = self._getExpected(input = self._tapTabs(descs), output = self._tapTabs([outputBefore, outputAfter]))
        return result

    def testPointedRectangleScale(self):
        descs = [
          self._getRectangleDesc(-1.0, -1.0, 1.0, 1.0),
          self._getRectangleDesc(-0.123456789, -0.123456789, 1.876543211, 3.876543211),
          self._getScaleDesc(-2.0, -2.0, 2.0)
        ]

        input = "".join(descs)
        outputBefore = '12.0 -1.0 -1.0 1.0 1.0 -0.1 -0.1 1.9 3.9\n'
        outputAfter =  '48.0 0.0 0.0 4.0 4.0 1.8 1.8 5.8 9.8\n'
        outputResult = outputBefore + outputAfter

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == outputResult)
        result.expected = self._getExpected(input = self._tapTabs(descs), output = self._tapTabs([outputBefore, outputAfter]))
        return result

    def testSquareScaleIfSquareIsImplemented(self):
        descs = [
          self._getSquareDesc(-1.0, -1.0, 2.0),
          self._getSquareDesc(-1.0, -0.5, 3.0),

          self._getSquareDesc(0.0, 0.0, -2.0),
          self._getSquareDesc(0.0, 0.0, 0.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '13.0 -1.0 -1.0 1.0 1.0 -1.0 -0.5 2.0 2.5\n'
            outputAfter =  '52.0 -2.0 -2.0 2.0 2.0 -2.0 -1.0 4.0 5.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testCircleScaleIfCircleIsImplemented(self):
        descs = [
          self._getCircleDesc(0.0, 0.0, 1.0),
          self._getCircleDesc(0.5, 1.0, 2.0),

          self._getCircleDesc(0.0, 0.0, -2.0),
          self._getCircleDesc(0.0, 0.0, 0.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '15.7 -1.0 -1.0 1.0 1.0 -1.5 -1.0 2.5 3.0\n'
            outputAfter =  '62.8 -2.0 -2.0 2.0 2.0 -3.0 -2.0 5.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testEllipseScaleIfEllipseIsImplemented(self):
        descs = [
          self._getEllipseDesc(0.0, 0.0, 1.0, 2.0),
          self._getEllipseDesc(0.5, 1.0, 2.0, 1.0),

          self._getEllipseDesc(0.0, 0.0, -1.0, 1.0),
          self._getEllipseDesc(0.0, 0.0, 0.0, 1.0),
          self._getEllipseDesc(0.0, 0.0, 1.0, 0.0),
          self._getEllipseDesc(0.0, 0.0, 1.0, -1.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '12.6 -2.0 -1.0 2.0 1.0 -0.5 -1.0 1.5 3.0\n'
            outputAfter =  '50.3 -4.0 -2.0 4.0 2.0 -1.0 -2.0 3.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testRingScaleIfRingIsImplemented(self):
        descs = [
          self._getRingDesc(0.0, 0.0, 2.0, 1.0),
          self._getRingDesc(0.5, 1.0, 2.0, 1.0),

          self._getRingDesc(0.0, 0.0, 1.0, 2.0),
          self._getRingDesc(0.0, 0.0, -1.0, 1.0),
          self._getRingDesc(0.0, 0.0, 0.0, 1.0),
          self._getRingDesc(0.0, 0.0, 1.0, 0.0),
          self._getRingDesc(0.0, 0.0, 1.0, -1.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '18.8 -2.0 -2.0 2.0 2.0 -1.5 -1.0 2.5 3.0\n'
            outputAfter = '75.4 -4.0 -4.0 4.0 4.0 -3.0 -2.0 5.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testDiamondScaleIfDiamondIsImplemented(self):
        descs = [
          self._getDiamondDesc(0.0, 0.0, 0.0, 1.0, -2.0, 0.0),
          self._getDiamondDesc(0.5, 3.0, -0.5, 1.0, 0.5, 1.0),

          self._getDiamondDesc(0.0, 0.0, 1.0, 1.0, 1.0, -1.0),
          self._getDiamondDesc(0.0, 0.0, 1.0, 1.0, 1.0, -2.0),
          self._getDiamondDesc(0.0, 0.0, 2.0, 2.0, 1.0, 1.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '8.0 -2.0 -1.0 2.0 1.0 -0.5 -1.0 1.5 3.0\n'
            outputAfter = '32.0 -4.0 -2.0 4.0 2.0 -1.0 -2.0 3.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testComplexquadScaleIfComplexquadIsImplemented(self):
        descs = [
          self._getComplexquadDesc(-1.0, -2.0, 1.0, 2.0, 1.0, -1.0, -2.0, 2.0),
          self._getComplexquadDesc(-0.5, -1.0, 1.5, 3.0, -1.5, 3.0, 1.5, 0.0),

          self._getComplexquadDesc(0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.0),
          self._getComplexquadDesc(0.0, 0.0, 2.0, 2.0, 1.0, 1.0, 2.0, 0.0),
          self._getComplexquadDesc(0.0, 0.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '9.0 -2.0 -2.0 1.0 2.0 -1.5 -1.0 1.5 3.0\n'
            outputAfter = '36.0 -4.0 -4.0 2.0 4.0 -3.0 -2.0 3.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testTriangleScaleIfTriangleIsImplemented(self):
        descs = [
          self._getTriangleDesc(-1.0, -1.0, 0.0, 2.0, 1.0, -1.0),
          self._getTriangleDesc(-0.5, -1.0, -0.5, 2.0, 1.5, 2.0),

          self._getTriangleDesc(0.0, 0.0, 1.0, 1.0, 0.0, 0.0),
          self._getTriangleDesc(0.0, 0.0, 2.0, 2.0, 1.0, 1.0),
          self._getTriangleDesc(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '6.0 -1.0 -1.0 1.0 2.0 -0.5 -1.0 1.5 2.0\n'
            outputAfter = '24.0 -2.0 -2.0 2.0 4.0 -1.0 -2.0 3.0 4.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testConcaveScaleIfConcaveIsImplemented(self):
        descs = [
          self._getConcaveDesc(-1.0, -1.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0),
          self._getConcaveDesc(-0.5, -1.0, 2.5, 1.0, 0.5, 3.0, 0.5, 1.0),

          self._getConcaveDesc(0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0),
          self._getConcaveDesc(0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, -1.0),
          self._getConcaveDesc(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '5.0 -1.0 -1.0 2.0 2.0 -0.5 -1.0 2.5 3.0\n'
            outputAfter = '20.0 -2.0 -2.0 4.0 4.0 -1.0 -2.0 5.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testParallelogramScaleIfParallelogramIsImplemented(self):
        descs = [
          self._getParallDesc(-2.0, -1.0, -1.0, 1.0, 2.0, 1.0),
          self._getParallDesc(4.5, 3.0, 0.5, 3.0, -3.5, -1.0),

          self._getParallDesc(2.0, 1.0, -2.0, -1.0, -1.0, 0.0),
          self._getParallDesc(-1.0, -1.0, -1.0, 1.0, 1.0, 2.0),
          self._getParallDesc(-1.0, -1.0, 0.0, 1.0, 0.0, 0.0),
          self._getParallDesc(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '22.0 -2.0 -1.0 2.0 1.0 -3.5 -1.0 4.5 3.0\n'
            outputAfter =  '88.0 -4.0 -2.0 4.0 2.0 -7.0 -2.0 9.0 6.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testPolygonScaleIfPolygonIsImplemented(self):
        descs = [
          self._getPolygonDesc([-1.0, -1.0, -2.0, 0.0, -1.0, 1.0, 1.0, 1.0, 2.0, 0.0, 1.0, -1.0]),
          self._getPolygonDesc([0.5, -1.0, -0.5, 0.0, -0.5, 2.0, 0.5, 3.0, 1.5, 2.0, 1.5, 0.0]),
          self._getPolygonDesc([0.0, -2.0, -3.0, -2.0, -3.0, 1.0, -2.0, 3.0, 1.0, 4.0, 4.0, 4.0, 4.0, 1.0, 3.0, -1.0]),

          self._getPolygonDesc([0.0, 0.0, 1.0, 1.0]),
          self._getPolygonDesc([0.0, 0.0, 1.0, 1.0, 1.0, 1.0]),
          self._getPolygonDesc([0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0]),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '47.0 -2.0 -1.0 2.0 1.0 -0.5 -1.0 1.5 3.0 -3.0 -2.0 4.0 4.0\n'
            outputAfter = '188.0 -4.0 -2.0 4.0 2.0 -1.0 -2.0 3.0 6.0 -6.0 -4.0 8.0 8.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

    def testRegularScaleIfRegularIsImplemented(self):
        descs = [
          self._getRegularDesc(0.0, 0.0, 1.0, 0.0, 1.0, 1.0),
          self._getRegularDesc(0.5, 1.0, 0.5, 3.0, -1.5, 3.0),
          self._getRegularDesc(0.0, 0.0, 1.0, 1.0, 2.0, 0.0),

          self._getRegularDesc(0.5, 1.0, 0.5, 4.0, -0.5, 4.0),

          self._getScaleDesc(0.0, 0.0, 2.0)
        ]
        if self._isShapeImplemented(descs[0]):
            input = "".join(descs)
            outputBefore = '28.0 -1.0 -1.0 1.0 1.0 -1.5 -1.0 2.5 3.0 -2.0 -2.0 2.0 2.0\n'
            outputAfter = '112.0 -2.0 -2.0 2.0 2.0 -3.0 -2.0 5.0 6.0 -4.0 -4.0 4.0 4.0\n'
            outputResult = outputBefore + outputAfter

            result = self.execute(input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == outputResult) and (len(result.error) != 0)

            inputForExpected = self._tapTabs(descs)
            outputForExpected = self._tapTabs([outputBefore, outputAfter])
            result.expected = self._getExpectedWithError(input = inputForExpected, output = outputForExpected)
            return result
        else:
            result = self.execute(input = '')
            result.succeeded = True
            return result

        def testClassDesign(self):
            extraPaths = []
            if os.path.exists(self.student + "/common"):
                extraPaths.append("-I" + self.student + "/common")
                if os.path.exists(self.student + "/common/include"):
                    extraPaths.append("-I" + self.student + "/common/include")
            result = self._invokeExternal("c++", ["-std=c++14", "-c", "-o", "/dev/null",
                                          "-Wall", "-Wextra", "-Werror",
                                          "-Wno-missing-field-initializers",
                                          "-Wold-style-cast"] + extraPaths + \
                                         ["-I" + self.student + "/" + self.lab,
                                          "-DNAMESPACE=" + self._getStudentLastName(),
                                          self._getTemplateFile(".cpp")])
            result.succeeded = (result.exitCode == 0) and (len(result.error) == 0)
            return result

if __name__ == "__main__":
    main(LabT1(sys.argv[1]))
