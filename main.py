import time
from csv import reader, writer
from xml.etree.ElementTree import Element, tostring

from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from starlette.requests import Request
from xmljson import badgerfish as bf

from src.estimator import estimator

app = FastAPI()


class Region(BaseModel):
    name: str
    avgAge: int
    avgDailyIncomeInUSD: float
    avgDailyIncomePopulation: float


class RequestData(BaseModel):
    region: Region
    periodType: str
    timeToElapse: int
    reportedCases: int
    population: int
    totalHospitalBeds: int


def append_request_log_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj, delimiter='\t')
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def record_performance_logs(func):
    def wrapper(request: Request, body: RequestData, response: Response):
        start_time = time.perf_counter()
        result = func(request, body, response)
        execution_time = f'{(time.perf_counter() - start_time) * 1000 :0.2f} ms'
        log = [request.method, request.url.path,
               response.status_code, execution_time]
        append_request_log_as_row('request_logs.csv', log)
        return result
    return wrapper


@app.post('/api/v1/on-covid-19/')
@app.post('/api/v1/on-covid-19/json')
@app.post('/api/v1/on-covid-19/xml')
@record_performance_logs
def estimate_covid_19(request: Request, body: RequestData, response: Response):
    result = estimator(body.dict())
    response.status_code = status.HTTP_200_OK
    if request.url.path.endswith('xml'):
        result = bf.etree(result, root=Element('xml'))
        result = tostring(result)
        return Response(content=result, media_type="application/xml")
    return JSONResponse(content=result, media_type="application/json")


@app.get('/api/v1/on-covid-19/logs')
def endpoint_logs():
    with open('request_logs.csv', 'r') as csv_obj:
        csv_reader = reader(csv_obj)
        text = ''
        for row in csv_reader:
            text += '\t'.join(row)
            text += '\n'
        text = text.replace('\t', '\t\t')
    return PlainTextResponse(text)
