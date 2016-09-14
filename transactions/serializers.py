# Created for REST APIs
# Doc:

from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'ui_type', 'transaction_token', 'js_result', 'date_created', 'user', 'service')

    # Not sure if needed:
    def create(self, validated_data):
        """
        Create and return a new `Transaction` instance, given the validated data.
        """
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Transaction` instance, given the validated data.
        """
        instance.ui_type = validated_data.get('ui_type', instance.ui_type)
        instance.save()
        return instance
