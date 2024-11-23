class NoCityFoundException(Exception):
    def __init__(self, message="No city found."):
        self.message = message
        super().__init__(self.message)


class InvalidEmailException(Exception):
    def __init__(self, message="The email is not valid."):
        self.message = message
        super().__init__(self.message)

class EmailNotFoundException(Exception):
    def __init__(self, message="The email was not found."):
        self.message = message
        super().__init__(self.message)


class TooManyActiveDiscountsException(Exception):
    def __init__(self, message="The number of active discounts exceeds the threshold."):
        self.message = message
        super().__init__(self.message)

class UserIdNotFoundException(Exception):
    def __init__(self, message="User id not found."):
        self.message = message
        super().__init__(self.message)

class InvalidUniDomain(Exception):
    def __init__(self, message="University domain not valid."):
        self.message = message
        super().__init__(self.message)

class NotAcceptedPolcy(Exception):
    def __init__(self, message="Policy and TOS not accepted."):
        self.message = message
        super().__init__(self.message)

class UniDomainAlreadyExistsException(Exception):
    def __init__(self, message="University domain already registered."):
        self.message = message
        super().__init__(self.message)

class FieldNotFoundException(Exception):
    def __init__(self, message="Some fields were not found."):
        self.message = message
        super().__init__(self.message)


class ExpiredTokenException(Exception):
    def __init__(self, message="Token is expired."):
        self.message = message
        super().__init__(self.message)


class InvalidCountryException(Exception):
    def __init__(self, message="Invalid country."):
        self.message = message
        super().__init__(self.message)

class InvalidUniDomainException(Exception):
    def __init__(self, message="Invalid university domain."):
        self.message = message
        super().__init__(self.message)

        
class InvalidIdException(Exception):
    def __init__(self, message="Invalid identifier."):
        self.message = message
        super().__init__(self.message)


class MemorandumUuidNotFoundException(Exception):
    def __init__(self, message="Memorandum uuid not found."):
        self.message = message
        super().__init__(self.message)


class MemorandumAlreadyConfirmedException(Exception):
    def __init__(self, message="Memorandum is already confirmed."):
        self.message = message
        super().__init__(self.message)

class OtpVerificationFailedException(Exception):
    def __init__(self, message="Otp verification went wrong! Try again"):
        self.message = message
        super().__init__(self.message)

class ExpiredOtpException(Exception):
    def __init__(self, message="Otp expired: 10 minutes passed!"):
        self.message = message
        super().__init__(self.message)