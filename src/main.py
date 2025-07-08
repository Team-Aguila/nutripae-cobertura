# pae_cobertura/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routes.departments import router as departments_router
from routes.towns import router as towns_router
from routes.institutions import router as institutions_router
from routes.campus import router as campuses_router
from routes.parametrics import router as parametrics_router
from routes.beneficiary import router as beneficiary_router
from routes.coverage import router as coverage_router
from core.config import settings
from utils import PrometheusMiddleware, metrics, setting_otlp
import uvicorn
import logging

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API de Recursos Humanos PAE",
        version="1.0.0",
        description="Backend para la gestión del personal y su disponibilidad.",
        routes=app.routes,
    )
    
    # Define the security scheme for JWT Bearer tokens
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token obtained from the NutriPAE-AUTH service /auth/login endpoint"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema para gestionar la estructura geográfica y de beneficiarios del PAE.",
    version="1.0.0"
)

app.add_middleware(PrometheusMiddleware, app_name=settings.APP_NAME)
app.add_route("/metrics", metrics)
# Setting OpenTelemetry exporter
setting_otlp(app, settings.APP_NAME, settings.OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
# Set custom OpenAPI schema
app.openapi = custom_openapi

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(beneficiary_router, prefix=settings.API_PREFIX_STR, tags=["Beneficiaries"])
app.include_router(campuses_router, prefix=settings.API_PREFIX_STR, tags=["Campuses"])
app.include_router(coverage_router, prefix=settings.API_PREFIX_STR, tags=["Coverages"])
app.include_router(departments_router, prefix=settings.API_PREFIX_STR, tags=["Departments"])
app.include_router(institutions_router, prefix=settings.API_PREFIX_STR, tags=["Institutions"])
app.include_router(towns_router, prefix=settings.API_PREFIX_STR, tags=["Towns"])
app.include_router(parametrics_router, prefix=settings.API_PREFIX_STR, tags=["Parametrics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the PAE Coverage API"}

if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)