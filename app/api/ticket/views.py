from lib.api import ApiSuccess, ApiFailure
from lib.error_codes import *
from app.models import TicketInsideSprint, User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def forward(request):
    try:
        user_id = request.session['user']['id']

        if (not user_id):
            raise Exception
    except:
        return ApiFailure(NEED_LOGIN)


    try:
        user = User.objects.get(id=user_id)
        tis_id = request.POST.get('tis_id')
        tis = TicketInsideSprint.objects.get(id=tis_id)

    except:
        return ApiFailure(BAD_PARAMS)

    try:
        if tis.progress < 4:
            tis.progress += 1

        tis.save()

    except:
        return ApiFailure(GET_SPRINT_FAILURE)

    return ApiSuccess()

@csrf_exempt
def backwards(request):
    try:
        user_id = request.session['user']['id']

        if (not user_id):
            raise Exception
    except:
        return ApiFailure(NEED_LOGIN)


    try:
        user = User.objects.get(id=user_id)
        tis_id = request.POST.get('tis_id')
        tis = TicketInsideSprint.objects.get(id=tis_id)

    except:
        return ApiFailure(BAD_PARAMS)

    try:
        if tis.progress > 0:
            tis.progress -= 1

        tis.save()

    except:
        return ApiFailure(GET_SPRINT_FAILURE)

    return ApiSuccess()