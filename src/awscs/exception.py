class AwscsException(Exception):
    ''' This is the base exception class for awscs'''


class WrongIndex(AwscsException):
    ''' User inputs wrong index '''
