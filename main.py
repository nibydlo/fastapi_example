from datetime import date
from fastapi import FastAPI

from service import get_recommendation_for_uid

app = FastAPI()


@app.get("/recommendations/")
def get_hardcoded_value(uid: int = -1, date_for_search: date = date.today()):
    return {
        'recommendations': get_recommendation_for_uid(uid, date_for_search)
    }
