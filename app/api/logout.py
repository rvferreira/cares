from lib.api import ApiFailure, ApiSuccess
from lib.error_codes import LOGOUT_FAILURE

def handler(request):
    try:
        del request.session["user_id"]
        del request.session["user_type"]

        return ApiSuccess()

    except KeyError:

        return ApiFailure(LOGOUT_FAILURE)