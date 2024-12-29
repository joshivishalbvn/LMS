from django.urls import path
from app_modules.users import views

app_name = 'users'

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/', views.UserListView.as_view(), name='admin_list'),
    path('student/', views.StudentListView.as_view(), name='student_list'),
    path('teacher/', views.TeacherListView.as_view(), name='teacher_list'),
    path('delete', views.UserDeleteAjaxView.as_view(), name='delete_user'),
    path('add/admin/', views.AdminCreateView.as_view(), name='add_user_form'),
    path('add/teacher/', views.TeacherCreateView.as_view(), name='add_teacher_form'),
    path('add/student/', views.StudentCreateView.as_view(), name='add_student_form'),
    path('<str:encoded_id>/update', views.UserUpdateView.as_view(), name='update_user'),
    path('<str:encoded_id>/details', views.UserDetailsView.as_view(), name='user_details'),
    path('user_list_ajax', views.UserDataTablesAjaxPagination.as_view(), name='user_list_ajax'),
]