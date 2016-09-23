from rest_framework import serializers
from .models import Transaction


class TransactionCreateSerializer(serializers.Serializer):

    email = serializers.EmailField()
    # TODO: change go company object and company serializer?
    company_id = serializers.IntegerField()
    version = serializers.CharField(max_length=30)

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            email=validated_data['email'],
            company_id=validated_data['company_id'],
            version=validated_data['version'],  # TODO: document_type=None
        )

        # TODO: Better fix needed. This is a hack to add transaction_id into the returned results
        self.validated_data['transaction_id'] = transaction.id

        return transaction

    # TODO: WIP. Not sure if needed.
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.company_id = validated_data.get('company_id', instance.company_id)
        instance.version = validated_data.get('version', instance.version)
        instance.save()
        return instance


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
