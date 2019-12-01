import os

from awscs import profile


class TestGetProfile():
    def test_get_profiles(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        profiles = '''
[test]
'''
        p.write(profiles)
        tmpdir.chdir()

        assert profile.get_profiles(os.path.join('sub', 'credentials')) == ['test']

    def test_get_profiles_1(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        profiles = '''
[test]
[hoge]
'''
        p.write(profiles)
        tmpdir.chdir()

        assert profile.get_profiles(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_profiles_2(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        profiles = '''
][
[test]
[hoge]
'''
        p.write(profiles)
        tmpdir.chdir()

        assert profile.get_profiles(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_profiles_3(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        profiles = '''
[test]
    [hoge]
'''
        p.write(profiles)
        tmpdir.chdir()

        assert profile.get_profiles(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_profiles_4(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        profiles = '''
[test]
    [hoge]
    [ad]b
'''
        p.write(profiles)
        tmpdir.chdir()

        assert profile.get_profiles(os.path.join('sub', 'credentials')) == ['test', 'hoge']

    def test_get_profiles_5(self, tmpdir):
        p = tmpdir.mkdir("sub").join("credentials")
        profiles = '''
[]
'''
        p.write(profiles)
        tmpdir.chdir()

        assert profile.get_profiles(os.path.join('sub', 'credentials')) == []
