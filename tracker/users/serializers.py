from rest_framework import serializers

from .models import Candidate


# class RecruiterSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Recruiter
#         fields = ('id', 'username', 'password')
#         ref_name = 'ReadOnlyUsers'
#         extra_kwargs = {'password': {'write_only': True}}


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
