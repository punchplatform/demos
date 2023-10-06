import unittest

from project.test.moduleTest import moduleTestBuilder

runner = unittest.TextTestRunner()
moduleTest = [moduleTestBuilder()]

for obj in moduleTest:
    runner.run(obj)
