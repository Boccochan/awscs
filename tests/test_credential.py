import os
import pytest

from awscs import credential
from awscs import exception

class TestLoadCredential():
    def test_exception_if_credential_file_does_not_exist(self, tmpdir):
        tmpdir.mkdir("sub")
        tmpdir.chdir()

        with pytest.raises(exception.NotFoundFile):
            credential.load(os.path.join(os.getcwd(), '.credential'))

    def test_return_list_if_crednetial_file_is_correct(self, tmpdir):
        p = tmpdir.join(".credential")
        tmpdir.chdir()
        profiles = '''
[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        assert credential.load(os.path.join(os.getcwd(), '.credential')) ==  ['test', 'hoge']

    def test_return_list_if_crednetial_file_is_correct_1(self, tmpdir):
        p = tmpdir.join(".credential")
        tmpdir.chdir()
        profiles = '''
    [aaa]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        assert credential.load(os.path.join(os.getcwd(), '.credential')) ==  ['aaa', 'test', 'hoge']

    def test_return_list_if_crednetial_file_is_correct_2(self, tmpdir):
        p = tmpdir.join(".credential")
        tmpdir.chdir()
        profiles = '''
    [aaa]b
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        assert credential.load(os.path.join(os.getcwd(), '.credential')) ==  ['test', 'hoge']

    def test_return_list_if_crednetial_file_is_correct_3(self, tmpdir):
        p = tmpdir.join(".credential")
        tmpdir.chdir()
        profiles = '''
    [ ]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        assert credential.load(os.path.join(os.getcwd(), '.credential')) ==  [' ', 'test', 'hoge']

    def test_return_list_if_crednetial_file_is_correct_4(self, tmpdir):
        p = tmpdir.join(".credential")
        tmpdir.chdir()
        profiles = '''
    ][ddd
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        assert credential.load(os.path.join(os.getcwd(), '.credential')) ==  ['test', 'hoge']

    def test_exception_default_tag_found(self, tmpdir):
        p = tmpdir.join("credential")
        tmpdir.chdir()

        profiles = '''[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[default]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        with pytest.raises(exception.FoundDefault):
            credential.load(os.path.join(os.getcwd(), 'credential'))

    def test_exception_not_found_tag(self, tmpdir):
        p = tmpdir.join("credential")
        tmpdir.chdir()

        profiles = ''
        p.write(profiles)

        with pytest.raises(exception.NotFoundTag):
            credential.load(os.path.join(os.getcwd(), 'credential'))


class TestSetDefault():
    def test_set_default(self, tmpdir):
        p = tmpdir.join(".credential")
        tmpdir.chdir()
        profiles = '''[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        os.environ['AWSCS_TEMPLATE_CREDENTIALS'] = os.path.join(os.getcwd(), '.credential')
        os.environ['AWSCS_PROFILE_PATH'] = os.path.join(os.getcwd(), 'credential')

        credential.set_default('hoge')

        expected = '''[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[default]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        with open(os.environ['AWSCS_PROFILE_PATH'], 'r') as f:
            result = ''.join(f.readlines())
            assert result == expected


class TestCopy():
    def test_copy_credential(self, tmpdir):
        p = tmpdir.join("credential")
        tmpdir.chdir()

        profiles = '''[test]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
[hoge]
aws_access_key_id=DKIAIOSFODNN7EXAMPLG
aws_secret_access_key=dJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
'''
        p.write(profiles)
        tmpdir.chdir()

        os.environ['AWSCS_TEMPLATE_CREDENTIALS'] = os.path.join(os.getcwd(), '.credential')
        os.environ['AWSCS_PROFILE_PATH'] = os.path.join(os.getcwd(), 'credential')

        credential.copy()

        with open(os.environ['AWSCS_PROFILE_PATH'], 'r') as f:
            result = ''.join(f.readlines())
            assert result == profiles

    def test_exception_credential_does_not_found(self, tmpdir):
        tmpdir.chdir()

        os.environ['AWSCS_TEMPLATE_CREDENTIALS'] = os.path.join(os.getcwd(), '.credential')
        os.environ['AWSCS_PROFILE_PATH'] = os.path.join(os.getcwd(), 'credential')

        with pytest.raises(exception.NotFoundFile):
            credential.copy()
