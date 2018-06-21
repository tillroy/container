class ContainerException(Exception):
    def __init__(self, message):
        super(ContainerException, self).__init__(message)


class IntError(ContainerException):
    def __init__(self, message):
        super(IntError, self).__init__(message)


class FloatError(ContainerException):
    def __init__(self, message):
        super(FloatError, self).__init__(message)


class ForbiddenValue(ContainerException):
    def __init__(self, message):
        super(ForbiddenValue, self).__init__(message)


class WrongFieldType(ContainerException):
    def __init__(self, message):
        super(WrongFieldType, self).__init__(message)


class RequiredField(ContainerException):
    def __init__(self, message):
        super(RequiredField, self).__init__(message)


class NotSupportedField(ContainerException):
    def __init__(self, message):
        super(NotSupportedField, self).__init__(message)