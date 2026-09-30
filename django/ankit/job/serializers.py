from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='recruiter.company', read_only=True)
    about_company = serializers.CharField(source='recruiter.about_company', read_only=True)
    website = serializers.CharField(source='recruiter.website', read_only=True)
    no_of_applicants = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'job_title', 'company', 'description', 'skills', 'experience',
            'work_location', 'employment_type', 'qualification', 'about_company',
            'website', 'openings', 'no_of_applicants', 'application_deadline'
        ]
        read_only_fields = ['id']

    def get_no_of_applicants(self, obj):
        return obj.applications.count()


class ApplicationSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(source='job.id', read_only=True)
    job_title = serializers.CharField(source='job.job_title', read_only=True)
    company = serializers.CharField(source='job.recruiter.company', read_only=True)
    applicant_id = serializers.IntegerField(source='applicant.id', read_only=True)
    applicant_name = serializers.CharField(source='applicant.name', read_only=True)
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)

    class Meta:
        model = Application
        fields = ['job_id', 'job_title', 'company', 'applicant_id', 'applicant_name', 'applicant_email']
