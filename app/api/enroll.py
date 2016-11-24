from lib.api import ApiSuccess, ApiFailure
from lib.error_codes import *
from lib.generator import main as generate_sprint
from app.models import User, Career, Enrollment, Ticket, TicketInsideSprint, Sprint
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

        sprint = Sprint()
        sprint.save()

        generated_sprint = generate_sprint(career.tickets.all())
        for ticket_id in generated_sprint:
            t = Ticket.objects.get(id=ticket_id)
            tis = TicketInsideSprint(ticket=t)
            tis.save()

            sprint.tickets.add(tis)
            sprint.save()


        try:
            e = Enrollment(
                student=user,
                career=career,
            )
            e.save()

            e.sprints.add(sprint)
            e.save()

        except:
            return ApiFailure(ENROLL_FAILURE)


        return ApiSuccess()

    return ApiFailure(ALREADY_ENROLLED)
