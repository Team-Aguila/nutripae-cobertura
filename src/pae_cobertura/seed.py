import logging
from sqlmodel import Session
from pae_cobertura.database import engine
from pae_cobertura.models import (
    DocumentType,
    Gender,
    Grade,
    EtnicGroup,
    DisabilityType,
    Department,
    Town,
    BenefitType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_data():
    session = Session(engine)
    try:
        # DocumentType
        document_types = [
            "registro de nacimiento",
            "documento de identidad",
            "pasaporte",
            "documento extranjero",
        ]
        for name in document_types:
            if not session.query(DocumentType).filter_by(name=name).first():
                session.add(DocumentType(name=name))
        
        # Gender
        genders = ["masculino", "femenino", "otro"]
        for name in genders:
            if not session.query(Gender).filter_by(name=name).first():
                session.add(Gender(name=name))

        # Grade
        grades = [
            "inicial 0-1 años", "inicial 1-2 años", "inicial 2-3 años",
            "pre-jardín", "jardín", "transición",
            "primero", "segundo", "tercero", "cuarto", "quinto",
            "sexto", "séptimo", "octavo", "noveno",
            "décimo", "once",
        ]
        for name in grades:
            if not session.query(Grade).filter_by(name=name).first():
                session.add(Grade(name=name))
        
        # EtnicGroup
        etnic_groups = [
            "afro", "indígena", "palenquero", "rom", "mestizo", "otro",
        ]
        for name in etnic_groups:
            if not session.query(EtnicGroup).filter_by(name=name).first():
                session.add(EtnicGroup(name=name))

        # DisabilityType
        disability_types = [
            "visual", "auditiva", "motora", "intelectual", "multiple",
        ]
        for name in disability_types:
            if not session.query(DisabilityType).filter_by(name=name).first():
                session.add(DisabilityType(name=name))

        # BenefitType
        benefit_types = ["desayuno", "almuerzo", "refrigerio"]
        for name in benefit_types:
            if not session.query(BenefitType).filter_by(name=name).first():
                session.add(BenefitType(name=name))

        # Departments and Towns
        colombia_data = {
            "Antioquia": ["Medellín", "Bello", "Itagüí", "Envigado", "Rionegro"],
            "Valle del Cauca": ["Cali", "Buenaventura", "Palmira", "Tuluá", "Buga"],
            "Cundinamarca": ["Bogotá", "Soacha", "Girardot", "Zipaquirá", "Fusagasugá"],
            "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Sabanalarga", "Puerto Colombia"],
            "Santander": ["Bucaramanga", "Floridablanca", "Girón", "Piedecuesta", "Barrancabermeja"],
            "Bolívar": ["Cartagena", "Magangué", "El Carmen de Bolívar", "Turbaco", "Arjona"],
            "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá", "Paipa"],
            "Nariño": ["Pasto", "Tumaco", "Ipiales", "Túquerres", "La Unión"],
            "Tolima": ["Ibagué", "Espinal", "Melgar", "Honda", "Líbano"],
            "Norte de Santander": ["Cúcuta", "Ocaña", "Pamplona", "Villa del Rosario", "Los Patios"]
        }

        dept_dane_code = 1
        town_dane_code = 1

        for dept_name, towns in colombia_data.items():
            department = session.query(Department).filter_by(name=dept_name).first()
            if not department:
                department = Department(name=dept_name, dane_code=f"{dept_dane_code:02d}")
                session.add(department)
                session.flush() # To get the ID for the towns
                dept_dane_code += 1

            for town_name in towns:
                if not session.query(Town).filter_by(name=town_name).first():
                    town = Town(name=town_name, dane_code=f"{department.dane_code}{town_dane_code:03d}", department_id=department.id)
                    session.add(town)
                    town_dane_code += 1
        
        session.commit()
        logger.info("Database populated with initial data.")
    except Exception as e:
        logger.error(f"Error populating data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_data() 