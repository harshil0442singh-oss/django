from django.db import models
from django.conf import settings


class Job(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    job_title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    work_location = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    openings = models.IntegerField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.job_title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} -> {self.job}"
