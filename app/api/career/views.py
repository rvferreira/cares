from rest_framework import generics
from app.models import Career
from app.serializers import SimplifiedCareerSerializer, CareerSerializer

class CareerList (generics.ListCreateAPIView):
    queryset = Career.objects.filter(public=1)
    serializer_class = SimplifiedCareerSerializer

class CareerDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer