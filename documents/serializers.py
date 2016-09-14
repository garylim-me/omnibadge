# Created for REST APIs
# Doc:

from rest_framework import serializers
from .models import DocPassport


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocPassport
        fields = ('id', 'date_created', 'version', 'verified', 'date_verified', 'transaction', 'user', 'document_type')

    def create(self, validated_data):
        """
        Create and return a new `Transaction` instance, given the validated data.
        """
        return DocPassport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Transaction` instance, given the validated data.
        """
        instance.ui_type = validated_data.get('ui_type', instance.ui_type)
        instance.save()
        return instance
