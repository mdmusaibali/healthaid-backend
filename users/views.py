from sqlite3 import IntegrityError
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .models import Patient, User, Staff
from .serializers import PatientSerializer, UserSerializer, StaffSerializer
from .permissions import IsSuperAdmin, IsStaff




# creating staff by superadmin
class CreateStaffView(APIView):
    permission_classes = (IsSuperAdmin,)
    parser_classes = [JSONParser]

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
    parser_classes = [JSONParser]


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
    parser_classes = [JSONParser]
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_superadmin:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


# check whether the token is expired or not
@api_view(['GET'])

def check_token(request):
    
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        AccessToken(token)
    except TokenError:
        return Response({"error": "Token has been expired"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)

@api_view(['POST'])

@permission_classes([IsAuthenticated, IsStaff])
def add_patient(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        patient_serializer = PatientSerializer(data=request.data)
        if patient_serializer.is_valid():
            patient = patient_serializer.save(user=user)
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED)
        return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class CreatePatientView(generics.CreateAPIView):
    parser_classes = [JSONParser,MultiPartParser]
    permission_classes = (IsStaff,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        
        patient = serializer.save()

#  get all patients for staff
@api_view(['GET'])

@permission_classes([IsAuthenticated, IsStaff])
def get_all_patients(request):
    if not request.user.is_staff:
        return Response({"error": "Only staff members can access this information."}, status=status.HTTP_401_UNAUTHORIZED)

    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# get all staff by superadmin
@api_view(['GET'])

@permission_classes([IsAuthenticated, IsSuperAdmin])
def get_all_staff(request):
    if not request.user.is_superadmin:
        return Response({"error": "Only SuperAdmin can access this information."}, status=status.HTTP_401_UNAUTHORIZED)

    staff = Staff.objects.all()
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# delete Staff by ID View
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def delete_staff(request, user_id):
    try:
        staff = Staff.objects.get(user_id=user_id)
    except Staff.DoesNotExist:
        return Response({"error": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=user_id)
    staff.delete()
    user.delete()

    return Response({"message": "Staff deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# delete patient by patient_id view
@api_view(['DELETE'])

@permission_classes([IsAuthenticated, IsStaff])
def delete_patient(request, patient_id):
    if not request.user.is_staff:
        return Response({"error": "Only staff can delete patients."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

    patient.delete()

    return Response({"message": "Patient deleted successfully."}, status=status.HTTP_200_OK)
