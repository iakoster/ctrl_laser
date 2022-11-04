import unittest
from pathlib import Path


__all__ = [
    "dev_tests_suite"
]


_tests_loader = unittest.TestLoader()
dev_tests_suite = unittest.TestSuite()
dev_tests_suite.addTests(_tests_loader.discover(r".\tests\dev_tests", top_level_dir='.'))