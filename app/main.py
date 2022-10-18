"""
App to listen to incoming calls and gather information about incoming traffic.
v 0.0.0
"""

from collections import deque
from datetime import datetime, timedelta
from typing import List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates/")


app = FastAPI(openapi_url="")


class HeaderReporter:
    """
    Class to hold recent call data
    """

    def __init__(self):
        self.recent_records = deque(maxlen=10)

    async def add_call(
        self,
        request: Request,
        filename: str,
        created_time: datetime = None,
    ):
        """
        Parse and add incoming calls to deque

        :param created_time:
        :param request:
        :param filename:
        :return:
        """
        if created_time is None:
            created_time = datetime.utcnow()

        last_call = {
            "created_time": created_time,
            "headers": request.headers,
            "method": request.method,
            "body": await request.body(),
            "file": filename,
            "url": request.url,
            "params": request.query_params,
            "cookies": request.cookies,
        }

        self.recent_records.appendleft(last_call)

    def get_stored(self) -> List[dict]:
        """
        Returns content of deque in as list.
        :return:
        """
        return list(self.recent_records)

    def clean_old_records(self, hours: int = 4):
        """
        Iterates current records and removes records that are older than hours.
        :param hours:
        :return:
        """
        now = datetime.utcnow()
        remove = []
        for record in self.recent_records:
            if now - record["created_time"] > timedelta(hours=hours):
                remove.append(record)
        for record in remove:
            self.recent_records.remove(record)

    def reset_stored(self):
        """
        Clears stored records.
        :return:
        """
        self.recent_records = deque(maxlen=10)


header_reporter = HeaderReporter()


@app.get("/", status_code=200, include_in_schema=False)
async def listening():
    """
    Simple health check.
    :return:
    """
    return "Listening!"


@app.get(
    "/recent_calls",
    status_code=200,
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def get_recent_calls(request: Request):
    """
    User-friendly display of data from last 10 calls.

    :param request:
    :return:
    """
    header_reporter.clean_old_records()

    return templates.TemplateResponse(
        "return_last.html",
        {"request": request, "recent_calls": header_reporter.get_stored()},
    )


@app.post("/recent_calls", status_code=201, include_in_schema=False)
async def reset_recent_calls():
    """
    Reset records.

    :param request:
    :return:
    """
    header_reporter.reset_stored()

    return


@app.get("/{filename}", status_code=200, include_in_schema=False)
async def get_one_level(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.post("/{filename}", status_code=200, include_in_schema=False)
async def post_one_level(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.put("/{filename}", status_code=200, include_in_schema=False)
async def put_one_level(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.get("/{level_one}/{filename}", status_code=200, include_in_schema=False)
async def get_two_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.post("/{level_one}/{filename}", status_code=200, include_in_schema=False)
async def post_two_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.put("/{level_one}/{filename}", status_code=200, include_in_schema=False)
async def put_two_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.get(
    "/{level_one}/{level_two}/{filename}", status_code=200, include_in_schema=False
)
async def get_three_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.post(
    "/{level_one}/{level_two}/{filename}", status_code=200, include_in_schema=False
)
async def post_three_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.put(
    "/{level_one}/{level_two}/{filename}", status_code=200, include_in_schema=False
)
async def put_three_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.get(
    "/{level_one}/{level_two}/{level_three}/{filename}",
    status_code=200,
    include_in_schema=False,
)
async def get_four_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.post(
    "/{level_one}/{level_two}/{level_three}/{filename}",
    status_code=200,
    include_in_schema=False,
)
async def post_four_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


@app.put(
    "/{level_one}/{level_two}/{level_three}/{filename}",
    status_code=200,
    include_in_schema=False,
)
async def put_four_levels(request: Request, filename: str):
    """
    Listener to lift call data.
    :param request:
    :param filename:
    :return:
    """
    await header_reporter.add_call(request, filename)
    return filename


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8008, log_level="info")
