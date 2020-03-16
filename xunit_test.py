import unittest
import unittest.mock

from xunit import TestSuite, TestCase, TestResult, WasRun
from unittest.mock import MagicMock


class TestCaseTest(unittest.TestCase):

	def setUp(self):
		self.result = TestResult()
		
	def testTemplateMethod(self):
		test = WasRun('testMethod')
		test.run(self.result)
		assert('setup testMethod tearDown ' == test.log)

	def testResult(self):
		test = WasRun('testMethod')
		test.run(self.result)
		assert('1 run, 0 failed' == self.result.summary())

	def testFailedResultDuringSetup(self):
		test = TestCase('testMethod')
		test.setUp = MagicMock(side_effect=Exception())
		test.run(self.result)
		assert('setup failed' == self.result.summary())

	def testFailedResultAlwaysTeardown(self):
		test = WasRun('testBrokenMethod')
		test.run(self.result)
		assert('tearDown' in test.log)

	def testFailedResult(self):
		test = WasRun('testBrokenMethod')
		test.run(self.result)
		assert('1 run, 1 failed', self.result.summary)

	def testFailedResultFormatting(self):
		self.result.testStarted()
		self.result.testFailed()
		assert('1 run, 1 failed' == self.result.summary())

	def testSuite(self):
		suite = TestSuite()
		suite.add(WasRun('testMethod'))
		suite.add(WasRun('testBrokenMethod'))
		suite.run(self.result)
		assert('2 run, 1 failed' == self.result.summary())