## to copy and paste only TODO: find out how to run .py directly

from documents.models import UserDocument
from users.models import User
user=User.objects.first()
from transactions.models import Transaction, DocumentType
transaction = Transaction.objects.first()

UserDocument.objects.create_doc(email="user@omnibadge.com", doc_type="Passport", version="v0", transaction_id="1", document_filename="filename", document_image="image")


# ==== CURL POST REQUESTS ====

# working user POST:
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email":"user3@omnibadge.com", "username":"user3", "first_name":"third", "last_name":"last", "phone":"123", "is_active":"False"}' http://api.127.0.0.1.xip.io:8000/users/

# document POST:
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "user@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "1", "document_filename": "filename", "document_image": "image"}' http://api.127.0.0.1.xip.io:8000/documents/

