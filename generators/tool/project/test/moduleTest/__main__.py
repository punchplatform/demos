import unittest

from project.test.moduleTest import moduleTestBuilder

runner = unittest.TextTestRunner()
runner.run(moduleTestBuilder())
