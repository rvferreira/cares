from django.http.response import JsonResponse
from error_codes import *

def ApiFailure(error):
    error_strings = {
        INVALID_CREDENTIALS: "Invalid credentials.",
        MALFORMED_REQUEST: "Malformed request.",
        LOGOUT_FAILURE: "Logout failed.",
        SIGNUP_FAILURE: "Sorry, your account creation has failed.",
        USER_COLISION: "This e-mail is already in use by another account. Use the password reset."
    }
    data = {}
    data['code'] = error
    data['message'] = error_strings[error]

    return JsonResponse(data)

def ApiSuccess():
    data = {}
    data['code'] = 0
    data['message'] = 'Ok.'

    return JsonResponse(data)