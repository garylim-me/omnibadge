# Created for REST APIs
# Doc:

from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'white_label', 'is_active', 'date_registered', )

    def create(self, validated_data):
        """
        Create and return a new `Company` instance, given the validated data.
        """
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Company` instance, given the validated data.
        """
        instance.ui_type = validated_data.get('ui_type', instance.ui_type)
        instance.save()
        return instance
