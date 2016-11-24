from lib.api import ApiSuccess, ApiFailure
from lib.error_codes import *
from app.models import Enrollment, Sprint, User

def latest_sprint(request):
    try:
        user_id = request.session['user']['id']

        if (not user_id):
            raise Exception
    except:
        return ApiFailure(NEED_LOGIN)


    try:
        user = User.objects.get(id=user_id)
        enrollment = request.GET.get('enrollment')
        enrollment = Enrollment.objects.get(id=enrollment, student=user)

        sprints = enrollment.sprints.all()

    except:
        return ApiFailure(BAD_PARAMS)

    try:
        last_sprint = sprints[0]

        for sprint in sprints:
            if sprint.id > last_sprint.id:
                last_sprint = sprint

        tickets = []

        for ticket in last_sprint.tickets.all():
            tickets.append({
                'tis_id': ticket.id,
                'id': ticket.ticket.id,
                'name': ticket.ticket.name,
                'topic': ticket.ticket.topic.name,
                'progress': ticket.progress,
                'description': ticket.ticket.description
            })
    except:
        return ApiFailure(GET_SPRINT_FAILURE)

    return ApiSuccess(tickets)