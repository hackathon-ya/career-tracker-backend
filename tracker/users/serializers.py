from rest_framework import serializers

from .models import Candidate


# class RecruiterSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Recruiter
#         fields = ('id', 'username', 'password')
#         ref_name = 'ReadOnlyUsers'
#         extra_kwargs = {'password': {'write_only': True}}


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('date_joined',)
        model = Candidate
