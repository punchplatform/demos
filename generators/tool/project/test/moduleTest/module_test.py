import unittest


class ModuleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.message = "This is a test"

    def testMessage(self):
        self.assertEqual(self.message, "This is a test")
