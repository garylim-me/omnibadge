# Created for REST APIs
# Doc:

from rest_framework import serializers
from .models import Transaction


class TransactionCreateSerializer(serializers.Serializer):

    email = serializers.EmailField()
    # TODO: change go company object and company serializer?
    company_id = serializers.IntegerField()
    version = serializers.CharField(max_length=30)

    # TODO: Add document type objects and serializer?
    # document_types = DocumentTypeSerializer(many=True)  # A nested list of 'document_type' items.

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            email=validated_data['email'],
            company_id=validated_data['company_id'],
            version=validated_data['version'],  # TODO: document_type=None
        )

        # TODO: Better fix needed. This is a hack to add transaction_id into the returned results
        self.validated_data['transaction_id'] = transaction.id

        return transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'ui_type', 'transaction_token', 'js_result', 'date_created', 'user', )  # temp removal TODO: 'service',

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