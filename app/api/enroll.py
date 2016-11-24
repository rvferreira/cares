from lib.api import ApiSuccess, ApiFailure
from lib.error_codes import *
from app.models import User, Career, Enrollment
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handler(request):
    try:
        career = request.POST.get('career')
        if (not career):
            raise Exception
    except:
        return ApiFailure(MALFORMED_REQUEST)

    try:
        user_id = request.session['user']['id']

        if (not user_id):
            raise Exception
    except:
        return ApiFailure(NEED_LOGIN)

    try:
        user = User.objects.get(id=user_id)
        career = Career.objects.get(id=career)

    except:
        return ApiFailure(BAD_PARAMS)

    try:
        if (user.user_type == 1):
            raise Exception
    except:
        return ApiFailure(NOT_A_STUDENT)

    try:
        e = Enrollment.objects.get(student=user, career=career)
    except:

        try:
            e = Enrollment(
                student=user,
                career=career,
            )

            e.save()

        except:
            return ApiFailure(ENROLL_FAILURE)


        return ApiSuccess()

    return ApiFailure(ALREADY_ENROLLED)
