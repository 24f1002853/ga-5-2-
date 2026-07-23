from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ProrationRequest(BaseModel):
    old_price: float
    new_price: float
    days_remaining: int
    days_in_actual_month: int
    spec: str


class ProrationResponse(BaseModel):
    charge: float


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/proration", response_model=ProrationResponse)
def calculate_proration(req: ProrationRequest):
    difference = req.new_price - req.old_price

    if req.spec == "v1":
        divisor = 30
    elif req.spec == "v2":
        divisor = req.days_in_actual_month
    else:
        # The assignment only uses v1 and v2, but this prevents server errors.
        divisor = 30

    charge = difference * (req.days_remaining / divisor)

    return {"charge": charge}
