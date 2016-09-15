## to copy and paste only TODO: find out how to run .py directly

from documents.models import UserDocument
from users.models import User
user=User.objects.first()
from transactions.models import Transaction, DocumentType
transaction = Transaction.objects.first()

UserDocument.objects.create_doc(user=user, doc_type="Passport", version="v0", transaction=transaction, document_filename="filename", document_image="image")