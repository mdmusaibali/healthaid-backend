from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Patient, User, Staff
from .serializers import PatientSerializer, UserSerializer, StaffSerializer
from .permissions import IsSuperAdmin


class PatientSignupView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        user_serializer = UserSerializer(data=self.request.data['user'])
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.is_patient = True
            user.save()
            raw_password = user.password
            user.set_password(raw_password)
            user.save()
            self.request.data['user'] = user.pk
            patient = serializer.save()
            # login(self.request, user) #user logged in after patient is created

# creating staff by superadmin
class CreateStaffView(APIView):
    permission_classes = (IsSuperAdmin,)

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not name or not email or not password:
            return Response({"error": "Please provide a name, email, and password"}, status=status.HTTP_400_BAD_REQUEST)
        try:

            user = User.objects.create_user(email=email, password=password, name=name, is_staff=True)
            user.save()

            staff = Staff(user=user)
            staff.save()
            return Response({"message": "staff successfully created"}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


# staff login 
class StaffLoginView(APIView):

    def post(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_staff:
            return Response({"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = AccessToken.for_user(user)

        return Response({
            "access_token": str(access_token),
            "token_type": "bearer"
        }, status=status.HTTP_200_OK)

# superadmin login view

class SuperadminLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_superadmin:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)