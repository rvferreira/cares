from lib.api import ApiFailure, ApiSuccess
from lib.error_codes import *
from app.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handler(request):

    try:
        email = request.POST.get('email')
        password = request.POST.get('password')

        if (not email) or (not password):
            raise Exception

    except Exception:
        return ApiFailure(MALFORMED_REQUEST)

    try:
        user = User.objects.get(email=email, password=password)

        cookie_info = {
            'id': user.id,
            'user_type': user.user_type
        }

        request.session['user'] = cookie_info

        return ApiSuccess()

    except Exception:
        return ApiFailure(INVALID_CREDENTIALS)