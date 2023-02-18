from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Staff, Patient
from django import forms

class UserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_superadmin', 'is_patient')
    list_filter = ('is_staff', 'is_superadmin', 'is_patient')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superadmin', 'is_patient')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_superadmin', 'is_patient')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('patient_id',)

# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # model = Patient
    form = PatientForm


admin.site.register(User)
admin.site.register(Staff)


