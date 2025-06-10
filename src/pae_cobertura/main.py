# pae_cobertura/main.py
from fastapi import FastAPI
from pae_cobertura.routes.departments import router as departments_router
from pae_cobertura.routes.towns import router as towns_router
from pae_cobertura.routes.institutions import router as institutions_router

app = FastAPI(
    title="API de Cobertura del PAE",
    description="Sistema para gestionar la estructura geográfica y de beneficiarios del PAE.",
    version="1.0.0"
)

# Incluir los routers de los endpoints
app.include_router(departments_router, prefix="/api/v1/departments", tags=["Departments"])
app.include_router(towns_router, prefix="/api/v1/towns", tags=["Towns"])
app.include_router(institutions_router, prefix="/api/v1/institutions", tags=["Institutions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the PAE Coverage API"}
