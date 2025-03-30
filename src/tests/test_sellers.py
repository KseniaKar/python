import pytest
from fastapi import status
from src.models.seller import Seller
from sqlalchemy import select

# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(db_session, async_client):
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "e_mail": "alice@example.com",
        "password": "123456",
    }
    response = await async_client.post("/api/v1/seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()
    resp_seller_id = result_data.pop("id", None)
    assert resp_seller_id, "Seller id not returned from endpoint"

    assert result_data == {
        "first_name": "Alice",
        "last_name": "Smith",
        "e_mail": "alice@example.com",
    }

# Тест на ручку получения списка продавцов (если такая ручка будет добавлена)
# Здесь ручка /api/v1/seller/ должна возвращать список — если она пока не реализована, можно временно закомментировать

@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = Seller(
        first_name="Alice",
        last_name="Smith",
        e_mail="alice@example.com",
        password="123456"
    )
    seller_2 = Seller(
        first_name="Bob",
        last_name="Johnson",
        e_mail="bob@example.com",
        password="654321"
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK
    sellers = response.json()["sellers"]
    assert len(sellers) == 2

    emails = [s["e_mail"] for s in sellers]
    assert "alice@example.com" in emails
    assert "bob@example.com" in emails

# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller = Seller(
        first_name="Alice", last_name="Smith", e_mail="alice@example.com", password="123456"
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_200_OK
    result_data = response.json()

    assert result_data["first_name"] == "Alice"
    assert result_data["last_name"] == "Smith"
    assert result_data["e_mail"] == "alice@example.com"

# Тест на ручку обновления продавца
@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = Seller(
        first_name="Alice", last_name="Smith", e_mail="alice@example.com", password="123456"
    )
    db_session.add(seller)
    await db_session.flush()

    updated_data = {
        "first_name": "Alicia",
        "last_name": "Smithe",
        "e_mail": "alicia@example.com",
        "password": "newpassword123",
    }

    response = await async_client.put(f"/api/v1/seller/{seller.id}", json=updated_data)

    assert response.status_code == status.HTTP_200_OK

    updated_seller = await db_session.get(Seller, seller.id)
    assert updated_seller.first_name == "Alicia"
    assert updated_seller.last_name == "Smithe"
    assert updated_seller.e_mail == "alicia@example.com"

# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = Seller(
        first_name="Alice", last_name="Smith", e_mail="alice@example.com", password="123456"
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    deleted_seller = await db_session.get(Seller, seller.id)
    assert deleted_seller is None

# Тест на ручку удаления продавца с несуществующим id
@pytest.mark.asyncio
async def test_delete_seller_with_invalid_id(db_session, async_client):
    response = await async_client.delete(f"/api/v1/seller/999999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
