import pytest

@pytest.mark.web
def test_get_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hesap Makinesi" in response.data

@pytest.mark.web
def test_post_add(client):
    data = {"operation": "add", "first_number": "10", "second_number": "5"}
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"10 + 5 = 15" in response.data

@pytest.mark.web
def test_post_divide_by_zero(client):
    data = {"operation": "divide", "first_number": "10", "second_number": "0"}
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert "Sıfıra bölme hatası".encode("utf-8") in response.data

@pytest.mark.web
def test_post_invalid_input(client):
    data = {"operation": "add", "first_number": "abc", "second_number": "5"}
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert "Hatalı giriş".encode("utf-8") in response.data
