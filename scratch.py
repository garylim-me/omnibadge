## to copy and paste only TODO: find out how to run .py directly

# GENERIC START UP SHELL
from documents.models import UserDocument, DocPassport
from users.models import User, SessionToken, Privilege
from transactions.models import Transaction, DocumentType, TransactionToken
from companies.models import Company


transaction = Transaction.objects.first()

# for test case
UserDocument.objects.create(email="user@omnibadge.com", doc_type="Passport", version="v0", transaction_id="1", document_filename="filename", document_image="image")


# ==== CREATE USER ====

from django.contrib.auth.models import User
user = User.objects.create_user(email='merchant2@omnibadge.com', password='passpass')


# ==== CURL POST REQUESTS ====

# user POST:
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email":"user3@omnibadge.com", "first_name":"third", "last_name":"last", "phone":"123", "is_active":"False"}' http://api.127.0.0.1.xip.io:8000/users/

# document POST:
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "user@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "4", "document_filename": "filename", "document_image": "image"}' http://api.127.0.0.1.xip.io:8000/documents/

# GET Api token with POST:
curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username": "admin@omnibadge.com", "password": "passpass"}' http://api.127.0.0.1.xip.io:8000/api-token-auth/
curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username": "admin@omnibadge.com", "password": "passpass"}' http://127.0.0.1:8000/users/api-token-auth/

# document details GET (with login credentials):
curl -v -u "admin:passpass" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://api.127.0.0.1.xip.io:8000/documents/34/

# document details GET (with session_token):
curl -v -H "Authorization: session_token 318997a7c199e2ab29d738a823d904a2c41829e7" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://api.127.0.0.1.xip.io:8000/documents/50/

# transaction POST (with session_token):
curl -v -H "Authorization: session_token 318997a7c199e2ab29d738a823d904a2c41829e7" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "usernew@omnibadge.com", "company_id": "1", "version": "v0"}' http://api.127.0.0.1.xip.io:8000/transactions/

curl -H "Authorization: session_token 318997a7c199e2ab29d738a823d904a2c41829e7" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "user@omnibadge.com", "company_id": "1", "version": "v0"}' http://127.0.0.1:8000/transactions/api/


# transaction GET (with COMPANY session_token):
curl -H "Authorization: session_token 3b3ee95e36ad0de4e434daeb9ee2d45d82730230" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://127.0.0.1:8000/transactions/api/

# Test user (w/o any privileges) retrieve transactions: session_token_test_user

curl -H "Authorization: session_token session_token_test_user2" -H "Accept: application/json" -H "Content-type: application/json" -X GET http://127.0.0.1:8000/transactions/api/


# test document details
curl -v -H "Authorization: session_token 3b3ee95e36ad0de4e434daeb9ee2d45d82730230" -H "Accept: application/json" -H "Content-type: application/json" GET http://127.0.0.1:8000/documents/api/36/

# test with different company token
curl -v -H "Authorization: session_token 318997a7c199e2ab29d738a823d904a2c41829e7" -H "Accept: application/json" -H "Content-type: application/json" GET http://127.0.0.1:8000/documents/api/36/

# document post NEW (but different transaction id)
curl -v -H "Authorization: session_token 3b3ee95e36ad0de4e434daeb9ee2d45d82730230" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "reguser@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "4", "document_filename": "filename", "document_image": "image", "transaction_token": "38f98ea41031322e05e105bd5696891ae966d347"}' http://api.127.0.0.1.xip.io:8000/documents/

# document post NEW, with different company session token and transaction token (SHOULD FAIL)
curl -v -H "Authorization: session_token 318997a7c199e2ab29d738a823d904a2c41829e7" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "reguser@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "4", "document_filename": "filename", "document_image": "image", "transaction_token": "	ed1e9d918399100832b9aa1261b78b5025d1f528"}' http://api.127.0.0.1.xip.io:8000/documents/

# document post NEW, with same session, but different company transaction token (SHOULD FAIL)
curl -v -H "Authorization: session_token 3b3ee95e36ad0de4e434daeb9ee2d45d82730230" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "reguser@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "4", "document_filename": "filename", "document_image": "image", "transaction_token": "	ed1e9d918399100832b9aa1261b78b5025d1f528"}' http://api.127.0.0.1.xip.io:8000/documents/

# document post NEW (but wrong email)
curl -v -H "Authorization: session_token 3b3ee95e36ad0de4e434daeb9ee2d45d82730230" -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "reguse1r@omnibadge.com", "doc_type": "Passport", "version": "v0", "transaction_id": "4", "document_filename": "filename", "document_image": "image", "transaction_token": "38f98ea41031322e05e105bd5696891ae966d347"}' http://api.127.0.0.1.xip.io:8000/documents/