"""tests"""
from asyncio import sleep as asleep
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.main import HeaderReporter, app

tc = TestClient(app)


def test_fastapi_routes():
    """basic tests of all routes and methods"""
    response = tc.get("/1234")
    assert response.status_code == 200

    response = tc.put("/1234")
    assert response.status_code == 200

    response = tc.post("/1234")
    assert response.status_code == 200

    response = tc.get("/1234/abcd")
    assert response.status_code == 200

    response = tc.put("/1234/abcd")
    assert response.status_code == 200

    response = tc.post("/1234/abcd")
    assert response.status_code == 200

    response = tc.get("/1234/abcd/asdfg")
    assert response.status_code == 200

    response = tc.put("/1234/abcd/asdfg")
    assert response.status_code == 200

    response = tc.post("/1234/abcd/asdfg")
    assert response.status_code == 200

    response = tc.get("/1234/asdafa/asda")
    assert response.status_code == 200

    response = tc.put("/1234/asdafa/asda")
    assert response.status_code == 200

    response = tc.post("/1234/asdafa/asda")
    assert response.status_code == 200

    response = tc.get("/")
    assert response.status_code == 200

    response = tc.get("/recent_calls")
    assert response.status_code == 200

    response = tc.post("/recent_calls")
    assert response.status_code == 201


class MockRequest(BaseModel):
    """
    Class to mock incoming requests
    """

    headers: dict
    method: str
    url: str
    query_params: list = Field(default_factory=list)
    cookies: dict = Field(default_factory=dict)

    async def body(self):
        """
        mock body
        :return:
        """
        return "BODY CONTENTS"


def _get_mock_request():
    """helper to create mock requests"""
    return MockRequest(
        **{
            "headers": {"header1": 1, "header2": 2},
            "method": "POST",
            "url": "request.url",
        }
    )


async def test_header_reporter_clean_old():
    """
    test for iterating over existing items in list and removing aged ones.
    :return:
    """

    h_r = HeaderReporter()
    new_req = _get_mock_request()
    old_req = _get_mock_request()
    await h_r.add_call(new_req, filename="test_new")
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=5),
    )
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=3),
    )
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=8),
    )
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=5),
    )
    await h_r.add_call(new_req, filename="test_new")
    assert len(h_r.recent_records) == 6

    h_r.clean_old_records()

    assert len(h_r.recent_records) == 3


async def test_header_reporter_reset():
    """
    Test for reseting stored incoming calls.
    :return:
    """
    h_r = HeaderReporter()
    new_req = _get_mock_request()
    old_req = _get_mock_request()
    await h_r.add_call(new_req, filename="test_new")
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=5),
    )
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=3),
    )
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=8),
    )
    await h_r.add_call(
        old_req,
        filename="test_old",
        created_time=datetime.utcnow() - timedelta(hours=5),
    )
    await h_r.add_call(new_req, filename="test_new")
    assert len(h_r.recent_records) == 6

    h_r.reset_stored()

    assert len(h_r.recent_records) == 0


async def test_header_reporter_created_time():
    """
    Test for correct created time for stored incoming calls.
    :return:
    """
    h_r = HeaderReporter()
    new_req = _get_mock_request()
    await h_r.add_call(new_req, filename="test_1")
    await asleep(1)
    await h_r.add_call(new_req, filename="test_2")
    assert h_r.recent_records[0]["created_time"] > h_r.recent_records[1]["created_time"]


if __name__ == "__main__":
    import asyncio
    import os

    os.chdir("../app")
    test_fastapi_routes()

    asyncio.run(test_header_reporter_clean_old())
    asyncio.run(test_header_reporter_reset())
    asyncio.run(test_header_reporter_created_time())
