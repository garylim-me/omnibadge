## to copy and paste only TODO: find out how to run .py directly

from documents.models import UserDocument
from users.models import User
user=User.objects.first()
from transactions.models import Transaction, DocumentType
transaction = Transaction.objects.first()

UserDocument.objects.create(email="user@omnibadge.com", doc_type="Passport", version="v0", transaction_id="1", document_filename="filename", document_image="image")


# ==== CURL POST REQUESTS ====

# user POST:
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email":"user3@omnibadge.com", "username":"user3", "first_name":"third", "last_name":"last", "phone":"123", "is_active":"False"}' http://api.127.0.0.1.xip.io:8000/users/

# document POST:
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "user@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "4", "document_filename": "filename", "document_image": "image"}' http://api.127.0.0.1.xip.io:8000/documents/

# GET Api token with POST:
curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username": "admin", "password": "passpass"}' http://api.127.0.0.1.xip.io:8000/api-token-auth/
curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username": "admin", "password": "passpass"}' http://127.0.0.1:8000/users/api-token-auth/

# document details GET (with login credentials):
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://api.127.0.0.1.xip.io:8000/documents/34/

# document details GET (with Auth token):
curl -v -H "Authorization: Token dde1831364fe97ac3dcdcc4412602e9c8ebf942e" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://api.127.0.0.1.xip.io:8000/documents/34/


# transaction POST (with Auth token):
curl -v -H "Authorization: Token 8a4154ad02448d8b2fad847d556bc22848fe0e43" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "user@omnibadge.com", "company_id": "1", "version": "v0"}' http://api.127.0.0.1.xip.io:8000/transactions/

curl -H "Authorization: Token 8a4154ad02448d8b2fad847d556bc22848fe0e43" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "user@omnibadge.com", "company_id": "1", "version": "v0"}' http://127.0.0.1:8000/transactions/api/




# Test user (w/o any privileges) retrieve transactions: session_token_test_user

curl -H "Authorization: Token session_token_test_user2" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://127.0.0.1:8000/transactions/api/