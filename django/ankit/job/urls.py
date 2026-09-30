from django.urls import path
from .views import (
    PostJobView, MyPostsView, UpdateJobView, JobStatusView,
    ViewApplicantProfileView, ApplyJobView, AppliedJobsView,
    ListJobView, FilterJobView
)

urlpatterns = [
    path('postjob/', PostJobView.as_view()),
    path('myposts/', MyPostsView.as_view()),
    path('updatejob/<int:id>', UpdateJobView.as_view()),
    path('jobstatus/<int:job_id>', JobStatusView.as_view()),
    path('viewprofile/<int:applicant_id>', ViewApplicantProfileView.as_view()),
    path('applyjob/', ApplyJobView.as_view()),
    path('appliedjobs/', AppliedJobsView.as_view()),
    path('listjob/', ListJobView.as_view()),
    path('filterjob/', FilterJobView.as_view()),
]
