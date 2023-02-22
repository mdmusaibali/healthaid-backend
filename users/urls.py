from django.urls import path
from .views import CreatePatientView, CreateStaffView, StaffLoginView, SuperadminLoginView, add_patient, check_token, delete_patient, delete_staff, get_all_patients, get_all_staff

urlpatterns = [
    path('superadmin/login/', SuperadminLoginView.as_view(), name='superadmin-login'),
    path('superadmin/create_staff/', CreateStaffView.as_view(), name='create-staff'),
    path('superadmin/get_staff/', get_all_staff, name='get-staff'),
    path('superadmin/delete_staff/<int:user_id>', delete_staff, name='delete-staff'),
    path('staff/create_patient/', CreatePatientView.as_view(), name='create-patient'),
    path('staff/delete_patient/<str:patient_id>', delete_patient, name='delete-patient'),
    path('staff/get_patients/', get_all_patients, name='get-patients'),
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
    path('user/check_token/', check_token, name='check-token'),



    



    


]
