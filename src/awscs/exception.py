class AwscsException(Exception):
    ''' This is the base exception class for awscs'''


class WrongIndex(AwscsException):
    ''' User inputs wrong index '''


class NotFoundFile(AwscsException):
    ''' Not found file '''


class FoundDefault(AwscsException):
    ''' Found default tag on credential '''


class NotFoundTag(AwscsException):
    ''' Found default tag on credential '''


class WrongInput(AwscsException):
    ''' User input wrong data '''