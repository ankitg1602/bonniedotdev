import pytest


@pytest.mark.usefixtures("test_client")
@pytest.mark.usefixtures("load_db_data")
def test_courses_route(db_session, load_db_data, test_client):
    response = test_client.get("/api/courses")
    course_titles = [course.title for course in response.json]

    assert course_titles == ["Awesome Course", "Simple Course"]
