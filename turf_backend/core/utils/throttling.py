from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class LoginThrottle(AnonRateThrottle):
    rate = '10/minute'

class SignupThrottle(AnonRateThrottle):
    rate = '20/hour'

class AuthUserLoginThrottle(UserRateThrottle):
    rate = '20/minute'
