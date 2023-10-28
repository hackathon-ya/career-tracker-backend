from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker

from core.models import City, Forms_of_employment, Work_arrangements
from users.models import Candidate, Favorites, Recruiter
from vacancies.models import Vacancy

fake = Faker()


class EndpointTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.recruiter = Recruiter.objects.create_user(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        cls.candidate = Candidate.objects.create(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        cls.candidate_2 = Candidate.objects.create(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        cls.city = City.objects.create(name=fake.city())
        cls.form_of_employment = Forms_of_employment.objects.create(name=fake.word())
        cls.work_arrangement = Work_arrangements.objects.create(name=fake.word())
        cls.vacancy = Vacancy.objects.create(
            user=cls.recruiter,
            job_title=fake.word(),
            company_name=fake.word(),
            city=cls.city,
            form_of_employment=cls.form_of_employment,
            min_salary=fake.random_int(min=0, max=1500),
            max_salary=fake.random_int(min=1501, max=30000),
            description=fake.text(max_nb_chars=1000),
            experience_month=fake.random_int(min=0, max=300),
            is_active=fake.boolean(),
            is_draft=fake.boolean(),
            is_archived=fake.boolean(),
            is_deleted=fake.boolean(),
        )
        cls.favorite = Favorites.objects.create(
            candidate=cls.candidate, recruiter=cls.recruiter
        )

    def test_get_create_endpoints(self):
        client = APIClient()
        responses = []
        responses.append(client.get(reverse("users:candidates-list")))
        responses.append(client.get(reverse("users:candidates-detail", args=(1,))))
        responses.append(client.get(reverse("vacancies:vacancy-list")))
        responses.append(client.get(reverse("vacancies:vacancy-detail", args=(1,))))
        responses.append(client.get(reverse("users:favorites-list")))
        responses.append(client.get(reverse("users:favorites-detail", args=(1,))))
        responses.append(client.post(reverse("users:favorite", args=(2,))))
        responses.append(client.get(reverse("vacancies:search", args=(1,))))

        for response in responses:
            with self.subTest(response):
                self.assertEqual(
                    response.status_code, status.HTTP_200_OK, "Что-то не так"
                )

    def test_delete_endpoints(self):
        client = APIClient()
        responses = []
        responses.append(client.delete(reverse("users:favorite", args=(2,))))

        for response in responses:
            with self.subTest(response):
                self.assertEqual(
                    response.status_code, status.HTTP_204_NO_CONTENT, "Что-то не так"
                )
