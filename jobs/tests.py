from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import Job
from model_mommy import mommy


class TestJobViewSet(TestCase):
    def setUp(self):
        # Create a sample Job instance for testing
        city = mommy.make('address.City', name='Test City')
        company = mommy.make('company.Company', name='Test Company')
        self.job_data = {
            'title': 'Test Job',
            'description': 'This is a test job description.',
            'work_type': 'office',  # Assuming 'full_time' is a valid WorkType
            'status': 'new',  # Assuming 'published' is a valid JobStatus
            'city': city,
            'company': company,
            'date_posted': '2020-01-01T00:00:00Z',
            'linkedin_job_id': "123123123"
        }
        self.job = mommy.make('jobs.Job', **self.job_data)

        # Create an instance of the APIClient for making requests
        self.client = APIClient()

    def test_list_jobs(self):
        # Test the endpoint that lists all jobs
        response = self.client.get('/api/jobs/')  # Adjust the URL according to your project's URL structure
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming there is one job in the database

    def test_retrieve_job(self):
        # Test the endpoint that retrieves a single job
        response = self.client.get(
            f'/api/jobs/{self.job.id}/')  # Adjust the URL according to your project's URL structure
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.job_data['title'])

    def test_create_job(self):
        # Test the endpoint that creates a new job
        job_data = {
            'title': 'Test Job2',
            'description': 'This is a test job description.',
            'work_type': 'office',  # Assuming 'full_time' is a valid WorkType
            'status': 'new',  # Assuming 'published' is a valid JobStatus
            'company': '1sds',
            'city': '1sdsadas',
            'date_posted': '2020-01-01T00:00:00Z',
            'linkedin_job_id': "123123123"
        }
        response = self.client.post('/api/jobs/', job_data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the new job was created in the database
        new_job = Job.objects.get(title=job_data['title'])
        self.assertIsNotNone(new_job)

    def test_update_job(self):
        # Test the endpoint that updates an existing job
        updated_data = {
            'title': 'Updated Test Job',
            'description': 'This is an updated test job description.',
            'work_type': 'contract',  # Assuming 'contract' is a valid WorkType
            'status': 'published',  # Assuming 'published' is a valid JobStatus
        }
        response = self.client.put(f'/api/jobs/{self.job.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the job in the database has been updated
        updated_job = Job.objects.get(id=self.job.id)
        self.assertEqual(updated_job.title, updated_data['title'])

    def test_delete_job(self):
        # Test the endpoint that deletes a job
        response = self.client.delete(
            f'/api/jobs/{self.job.id}/')  # Adjust the URL according to your project's URL structure
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the job has been deleted from the database
        with self.assertRaises(Job.DoesNotExist):
            Job.objects.get(id=self.job.id)
