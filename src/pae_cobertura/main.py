# pae_cobertura/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pae_cobertura.routes.departments import router as departments_router
from pae_cobertura.routes.towns import router as towns_router
from pae_cobertura.routes.institutions import router as institutions_router
from pae_cobertura.routes.campus import router as campuses_router
from pae_cobertura.routers.parametrics import router as parametrics_router

app = FastAPI(
    title="API de Cobertura del PAE",
    description="Sistema para gestionar la estructura geográfica y de beneficiarios del PAE.",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir los routers de los endpoints
app.include_router(departments_router, prefix="/api/v1/departments", tags=["Departments"])
app.include_router(towns_router, prefix="/api/v1/towns", tags=["Towns"])
app.include_router(institutions_router, prefix="/api/v1/institutions", tags=["Institutions"])
app.include_router(campuses_router, prefix="/api/v1/campuses", tags=["Campuses"])
app.include_router(parametrics_router, prefix="/api/v1/parametrics", tags=["Parametrics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the PAE Coverage API"}
