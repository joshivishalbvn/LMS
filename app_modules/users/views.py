from django.db.models import Q
from app_modules.users import tasks
from app_modules.users import models
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.encoding import force_str
from allauth.account.views import LogoutView
from django.urls import reverse , reverse_lazy
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from app_modules.users.user_forms import UserForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model,logout
from django_datatables_too.mixins import DataTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from app_modules.base.utils import get_encoded_id,get_actions_buttons
from django.views.generic import TemplateView,View,UpdateView,DetailView
from app_modules.base.views import BaseDeleteAjaxView, BaseListView, BaseCreateView

User = get_user_model()

class DashboardView(LoginRequiredMixin,TemplateView):
    
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['current_page'] = "Dashboard"
        return ctx

class UserListView(BaseListView):

    template_name = "users/list.html"
    queryset = models.SuperAdmin.objects.all()

    def get_table_name(self):
        return "Admin"
    
    def get_user_type(self):
        return User.SUPER_ADMIN
    
    def get_create_url(self):
        return reverse('users:add_user_form')

class StudentListView(BaseListView):

    template_name = "users/list.html"
    queryset = models.SuperAdmin.objects.all()

    def get_table_name(self):
        return User.STUDENT

    def get_user_type(self):
        return User.STUDENT
    
    def get_create_url(self):
        return reverse('users:add_student_form')

class TeacherListView(BaseListView):

    template_name = "users/list.html"
    queryset = models.SuperAdmin.objects.all()

    def get_table_name(self):
        return User.TEACHER
    
    def get_user_type(self):
        return User.TEACHER
    
    def get_create_url(self):
        return reverse('users:add_teacher_form')
   
class BaseUserCreateView(BaseCreateView):

    """Base User Create View to handle common logic for all user roles."""

    model = User
    password = "test@123" 
    form_class = UserForm
    template_name = "users/user_form.html"

    def get_user_role(self):
        """Method to be overridden in subclasses to set user role."""
        raise NotImplementedError

    def get_role_specific_data(self):
        """Method to return role-specific data for breadcrumbs and current page."""
        raise NotImplementedError

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = self.get_user_role()  
        user.set_password(self.password)
        user.save()
        tasks.send_email_notifications.delay()
        task_obj = tasks.SendUserCredentialsEmail()
        task_obj.apply_async(args=[user.id, self.password])
        return super().form_valid(form)

    def get_current_page_name(self):
        return self.get_role_specific_data()['current_page']

    def get_breadcrumb_name(self):
        return self.get_role_specific_data()['breadcrumb_name']

    def get_breadcrumb_url(self):
        return self.get_role_specific_data()['breadcrumb_url']

class AdminCreateView(BaseUserCreateView):

    """Admin Create View."""

    success_url = reverse_lazy('users:admin_list')
    
    def get_user_role(self):
        return User.SUPER_ADMIN

    def get_role_specific_data(self):
        return {
            'current_page': "Admin",
            'breadcrumb_name': "Admin",
            'breadcrumb_url': reverse_lazy('users:admin_list')
        }

class TeacherCreateView(BaseUserCreateView):

    """Teacher Create View."""

    success_url = reverse_lazy('users:teacher_list')

    def get_user_role(self):
        return User.TEACHER

    def get_role_specific_data(self):
        return {
            'current_page': User.TEACHER,
            'breadcrumb_name': User.TEACHER,
            'breadcrumb_url': reverse_lazy('users:teacher_list')
        }

class StudentCreateView(BaseUserCreateView):

    """Student Create View."""
    
    success_url = reverse_lazy('users:student_list')

    def get_user_role(self):
        return User.STUDENT

    def get_role_specific_data(self):
        return {
            'current_page': User.STUDENT,
            'breadcrumb_name': User.STUDENT,
            'breadcrumb_url': reverse_lazy('users:student_list')
        }

class UserUpdateView(LoginRequiredMixin,UpdateView):

    model = User
    form_class = UserForm
    template_name = "users/user_form.html"

    def get_object(self, queryset=None):

        return get_object_or_404(User, id=force_str(urlsafe_base64_decode(self.kwargs['encoded_id'])))

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()

        role_mapping = {
            User.SUPER_ADMIN: ("Update Admin", "Admin", reverse('users:admin_list')),
            User.TEACHER: ("Update Teacher", "Teacher", reverse('users:teacher_list')),
            User.STUDENT: ("Update Student", "Student", reverse('users:student_list')),
        }

        current_page, page_name, breadcrumb_url = role_mapping.get(obj.role)

        ctx.update({
            'current_page': current_page,
            'page_name': page_name,
            'breadcrumbs': [
                {"name": "Dashboard", "url": reverse_lazy('dashboard')},
                {"name": page_name, "url": breadcrumb_url},
            ]
        })
        
        return ctx
    
    def get_success_url(self):

        role_to_url = {
            User.SUPER_ADMIN: 'users:admin_list',
            User.TEACHER: 'users:teacher_list',
            User.STUDENT: 'users:student_list',
        }
        return reverse_lazy(role_to_url.get(self.object.role)) 
        
class UserDetailsView(LoginRequiredMixin,DetailView):

    model = User
    pk_url_kwarg = 'encoded_id'
    context_object_name = 'user'
    template_name = "users/user_details.html"

    def get_object(self):

        encoded_pk = self.kwargs.get(self.pk_url_kwarg)
        user_id = force_str(urlsafe_base64_decode(encoded_pk))
        return get_object_or_404(User, id=user_id)
    
    def get_context_data(self, **kwargs):

        ctx =  super().get_context_data(**kwargs)
        ctx['breadcrumbs'] = [
            {"name": "Pages", "url": "javascript:;"},
        ]
        ctx["current_page"] = self.get_object().get_full_name()
        return ctx
    
class UserDeleteAjaxView(BaseDeleteAjaxView):

    """User Delete View"""
    
    model = User  
    
class UserDataTablesAjaxPagination(LoginRequiredMixin,DataTableMixin, View):

    """User Datatable View"""

    model = User

    def get_queryset(self):

        qs = User.objects.all()
        role = self.request.GET.get("role")
        if role:
            qs = qs.filter(role=role)
        return self.filter_queryset(qs)

    def _get_actions(self, obj):

        delete_url = reverse('users:delete_user')
        update_url = reverse('users:update_user', kwargs={'encoded_id': get_encoded_id(obj.id)})
        return get_actions_buttons(update_url,delete_url,obj.get_full_name(),get_encoded_id(obj.id))

    def filter_queryset(self, qs):

        if self.search:
            return qs.filter(
                Q(first_name__icontains=self.search) |
                Q(last_name__icontains=self.search) | 
                Q(email__icontains=self.search) | 
                Q(mobile__icontains=self.search)
            )
        return qs
    
    def _get_full_name(self,obj):

        t = get_template("users/get_full_name.html")
        context = {
            "obj": obj,
        }
        return t.render(context)

    def prepare_results(self, qs):

        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "full_name": self._get_full_name(o),
                    "mobile": o.mobile if o.mobile else "-----",
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):

        context_data = self.get_context_data(request)
        return JsonResponse(context_data)
   
class LogoutView(LoginRequiredMixin,LogoutView):

    def get(self, request):
        logout(self.request)
        return redirect("/accounts/login")