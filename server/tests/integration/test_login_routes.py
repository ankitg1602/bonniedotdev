import pytest


@pytest.mark.usefixtures("test_client")
@pytest.mark.usefixtures("load_db_data")
@pytest.mark.parametrize(
    ["username", "password", "expected_response"],
    [
        # valid user/password
        ("admin", "abc123", True),
        # invalid password
        ("admin", "wrong", False),
        # nonexistent user
        ("not_admin", "abc123", False),
    ],
)
def test_valid_login(
    db_session,
    test_client,
    load_db_data,
    username,
    password,
    expected_response,
):
    print("starting login test")

    response = test_client.get(
        "/api/login",
        json={"username": username, "password": password},
    )

    print("ending login test")

    assert response.json["valid"] == expected_response
