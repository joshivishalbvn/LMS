from .models import *
from django.contrib import admin

class StudentsAdmin(admin.ModelAdmin):

    exclude = ('role', 'is_superuser', 'is_staff', 'last_login', 'groups', 'user_permissions',)
    fieldsets = (
        ('Primary Details', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'mobile', 'image', 'status')
        }),
        ('Authentication', {
            'fields': ('password',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.role = User.STUDENT 
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class TeachersAdmin(admin.ModelAdmin):

    exclude = ('role', 'is_superuser', 'is_staff', 'last_login', 'groups', 'user_permissions',)
    fieldsets = (
        ('Primary Details', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'mobile', 'image', 'status')
        }),
        ('Authentication', {
            'fields': ('password',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.role = User.TEACHER  
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class SuperAdminAdmin(admin.ModelAdmin):

    exclude = ('role','last_login', 'groups', 'user_permissions',)
    fieldsets = (
        ('Primary Details', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'mobile', 'image', 'status')
        }),
        ('Authentication', {
            'fields': ('password',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.role = User.SUPER_ADMIN  
        obj.is_superuser = True     
        obj.is_staff = True         
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(Students, StudentsAdmin)
admin.site.register(Teachers, TeachersAdmin)
admin.site.register(SuperAdmin, SuperAdminAdmin)