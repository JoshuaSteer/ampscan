"""
Testing suite for trim module
"""
import unittest
import os


class TestTrim(unittest.TestCase):

    def setUp(self):
        """Runs before each unit test
        Sets up the AmpObject object using "sample_stl_sphere_BIN.stl"
        """
        from AmpScan.core import AmpObject
        stl_path = self.get_path("sample_stl_sphere_BIN.stl")
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

    @staticmethod
    def get_path(filename):
        """Returns the absolute path to a test file

        Parameters
        ----------
        filename : string
            Name of file in tests to get path to

        Returns
        -------
        stl_path : string
            The path to the file
        """

        # Check if the parent directory is tests (this is for Pycharm unittests)
        if os.path.basename(os.getcwd()) == "tests":
            # This is for Pycharm testing
            stl_path = filename
        else:
            # This is for the Gitlab testing
            stl_path = os.path.abspath(os.getcwd()) + "\\tests\\"+filename
        return stl_path
