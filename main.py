from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_hardcoded_value():
    return {'hardcoded': 'value'}