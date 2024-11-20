import uuid
from app.services.api_key_service.database_service.database_service import (
    DatabaseService,
)
from pocketbase.models.record import Record
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi_login import LoginManager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.services.api_key_service.helpers.api_key_generation import (
    create_api_key,
    verify_api_key,
)


class ApiKeyManager:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def generate_api_key(self, org_id, key_name):
        api_key, hashed_key = create_api_key()
        self.db_service.set_api_key(org_id, hashed_key, key_name)
        return api_key

    def verify_api_key(self, incoming_key):
        stored_hash = self.db_service.get_api_key_by_hash(incoming_key)

        if not stored_hash:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
            )

        if not verify_api_key(incoming_key, stored_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
            )
        return True

    def fetch_api_key(self, org_id, key_name):
        return self.db_service.get_api_key(org_id, key_name)

    def create_organization(self, org_name, admin_id):
        return self.db_service.create_organization(org_name, admin_id)

    def add_user_to_organization(self, org_id, user_email):
        return self.db_service.add_user_to_organization(org_id, user_email)

    def get_organization(self, org_id, user_id):
        return self.db_service.get_organization(org_id, user_id)

    def get_organizations(self, user_email):
        return self.db_service.get_organizations(user_email)

    def get_api_keys(self, org_id):
        return self.db_service.get_api_keys(org_id)

    def delete_user_from_organization(self, org_id, user_email):
        return self.db_service.delete_user_from_organization(org_id, user_email)

    def delete_organization(self, org_id, admin_email):
        return self.db_service.delete_organization(org_id, admin_email)
