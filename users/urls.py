from django.urls import path
from .views import PatientSignupView, CreateStaffView, StaffLoginView, SuperadminLoginView

urlpatterns = [
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
    path('superadmin/login/', SuperadminLoginView.as_view(), name='superadmin-login'),
    path('superadmin/create_staff/', CreateStaffView.as_view(), name='create-staff'),
    path('patients/signup/', PatientSignupView.as_view(), name='patient-signup'),
]
