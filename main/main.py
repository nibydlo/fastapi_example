from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List

from dbservice import UnknownUserException
from service import Service
from utils import check_city, check_day_from_now


class Response(BaseModel):
    code: int
    message: str
    recommendations: List[int]


app = FastAPI()

main_service = Service()


@app.get("/recommendations", response_model=Response)
def get_recs(uid: int, city: str = 'spb', day_from_today: int = 1):

    if not check_city(city):
        return Response(code=status.HTTP_400_BAD_REQUEST, message='city is not supported: ' + city, recommendations=[])

    if not check_day_from_now(day_from_today):
        return Response(code=status.HTTP_400_BAD_REQUEST, message='support only 30 days from today', recommendations=[])
    try:
        recs = main_service.get_recommendation_for_uid(uid, city, day_from_today)
        return Response(code=status.HTTP_200_OK, message='ok', recommendations=recs)
    except UnknownUserException:
        return Response(code=status.HTTP_400_BAD_REQUEST, message='unknown user: ' + str(uid), recommendations=[])
