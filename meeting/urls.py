from django.urls import path

from . import views

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('projects/create', views.ProjectCreationProcess.as_view(), name='ProjectCreationProcess'),
    path('projects/<int:project_key>', views.ProjectViewProcess.as_view(), name="ProjectViewProcess"),
    path('projects/<int:project_key>/edit', views.ProjectModificationProcess.as_view(), name="ProjectModificationProcess"),
    path('projects/<int:project_key>/meetings/create', views.MeetingView.as_view(), name="MeetingView"),
    path('login', views.LoginProcess.as_view(), name="LoginProcess"),
    path('register', views.RegisterProcess.as_view(), name="RegisterProcess"),
    path('availability', views.availability, name='Availability'),
    path('availability/<int:meeting_id>', views.Availability.as_view(), name='meeting_availability'),
    path('availability/<int:meeting_id>/delete', views.AvailabilityDelete.as_view(), name='AvailabilityDelete'),
    path('voting', views.Voting.as_view(), name='Voting'),
    path('profile', views.ProfilePage.as_view(), name="ProfilePage"),
    path('notification_demo', views.notification_demo, name='notification_demo'),
    path('notifications', views.NotificationProcess.as_view(), name='NotificationProcess')
]
