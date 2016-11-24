from rest_framework import generics
from lib.api import ApiFailure, ApiSuccess
from lib.error_codes import *
from app.models import User, Enrollment
from app.serializers import UserSerializer, UserEnrollmentSerializer

class UserList (generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EnrollmentList (generics.ListCreateAPIView):
    serializer_class = UserEnrollmentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        test = Enrollment.objects.filter(student__id=user_id)
        return test

def get_all_enrollments(request):
    try:
        user_id = request.session['user']['id']

        if (not user_id):
            raise Exception
    except:
        return ApiFailure(NEED_LOGIN)


    try:
        user = User.objects.get(id=user_id)

    except:
        return ApiFailure(BAD_PARAMS)

    try:
        enrollments = []
        e = Enrollment.objects.filter(student=user).all()

        for elem in e:
            enrollments.append({
                'id': elem.id,
                'career': elem.career.name
            })

    except:
        ApiFailure(GET_ENROLLMENTS_FAILURE)

    return ApiSuccess(enrollments)
