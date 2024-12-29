import datetime
from django import forms
from app_modules.course import models
from ckeditor.widgets import CKEditorWidget
from django_select2 import forms as s2forms
from durationwidget.widgets import TimeDurationWidget

class CategoryForm(forms.ModelForm):
    
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Category
        fields = ['name', 'description',"image"]

class CategoryWidget(s2forms.ModelSelect2Widget):

    model = models.Category
    search_fields = [
        "name__icontains",
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs["data-minimum-input-length"] = 0
        attrs["data-allow-clear"] = True
        return attrs

class InstructorWidget(s2forms.ModelSelect2Widget):
    
    model = models.Teachers
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs["data-minimum-input-length"] = 0
        attrs["data-allow-clear"] = True
        return attrs
    
class CourseForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorWidget())
    duration = forms.DurationField(
        widget=TimeDurationWidget(
            show_days=True, show_hours=False, show_minutes=False, show_seconds=False
        ), 
        required=False
    )

    class Meta:
        model = models.Course
        fields = (
            "title",
            "description",
            "category",
            "instructor",
            "duration",
            "start_date",
            "end_date",
            "level",
            "image",
            "price",
            "is_free",
        )
        widgets = {
            "category": CategoryWidget,
            "instructor": InstructorWidget,
        } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs.update({
            'class': 'datepicker',
            'onchange': 'calculate_duration()'
        })
        self.fields['end_date'].widget.attrs.update({
            'class': 'datepicker',
            'onchange': 'calculate_duration()'
        })

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        duration = cleaned_data.get('duration')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', "End date cannot be earlier than start date.")
            
            diff_duration = end_date - start_date + datetime.timedelta(days=1)
        
        if duration != diff_duration:
            self.add_error('duration', "The duration should be the difference between start and end dates.")

        return cleaned_data
    
class CourseWidget(s2forms.ModelSelect2Widget):

    model = models.Course
    search_fields = [
        "title__icontains",
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs["data-minimum-input-length"] = 0
        attrs["data-allow-clear"] = True
        return attrs
    
class LessonForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Lesson
        fields = (
            "course",
            "title",
            "description",
            "video_url",
            "content",
        )
        widgets = {
            "course": CourseWidget,
        } 