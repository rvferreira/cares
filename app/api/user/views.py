from rest_framework import generics
from app.models import User, Enrollment
from app.serializers import UserSerializer, UserEnrollmentSerializer

class UserList (generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CareersList (generics.ListCreateAPIView):
    serializer_class = UserEnrollmentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        test = Enrollment.objects.filter(student__id=user_id)
        print ">>>>>>", test
        return test