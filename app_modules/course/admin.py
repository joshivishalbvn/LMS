from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import Category, Course, Lesson, Enrollment

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    description = forms.CharField(widget=CKEditorWidget())

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    description = forms.CharField(widget=CKEditorWidget())

class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

    description = forms.CharField(widget=CKEditorWidget())
    content = forms.CharField(widget=CKEditorWidget())

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm

admin.site.register(Enrollment)
