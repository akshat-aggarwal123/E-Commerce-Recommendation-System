from fastapi import FastAPI
from .api.v1.endpoints import recommendations

app = FastAPI()

# Include API routers
app.include_router(recommendations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recommendation Engine API"}