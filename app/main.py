# app/main.py
from fastapi import FastAPI
from app.routers import csv_routes
from app.database.db import Base, engine
from app.routers import auth

app = FastAPI(title="StanTech AI - Assignment(CSV Processing App)")

Base.metadata.create_all(bind=engine)

# Include routers from the `routers` folder
app.include_router(auth.router,tags=["Auth"])
app.include_router(csv_routes.router, prefix="/process_csv", tags=["CSV Processing & Generate Summary Report"])
