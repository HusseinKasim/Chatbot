import pytest
from fastapi.TestClient import TestClient
from app import app

client = TestClient(app)