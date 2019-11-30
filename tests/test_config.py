import os

from awscs import config

class TestConfig():
    def test_get_config(self, tmpdir):
        p = tmpdir.mkdir("sub").join(".config.json")
        data = '''
{
    "AWS_PROFILE": "test",
    "AWS_DEFAULT_REGION": "ap-northeast-1"
}
'''
        p.write(data)
        tmpdir.chdir()

        os.environ['AWSCSPATH'] = os.path.join(os.getcwd(), "sub", ".config.json")

        assert config.get_setting() == {'AWS_PROFILE': "test", 'AWS_DEFAULT_REGION': "ap-northeast-1"}

    def test_return_none_if_file_does_not_exist(self, tmpdir):
        tmpdir.mkdir("sub")
        tmpdir.chdir()

        os.environ['AWSCSPATH'] = os.path.join(os.getcwd(), "sub", ".config.json")

        assert config.get_setting() == None


    def test_set_config(self, tmpdir):
        tmpdir.mkdir("sub")
        tmpdir.chdir()

        os.environ['AWSCSPATH'] = os.path.join(os.getcwd(), "sub", ".config.json")

        config.set_setting('test', "hogehoge")

        assert config.get_setting() == {'AWS_PROFILE': "test", 'AWS_DEFAULT_REGION': "hogehoge"}
