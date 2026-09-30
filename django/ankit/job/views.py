from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from user.permissions import IsRecruiter, IsSeeker
from user.models import UserDetails
from user.serializers import SeekerProfileSerializer


class PostJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recruiter=request.user)
            return Response({"message": "job details have been posted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyPostsView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request):
        jobs = Job.objects.filter(recruiter=request.user)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class UpdateJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def _get_job(self, pk, user):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return None, Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if job.recruiter != user:
            return None, Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return job, None

    def patch(self, request, id):
        job, err = self._get_job(id, request.user)
        if err:
            return err
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "job details have been updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        job, err = self._get_job(id, request.user)
        if err:
            return err
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobStatusView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if job.recruiter != request.user:
            return Response(
                {"message": "You do not have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        applications = Application.objects.filter(job=job)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ViewApplicantProfileView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request, applicant_id):
        try:
            seeker = UserDetails.objects.get(pk=applicant_id, is_staff=False)
        except UserDetails.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SeekerProfileSerializer(seeker)
        return Response(serializer.data)


class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def post(self, request):
        job_id = request.data.get('job_id')
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if Application.objects.filter(job=job, applicant=request.user).exists():
            return Response(
                {"message": "You have already applied for this job"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        Application.objects.create(job=job, applicant=request.user)
        return Response({"message": "You have successfully applied for this job"}, status=status.HTTP_200_OK)


class AppliedJobsView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def get(self, request):
        applications = Application.objects.filter(applicant=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ListJobView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class FilterJobView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search = request.query_params.get('search', '')
        jobs = Job.objects.filter(
            Q(job_title__icontains=search) |
            Q(work_location__icontains=search) |
            Q(skills__icontains=search) |
            Q(recruiter__company__icontains=search)
        )
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
