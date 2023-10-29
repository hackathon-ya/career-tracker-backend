from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient, APIRequestFactory

from core.models import City, Forms_of_employment, Work_arrangements
from users.models import Candidate, Favorites, Recruiter
from users.views import CandidateViewSet
from vacancies.views import MatchCandidateViewSet
from vacancies.models import Vacancy

fake = Faker()


class ViewSetTestCase(TestCase):
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

    def test_candidates(self):
        factory = APIRequestFactory()
        responses = []

        request = factory.get("/candidates/")
        view = CandidateViewSet.as_view({"get": "list"})
        responses.append(view(request))

        request = factory.get("candidates/<int:pk>")
        view = CandidateViewSet.as_view({"get": "retrieve"})
        responses.append(view(request, pk=ViewSetTestCase.candidate.pk))

        request = factory.get(reverse("vacancies:search", args=(1,)))
        view = MatchCandidateViewSet.as_view()
        responses.append(view(request, pk=ViewSetTestCase.candidate.pk))

        for response in responses:
            with self.subTest(response):
                self.assertEqual(response.status_code, 200, "Что-то не так")


class APIAddFavoriteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.recruiter = Recruiter.objects.create_user(
            username=fake.user_name(),
        )
        cls.candidate = Candidate.objects.create(
            username=fake.user_name(),
        )
        cls.favorite = Favorites.objects.create(
            candidate=cls.candidate, recruiter=cls.recruiter
        )

    def test_add_favorite(self):
        client = APIClient()
        client.force_authenticate(user=self.recruiter)

        url = reverse("users:favorite", args=[APIAddFavoriteTestCase.candidate.pk])
        response = client.post(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Favorites.objects.filter(
                candidate=self.candidate, recruiter=self.recruiter
            ).exists()
        )

    def test_remove_favorite(self):
        client = APIClient()
        client.force_authenticate(user=self.recruiter)

        url = reverse("users:favorite", args=[self.candidate.pk])
        response = client.delete(url)

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Favorites.objects.filter(
                candidate=self.candidate, recruiter=self.recruiter
            ).exists()
        )
