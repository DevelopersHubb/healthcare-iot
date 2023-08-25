from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Hospital, User, User_Role
from .serializers import CustomCreateSerializer, HospitalSerializer, UserSerializer, UserRoleSerializer


class CustomCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None, *args, **kwargs):
        instance = Hospital.objects.get(id=id)
        serializer = CustomCreateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRoleViewSet(ModelViewSet):
    queryset = User_Role.objects.all()
    serializer_class = UserRoleSerializer

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def doctors_profile(self, request):
        doctors_profile = self.queryset.filter(user_role='doctor')
        serializer = UserRoleSerializer(doctors_profile, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def hospital_admin_profile(self, request):
        hospital_admin_profile = self.queryset.filter(user_role='hospital_admin')
        serializer = UserRoleSerializer(hospital_admin_profile, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def nurse_profile(self, request):
        nurse_profile = self.queryset.filter(user_role='nurse')
        serializer = UserRoleSerializer(nurse_profile, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
