from lib.api import ApiFailure, ApiSuccess
from lib.error_codes import *
from app.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handler(request):
    try:
        name = request.POST.get('name')
        email= request.POST.get('email')
        password= request.POST.get('password')
        level_of_education= request.POST.get('level_of_education')
        user_type= request.POST.get('user_type')
        date_of_birth= request.POST.get('date_of_birth')

        if (not email) or (not password) or (not user_type):
            raise Exception

    except:
        return ApiFailure(MALFORMED_REQUEST)

    try:
        u = User.objects.get(email=email)
    except:
        try:
            u = User(
                name=name,
                email=email,
                password=password,
                level_of_education=level_of_education,
                user_type=user_type,
                date_of_birth=date_of_birth,
            )

            u.save()

        except:
            return ApiFailure(SIGNUP_FAILURE)

        return ApiSuccess()

    return ApiFailure(USER_COLISION)