import unittest

from project.test.moduleTest.module_test import ModuleTest


def moduleTestBuilder():
    testChainsBuilder = unittest.TestSuite()
    testsChainsObject = [ModuleTest("testMessage")]

    for obj in testsChainsObject:
        testChainsBuilder.addTest(obj)

    return testChainsBuilder
