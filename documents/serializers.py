# Created for REST APIs
# Doc: http://www.django-rest-framework.org/api-guide/serializers/

from rest_framework import serializers
from .models import DocPassport, UserDocument


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocPassport
        fields = ('date_created', 'version', 'verified', 'date_verified', 'transaction', 'owner', 'document_type')

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Transaction` instance, given the validated data.
    #     """
    #     instance.ui_type = validated_data.get('ui_type', instance.ui_type)
    #     instance.save()
    #     return instance


# All Document GET/POSTs should pass thru this!!
class UserDocumentSerializer(serializers.ModelSerializer):

    # This is a roundabout way -- it's not extracting the document type from the base table
    # http://stackoverflow.com/questions/31289122/how-to-pull-nested-fields-out-when-serializing-django-rest-framework
    document_type = serializers.CharField(source='document_object.document_type.name')

    # Extracting document fields
    # TODO: improvements needed here to dynamically include all fields of document subtypes
    # TODO: need to write some model-based serializers and have the model output its serialized data itself
    document_object = DocumentSerializer()

    class Meta:
        model = UserDocument
        # Note that "document_id" is the hidden id of the other table. Hence not displayed to public.
        fields = ('id', 'user', 'document_type', 'document_object')

    def create(self, validated_data):
        """
        Create and return a new `Transaction` instance, given the validated data.
        """
        print "CREATE RUN!"
        return UserDocument.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Transaction` instance, given the validated data.
        """
        instance.document_type = validated_data.get('document_type', instance.document_type)
        instance.save()
        return instance


class CreateDocumentSerializer(serializers.Serializer):

    # TODO: need to record document creator too
    # http://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # creator_id = serializers.SerializerMethodField(source='creator.id')
    # creator_id = serializers.ReadOnlyField(source='creator.id')
    email = serializers.CharField(max_length=120)
    doc_type = serializers.CharField(max_length=10)
    version = serializers.CharField(max_length=10)
    transaction_id = serializers.IntegerField()
    document_filename = serializers.CharField(required=False, allow_blank=True, max_length=100)
    document_image = serializers.CharField(required=False, allow_blank=True, max_length=100)

    # class Meta:
    #     # TODO:
    #     # model = Document
    #     fields = ("email", "doc_type", "version", "transaction_id", "document_filename", "document_image")

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        # TODO: Better fix needed. This is a hack to add creator_id into the validated_data to create doc
        # self.validated_data['creator_id'] = self.creator.id

        # print 'ACTUAL CREATE TRIGGERED!!'
        user_doc = UserDocument.objects.create(**validated_data)

        # TODO: Better fix needed. This is a hack to add document_id into the returned results
        self.validated_data['document_id'] = user_doc.id
        return user_doc

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance