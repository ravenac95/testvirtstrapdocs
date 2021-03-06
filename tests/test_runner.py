"""
Runner Tests
============

Very high level tests for the virtstrap runner
"""
import os
import sys
import fudge
from cStringIO import StringIO
from virtstrap.runner import VirtstrapRunner
from tests.tools import *
from nose.tools import raises

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../'))
PACKAGES_DIR = os.path.abspath(os.path.join(PROJECT_DIR,
                    'tests/fixture/packages'))

TEST_CONFIG = """
requirements:
  - test1
  - test5

--- # Development profile
profile: development

requirements:
  - test4

---
profile: production

requirements:
  - test6
"""

def test_initialize_runner():
    """Test that we can initialize the VirtstrapRunner"""
    runner = VirtstrapRunner()

class TestVirtstrapRunner(object):
    def setup(self):
        self.runner = VirtstrapRunner()

    def teardown(self):
        self.runner = None

    @fudge.patch('sys.stderr')
    def test_run_no_args(self, fake_sys_stderr):
        """Run the main command line utility with no args"""
        fake_sys_stderr.is_a_stub() # just want to silence stderr
        try:
            return_code = self.runner.main()
        except SystemExit, e:
            system_exit = True
            assert e.code == 2
        assert system_exit == True, "Runner didn't issue a system exit"

    def test_run_help(self):
        """Run the help command"""
        test_args = ['--help']
        system_exit = False
        try:
            code = self.runner.main(args=test_args)
        except SystemExit, e:
            system_exit = True
            assert e.code == 0
        assert system_exit == True, "Runner didn't issue a system exit"

    def test_run_init(self):
        """Run the init command"""
        test_args = ['init']
        with in_temp_directory() as temp_directory:
            return_code = self.runner.main(args=test_args)
            virtual_environment_path = os.path.join(temp_directory, '.vs.env')
            quick_activate_path = os.path.join(temp_directory, 'quickactivate.sh')
            assert os.path.exists(virtual_environment_path) == True
            assert os.path.exists(quick_activate_path) == True
            assert return_code == 0

    def test_run_init_to_different_directory(self):
        """Run the init command with a different virtstrap directory"""
        env_dir = 'envdir'
        test_args = ['init', '--virtstrap-dir=%s' % env_dir]
        with in_temp_directory() as temp_directory:
            return_code = self.runner.main(args=test_args)
            virtual_environment_path = os.path.join(temp_directory, env_dir)
            quick_activate_path = os.path.join(temp_directory, 'quickactivate.sh')
            assert os.path.exists(virtual_environment_path) == True
            assert os.path.exists(quick_activate_path) == True
            assert return_code == 0

    def test_run_init_with_a_config(self):
        """Run the init command with a VEfile in the directory"""
        test_args = ['init']
        with temp_pip_index(PACKAGES_DIR) as index_url:
            with in_temp_directory() as temp_directory:
                # Create temp config file
                vefile = open('VEfile', 'w')
                vefile.write(TEST_CONFIG)
                vefile.close()
                # If the config file was correctly written then 
                # it will install all the software
                return_code = self.runner.main(args=test_args)
                # Do a loose check of the requirements
                requirements = open('requirements.txt')
                requirements_string = requirements.read()
                expected_strings = ['test1', 'test5', 'test4']
                for package in expected_strings:
                    assert package in requirements_string
                assert return_code == 0

    def test_run_init_with_a_config_using_custom_config_file(self):
        """Run the init command with a custom file in the directory"""
        custom_config_file = 'testfile'
        test_args = ['init', '--config-file=%s' % custom_config_file]
        with temp_pip_index(PACKAGES_DIR) as index_url:
            with in_temp_directory() as temp_directory:
                # Create the custom config file
                vefile = open(custom_config_file, 'w')
                vefile.write(TEST_CONFIG)
                vefile.close()
                return_code = self.runner.main(args=test_args)
                # Do a loose check of the requirements
                requirements = open('requirements.txt')
                requirements_string = requirements.read()
                expected_strings = ['feedparser', 'werkzeug', 'requests', 
                        'brownie']
                expected_strings = ['test1', 'test5', 'test4']
                for package in expected_strings:
                    assert package in requirements_string
                assert return_code == 0

    def test_run_init_with_a_config_using_different_profile(self):
        """Run the init command using a different profile"""
        profiles = 'production'
        test_args = ['init', '--profiles=%s' % profiles]
        with temp_pip_index(PACKAGES_DIR) as index_url:
            with in_temp_directory() as temp_directory:
                vefile = open('VEfile', 'w')
                vefile.write(TEST_CONFIG)
                vefile.close()
                return_code = self.runner.main(args=test_args)
                # Do a loose check of the requirements
                requirements = open('requirements.txt')
                requirements_string = requirements.read()
                expected_strings = ['test1', 'test5', 'test6']
                for package in expected_strings:
                    assert package in requirements_string
                assert return_code == 0
