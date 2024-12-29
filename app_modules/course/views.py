from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django.urls import reverse , reverse_lazy
from django.template.loader import get_template
from app_modules.course import course_forms , models
from django_datatables_too.mixins import DataTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from app_modules.base.utils import get_encoded_id , get_actions_buttons
from app_modules.base.views import BaseCreateView, BaseDeleteAjaxView, BaseListView, BaseUpdateView

#  <---------------------------------------------- List Views ----------------------------------------------->

class CategoryList(BaseListView):

    model = models.Category
    template_name = "categories/list.html"
    
    def get_user_type(self):
        return None
    
    def get_table_name(self):
        return "Category"
    
    def get_create_url(self):
        return reverse('course:create_category')
    
class CourseList(BaseListView):

    model = models.Course
    template_name = "course/list.html"
    
    def get_user_type(self):
        return None
    
    def get_table_name(self):
        return "Course"
    
    def get_create_url(self):
        return reverse('course:create_course')
    
class LessonList(BaseListView):

    model = models.Lesson
    template_name = "lesson/list.html"
    
    def get_user_type(self):
        return None
    
    def get_table_name(self):
        return "Lesson"
    
    def get_create_url(self):
        return reverse('course:create_lesson')

#  <---------------------------------------------- List Views ----------------------------------------------->

#  <---------------------------------------------- Data Tables ---------------------------------------------->

class CategoryDataTablesAjaxPagination(LoginRequiredMixin,DataTableMixin, View):

    """Category Datatable View"""

    model = models.Category

    def get_queryset(self):
        qs = models.Category.objects.all().order_by("-id")
        return self.filter_queryset(qs)

    def _get_actions(self, obj):
        update_url = reverse('course:update_category', kwargs={'encoded_id': get_encoded_id(obj.id)})
        delete_url = reverse('course:delete_category')
        return get_actions_buttons(update_url,delete_url,obj.name,get_encoded_id(obj.id))
        
    def filter_queryset(self, qs):
        return qs.filter(name__icontains=self.search) if self.search else qs
    
    def _get_full_name(self,obj):
        t = get_template("categories/get_name.html")
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
                    "name": self._get_full_name(o),
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)

class CourseDataTablesAjaxPagination(LoginRequiredMixin,DataTableMixin, View):

    """Course Datatable View"""

    model = models.Course

    def get_queryset(self):
        qs = self.model.objects.all().order_by("-id")
        return self.filter_queryset(qs)
    
    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(
                Q(title__icontains=self.search) |
                Q(category__name__icontains=self.search) | 
                Q(instructor__last_name__icontains=self.search) | 
                Q(instructor__first_name__icontains=self.search)
            )
        return qs
    
    def _get_actions(self, obj):
        update_url = reverse('course:update_course', kwargs={'encoded_id': get_encoded_id(obj.id)})
        delete_url = reverse('course:delete_course')
        return get_actions_buttons(update_url,delete_url,obj.title,get_encoded_id(obj.id))
        
    def prepare_results(self, qs):
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "name": o.title,
                    "category": o.category.name,
                    "instructor": o.instructor.get_full_name(),
                    "actions": self._get_actions(o),
                }
            )
        return data
    
    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)

class LessonDataTablesAjaxPagination(LoginRequiredMixin,DataTableMixin, View):

    """Lesson Datatable View"""

    model = models.Lesson

    def get_queryset(self):
        qs = self.model.objects.all().order_by("-id")
        return self.filter_queryset(qs)
    
    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(
                Q(title__icontains=self.search) |
                Q(course__title__icontains=self.search)
            )
        return qs
    
    def _get_actions(self, obj):
        update_url = reverse('course:update_lesson', kwargs={'encoded_id': get_encoded_id(obj.id)})
        delete_url = reverse('course:delete_lesson')
        return get_actions_buttons(update_url,delete_url,obj.title,get_encoded_id(obj.id))
            
    def prepare_results(self, qs):
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "name": o.title,
                    "course": o.course.title,
                    "actions": self._get_actions(o),
                }
            )
        return data
    
    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)

#  <---------------------------------------------- Data Tables ---------------------------------------------->

#  <---------------------------------------------- Create View ---------------------------------------------->
class CreateCategory(BaseCreateView):
    
    form_class = course_forms.CategoryForm
    template_name = "categories/form.html"
    success_url = reverse_lazy('course:categories_list')

    def get_current_page_name(self):
        return "Category"
    
    def get_breadcrumb_name(self):
        return "Category"
    
    def get_breadcrumb_url(self):
        return reverse_lazy('course:categories_list')
    
class CourseCreateView(BaseCreateView):
    
    form_class = course_forms.CourseForm
    template_name = "course/form.html"
    success_url = reverse_lazy('course:course_list')

    def get_current_page_name(self):
        return "Course"
    
    def get_breadcrumb_name(self):
        return "Course"
    
    def get_breadcrumb_url(self):
        return reverse_lazy('course:course_list')

class LessonCreateView(BaseCreateView):
    
    form_class = course_forms.LessonForm
    template_name = "lesson/form.html"
    success_url = reverse_lazy('course:lesson_list')

    def get_current_page_name(self):
        return "Lesson"
    
    def get_breadcrumb_name(self):
        return "Lesson"
    
    def get_breadcrumb_url(self):
        return reverse_lazy('course:lesson_list')

#  <---------------------------------------------- Create View ---------------------------------------------->

#  <---------------------------------------------- Update View ---------------------------------------------->
   
class CategoryUpdateView(BaseUpdateView):

    model = models.Category
    form_class = course_forms.CategoryForm
    template_name = "categories/form.html"
    success_url = reverse_lazy('course:categories_list')

    def get_breadcrumb_name(self):
        return "Categories"
    
    def get_breadcrumb_url(self):
        return reverse_lazy('course:categories_list')
    
    def get_page_name(self):
        return "Category"
    
    def get_current_page(self):
        return "Update Category"

class CourseUpdateView(BaseUpdateView):

    model = models.Course
    form_class = course_forms.CourseForm
    template_name = "course/form.html"
    success_url = reverse_lazy('course:course_list')

    def get_breadcrumb_name(self):
        return "Course"
    
    def get_breadcrumb_url(self):
        return reverse_lazy('course:course_list')
    
    def get_page_name(self):
        return "Course"
    
    def get_current_page(self):
        return "Update Course"

class LessonUpdateView(BaseUpdateView):

    model = models.Lesson
    form_class = course_forms.LessonForm
    template_name = "lesson/form.html"
    success_url = reverse_lazy('course:lesson_list')

    def get_breadcrumb_name(self):
        return "Lesson"
    
    def get_breadcrumb_url(self):
        return reverse_lazy('course:lesson_list')
    
    def get_page_name(self):
        return "Lesson"
    
    def get_current_page(self):
        return "Update Lesson"

#  <---------------------------------------------- Update View ---------------------------------------------->

#  <---------------------------------------------- Delete View ---------------------------------------------->

class CategoryDeleteAjaxView(BaseDeleteAjaxView):
    model = models.Category 

class CourseDeleteAjaxView(BaseDeleteAjaxView):
    model = models.Course 

class LessonDeleteAjaxView(BaseDeleteAjaxView):
    model = models.Lesson 
    
#  <---------------------------------------------- Delete View ---------------------------------------------->