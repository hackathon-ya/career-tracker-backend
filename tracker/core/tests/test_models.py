from django.test import TestCase
from faker import Faker

from core.models import City, Forms_of_employment, Work_arrangements
from users.models import Candidate, Favorites, Recruiter
from vacancies.models import Vacancy

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
