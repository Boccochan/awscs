import os

from awscs import handler


class TestGetCredentials():
    def test_get_credentials(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        credentials = '''
[test]
'''
        p.write(credentials)
        tmpdir.chdir()

        assert handler.get_credentials(os.path.join('sub', 'credentials')) == ['test']

    def test_get_credentials_1(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        credentials = '''
[test]
[hoge]
'''
        p.write(credentials)
        tmpdir.chdir()

        assert handler.get_credentials(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_credentials_2(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        credentials = '''
][
[test]
[hoge]
'''
        p.write(credentials)
        tmpdir.chdir()

        assert handler.get_credentials(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_credentials_3(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        credentials = '''
[test]
    [hoge]
'''
        p.write(credentials)
        tmpdir.chdir()

        assert handler.get_credentials(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_credentials_4(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        credentials = '''
[test]
    [hoge]
    [ad]b
'''
        p.write(credentials)
        tmpdir.chdir()

        assert handler.get_credentials(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_credentials_5(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        credentials = '''
[]
'''
        p.write(credentials)
        tmpdir.chdir()

        assert handler.get_credentials(os.path.join('sub', 'credentials')) == []
