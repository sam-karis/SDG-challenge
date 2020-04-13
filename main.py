from xml.etree.ElementTree import Element, tostring

from fastapi import FastAPI
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


@app.post('/api/v1/on-covid-19')
@app.post('/api/v1/on-covid-19/json')
@app.post('/api/v1/on-covid-19/xml')
def estimate_covid_19(request: Request, body: RequestData):
    result = estimator(body.dict())
    if request.url.path.endswith('xml'):
        result = bf.etree(result, root=Element('html'))
        result = tostring(result)
    return result


@app.get('/api/v1/on-covid-19/logs')
def endpoint_logs():
    pass
