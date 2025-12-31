from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Shopify AI Analytics Service")

app.include_router(router)