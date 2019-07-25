"""
Testing suite for trim module
"""
import unittest
from util import get_path


class TestTrim(unittest.TestCase):

    def setUp(self):
        """Runs before each unit test
        Sets up the AmpObject object using "stl_file.stl"
        """
        from AmpScan.core import AmpObject
        stl_path = get_path("stl_file.stl")
        self.amp = AmpObject(stl_path)

    def test_trim(self):
        """Tests the trim method of AmpObject"""

        # Testing that the method runs
        self.amp.planarTrim(0.6, plane=2)

        # Testing invalid data types raise TypeErrors
        with self.assertRaises(TypeError):
            self.amp.planarTrim(0.6, plane=[])
        with self.assertRaises(TypeError):
            self.amp.planarTrim(0.6, plane=0.9)
        with self.assertRaises(TypeError):
            self.amp.planarTrim([], plane=[])
