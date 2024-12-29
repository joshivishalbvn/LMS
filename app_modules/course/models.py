from time import timezone
from django.db import models
from ckeditor.fields import RichTextField
from app_modules.base.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app_modules.users.models import Teachers, Students

class Category(BaseModel):

    name        = models.CharField(_('Name'), max_length=100, unique=True)
    image       = models.ImageField(_('Category Image'), upload_to='categories/', null=True, blank=True)
    description = RichTextField(_('Description'), null=True, blank=True)

    class Meta:
        ordering = ['-created_at']  
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"

    def __str__(self):
        return self.name

class Course(BaseModel):

    BEGINNER     = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED     = "Advanced"

    LEVEL_CHOICES = (
        (BEGINNER, BEGINNER),
        (INTERMEDIATE, INTERMEDIATE),
        (ADVANCED, ADVANCED),
    )

    title       = models.CharField(_('Title'), max_length=200)
    description = RichTextField(_('Description'))  
    category    = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)
    instructor  = models.ForeignKey(Teachers, related_name='course_teacher', on_delete=models.CASCADE)
    duration    = models.DurationField(_('Duration')) 
    start_date  = models.DateField(_('Start Date'))
    end_date    = models.DateField(_('End Date'))
    level       = models.CharField(_('Level'), choices=LEVEL_CHOICES, default=BEGINNER, max_length=100)
    image       = models.ImageField(_('Image'), upload_to='courses/', null=True, blank=True)
    price       = models.DecimalField(_('Price'), max_digits=8, decimal_places=2, null=True, blank=True)
    is_free     = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return self.title
    
    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date

class Lesson(BaseModel):

    course      = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title       = models.CharField(_('Title'), max_length=200)
    description = RichTextField(_('Description'))  
    video_url   = models.URLField(_('Video URL'), null=True, blank=True)
    content     = RichTextField(_('Content'), null=True, blank=True)
    
    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
    
    def __str__(self):
        return self.title

class Enrollment(BaseModel):

    student     = models.ForeignKey(Students, related_name='enrollments', on_delete=models.CASCADE)
    course      = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed   = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f'{self.student.username} enrolled in {self.course.title}'