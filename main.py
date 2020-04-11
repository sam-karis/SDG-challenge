from fastapi import FastAPI
from pydantic import BaseModel

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
def estimate_covid_19(body: RequestData):
    result = estimator(body.dict())
    return result
