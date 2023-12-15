import unittest
from test_util import init_test
import bibtex_creator

class BibtexCreatorTest(unittest.TestCase):
	def setUp(self):
		self.app, self.db = init_test()
