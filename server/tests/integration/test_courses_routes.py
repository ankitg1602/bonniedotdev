import pytest


@pytest.mark.usefixtures("test_client")
def test_courses_route(db_session, test_client):
    response = test_client.get("/api/courses")
    course_titles = [course.title for course in response.json]

    assert course_titles == ["Awesome Course", "Simple Course"]
