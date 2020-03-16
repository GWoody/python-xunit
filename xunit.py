class TestSuite:
	def __init__(self):
	 self.tests = []

	def add(self, test):
		self.tests.append(test)
	
	def run(self, result):
		for test in self.tests:
			test.run(result)

class TestCase: 
	def __init__(self, name):
		self.name = name

	def setUp(self):
		self.wasRun = None
		self.wasSetup = 1

	def run(self, result):
		result.testStarted()
		try:
			self.setUp()
		except:
			return result.setupCheck()
		try:
			method = getattr(self,self.name)
			method()
		except:
			return result.testFailed()
		finally:
			self.tearDown()

	def tearDown(self):
		self.wasTornDown = 1

class WasRun(TestCase): 
	def __init__(self, name):
		TestCase.__init__(self,name)

	def setUp(self):
		self.log = 'setup '
	
	def testMethod(self): 
		self.log = self.log + 'testMethod '

	def tearDown(self):
		self.log = self.log + 'tearDown '

	def testBrokenMethod(self):
		raise Exception

class TestResult:
	def __init__(self):
		self.setupFailed = False
		self.teardownSuccess = False
		self.runCount = 0
		self.errorCount = 0

	def testStarted(self):
		self.runCount = self.runCount + 1

	def testFailed(self):
		self.errorCount = self.errorCount + 1

	def setupCheck(self):
		self.setupFailed = True

	def summary(self): 
		if self.setupFailed: return 'setup failed'
		return '%d run, %d failed' % (self.runCount, self.errorCount)