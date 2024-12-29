from django.urls import path
from app_modules.course import views

app_name = 'course'

urlpatterns = [
    # <------------------------------------------- Categories ------------------------------------------->
    path('categories/', views.CategoryList.as_view(), name='categories_list'),
    path('category/add/', views.CreateCategory.as_view(), name='create_category'),
    path('category/delete', views.CategoryDeleteAjaxView.as_view(), name='delete_category'),
    path('category/<str:encoded_id>/update', views.CategoryUpdateView.as_view(), name='update_category'),
    # <------------------------------------------- Categories ------------------------------------------->

    # <--------------------------------------------- Course --------------------------------------------->
    path('courses', views.CourseList.as_view(), name='course_list'),
    path('course/add/', views.CourseCreateView.as_view(), name='create_course'),
    path('course/delete', views.CourseDeleteAjaxView.as_view(), name='delete_course'),
    path('<str:encoded_id>/update', views.CourseUpdateView.as_view(), name='update_course'),
    # <--------------------------------------------- Course --------------------------------------------->

    # <-------------------------------------------- Lessons --------------------------------------------->
    path('lessons', views.LessonList.as_view(), name='lesson_list'),
    path('lesson/add/', views.LessonCreateView.as_view(), name='create_lesson'),
    path('lesson/delete', views.LessonDeleteAjaxView.as_view(), name='delete_lesson'),
    path('lesson/<str:encoded_id>/update', views.LessonUpdateView.as_view(), name='update_lesson'),
    # <-------------------------------------------- Lessons --------------------------------------------->

    # <------------------------------------------ Data Table -------------------------------------------->
    path('course_list_ajax', views.CourseDataTablesAjaxPagination.as_view(), name='course_list_ajax'),
    path('lesson_list_ajax', views.LessonDataTablesAjaxPagination.as_view(), name='lesson_list_ajax'),
    path('category_list_ajax', views.CategoryDataTablesAjaxPagination.as_view(), name='category_list_ajax'),
    # <------------------------------------------ Data Table -------------------------------------------->
]