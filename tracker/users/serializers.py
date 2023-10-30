from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Candidate, Favorites


class CandidateSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    status_from_kt = serializers.StringRelatedField()
    education = serializers.StringRelatedField()
    education_YP = serializers.StringRelatedField()
    form_of_employment = serializers.StringRelatedField(many=True)
    work_arrangement = serializers.StringRelatedField(many=True)
    skills = serializers.StringRelatedField(many=True)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    date_of_birth = serializers.DateField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        exclude = (
            "date_joined",
            "groups",
            "user_permissions",
            "is_superuser",
            "password",
            "username",
            "is_active",
            "is_staff",
        )
        model = Candidate

    def get_is_favorite(self, obj):
        recruiter = get_user_model().objects.first()
        if Favorites.objects.filter(candidate=obj, recruiter=recruiter).exists():
            return True
        return False

    def to_representation(self, instance):
        recruiter = get_user_model().objects.first()
        representation = super().to_representation(instance)
        representation["recruiter"] = recruiter.username if recruiter else None
        return representation
