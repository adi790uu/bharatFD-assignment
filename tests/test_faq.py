from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.deps import get_db
from app.core.config import settings
import pytest
import httpx

engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=5,
    pool_recycle=3600,
    pool_timeout=60,
)

TestingAsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def override_get_db():
    async with TestingAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["success"]


@pytest.mark.asyncio
async def test_create_faq():
    response = client.post(
        "/api/faqs/create",
        json={
            "question": "Test Question",
            "answer": "Test Answer",
            "language": "en",
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_faqs():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=None
    ) as client:
        response = await client.get("/api/faqs/?lang=en")
        assert response.status_code == 200
        assert response.json()["success"]
        assert isinstance(response.json()["data"]["faqs"], list)


@pytest.mark.asyncio
async def test_delete_nonexistent_faq():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=None
    ) as client:
        response = await client.delete("/api/faqs/delete?faq_id=99999")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_faq():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=None
    ) as client:
        create_response = await client.post(
            "/api/faqs/create",
            json={
                "question": "Delete Test Question",
                "answer": "Delete Test Answer",
                "language": "en",
            },
        )
        assert create_response.status_code == 201

        faq_id = create_response.json()["data"]["id"]

        delete_response = await client.delete(
            f"/api/faqs/delete?faq_id={faq_id}",
        )
        assert delete_response.status_code == 200
        assert delete_response.json()["success"] is True

        get_response = await client.get("/api/faqs/?lang=en")
        faqs = get_response.json()["data"]["faqs"]
        assert all(faq["id"] != faq_id for faq in faqs)


@pytest.mark.asyncio
async def test_random_language_support():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=None
    ) as client:
        response = await client.post(
            "/api/faqs/create",
            json={
                "question": "Test Question",
                "answer": "Test Answer",
                "language": "random",
            },
        )

        assert response.status_code == 400
