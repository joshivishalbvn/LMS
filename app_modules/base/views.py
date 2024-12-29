from django.urls import reverse
from django.http import JsonResponse
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404
from app_modules.base.utils import delete_image
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,View,UpdateView

class BaseListView(LoginRequiredMixin,ListView):

    queryset = None
    template_name = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breadcrumbs"] = [
            {"name": "Dashboard", "url": reverse('dashboard')},
        ]
        ctx['current_page'] = self.get_current_page()
        ctx['create_url'] = self.get_create_url()
        ctx['table_name'] = self.get_table_name()
        ctx['user_type'] = self.get_user_type()
        return ctx
    
    def get_table_name(self):
        raise NotImplementedError("Subclasses should implement get_table_name() method")

    def get_user_type(self):
        raise NotImplementedError("Subclasses should implement get_user_type() method")

    def get_create_url(self):
        raise NotImplementedError("Subclasses should implement get_create_url() method")

    def get_current_page(self):
        return self.get_table_name()
    
class BaseCreateView(LoginRequiredMixin,CreateView):
    
    model = None
    form_class = None
    template_name = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breadcrumbs"] = [
            {"name": "Dashboard", "url": reverse('dashboard')},
            {"name": self.get_breadcrumb_name(), "url": self.get_breadcrumb_url()},
        ]
        ctx["page_name"] = self.get_current_page_name()
        ctx["current_page"] = self.get_current_page()
        return ctx

    def get_breadcrumb_name(self):
        raise NotImplementedError("Subclasses must implement get_breadcrumb_name")

    def get_breadcrumb_url(self):
        raise NotImplementedError("Subclasses must implement get_breadcrumb_url")

    def get_current_page(self):
        return f"Add {self.get_current_page_name()}"
    
    def get_current_page_name(self):
        raise NotImplementedError("Subclasses must implement get_current_page_name")
    
class BaseDeleteAjaxView(LoginRequiredMixin, View):

    """Base class for delete views to avoid redundancy."""
    
    model = None  
    
    def post(self, request):

        obj_id = force_str(urlsafe_base64_decode(request.POST.get("id")))
        obj = get_object_or_404(self.model, id=obj_id)
        image_path = obj.image.path if obj.image else None
        
        try:
            obj_name = obj.title if hasattr(obj, 'title') else obj.name  
        except:
            obj_name = obj.get_full_name()
        
        obj.delete()
        if image_path:
            delete_image(image_path)
        
        return JsonResponse({
            "message": f"{obj_name.title()} Deleted Successfully."
        })
    
class BaseUpdateView(LoginRequiredMixin,UpdateView):
    
    """Base class for update views to avoid redundancy."""
    
    model = None  
    form_class = None  
    success_url = None  
    template_name = None 
    
    def get_object(self, queryset=None):
        obj_id = force_str(urlsafe_base64_decode(self.kwargs['encoded_id']))
        return get_object_or_404(self.model, id=obj_id)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breadcrumbs"] = [
            {"name": "Dashboard", "url": reverse('dashboard')},
            {"name": self.get_breadcrumb_name(), "url": self.get_breadcrumb_url()},
        ]
        ctx['page_name'] = self.get_page_name()
        ctx['current_page'] = self.get_current_page()
        return ctx
    
    def get_breadcrumb_name(self):
        raise NotImplementedError("Subclasses should implement get_breadcrumb_name()")

    def get_breadcrumb_url(self):
        raise NotImplementedError("Subclasses should implement get_breadcrumb_url()")
    
    def get_page_name(self):
        raise NotImplementedError("Subclasses should implement get_page_name()")
    
    def get_current_page(self):
        raise NotImplementedError("Subclasses should implement get_current_page()")