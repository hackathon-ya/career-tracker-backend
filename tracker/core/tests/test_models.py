from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient, APIRequestFactory

from core.models import City, Forms_of_employment, Work_arrangements
from users.models import Candidate, Favorites, Recruiter
from users.views import CandidateViewSet
from vacancies.views import MatchCandidateViewSet
from vacancies.models import Vacancy


User = get_user_model()
fake = Faker()


class ModelTest(TestCase):
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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        candidate = ModelTest.candidate
        recruiter = ModelTest.recruiter
        vacancy = ModelTest.vacancy
        test_models = [
            (candidate, f"{candidate.first_name} {candidate.last_name}"),
            (recruiter, f"{recruiter.first_name} {recruiter.last_name}"),
            (vacancy, vacancy.job_title),
        ]

        for model, expected_value in test_models:
            with self.subTest(model=model):
                self.assertEqual(str(model), expected_value, "Что-то не так")


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

        request = factory.get('/candidates/')
        view = CandidateViewSet.as_view({'get': 'list'})
        responses.append(view(request))

        request = factory.get('candidates/<int:pk>')
        view = CandidateViewSet.as_view({'get': 'retrieve'})
        responses.append(view(request, pk=ViewSetTestCase.candidate.pk))

        request = factory.get('vacancies/<int:pk>/candidates/')
        view = MatchCandidateViewSet.as_view({'get': 'list'})
        responses.append(view(request, pk=ViewSetTestCase.candidate.pk))

        for response in responses:
            with self.subTest(response):
                self.assertEqual(response.status_code, 200, "Что-то не так")


from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import Candidate, Favorites
from users.views import APIAddFavorite

class APIAddFavoriteTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username="recruiter")
        self.candidate = Candidate.objects.create(name="Test Candidate")

    def test_add_favorite(self):
        client = APIClient()
        client.force_authenticate(user=self.recruiter)

        url = reverse('add-favorite', args=[self.candidate.pk])
        response = client.post(url)

        # Verify the response status code
        self.assertEqual(response.status_code, 200)

        # Verify that the favorite was created
        self.assertTrue(Favorites.objects.filter(candidate=self.candidate, recruiter=self.recruiter).exists())

    def test_remove_favorite(self):
        # Create a favorite
        Favorites.objects.create(candidate=self.candidate, recruiter=self.recruiter)

        client = APIClient()
        client.force_authenticate(user=self.recruiter)

        url = reverse('remove-favorite', args=[self.candidate.pk])
        response = client.delete(url)

        # Verify the response status code
        self.assertEqual(response.status_code, 204)

        # Verify that the favorite was removed
        self.assertFalse(Favorites.objects.filter(candidate=self.candidate, recruiter=self.recruiter).exists())

