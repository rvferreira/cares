from django.http.response import JsonResponse
from error_codes import *

def ApiFailure(error):
    error_strings = {
        INVALID_CREDENTIALS:    "Invalid credentials.",
        MALFORMED_REQUEST:      "Malformed request.",
        LOGOUT_FAILURE:         "Logout failed.",
        SIGNUP_FAILURE:         "Sorry, your account creation has failed.",
        USER_COLISION:          "This e-mail is already in use by another account. Use the password reset.",
        NEED_LOGIN:             "You need to login to perform this operation.",
        BAD_PARAMS:             "Bad parameters.",
        ENROLL_FAILURE:         "Sorry, your enrollment has failed.",
        ALREADY_ENROLLED:       "User is already enrolled in this career.",
        NOT_A_STUDENT:          "User is not a student.",
        NOT_A_PROFESSOR:        "User is not a professor.",
    }

    data = {}
    data['code'] = error
    data['message'] = error_strings[error]

    return JsonResponse(data)

def ApiSuccess(result=""):
    data = {}
    data['code'] = 0
    data['message'] = 'Ok.'
    if (result):
        data['result'] = result

    return JsonResponse(data)