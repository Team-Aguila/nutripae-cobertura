import logging
import random
from faker import Faker
from sqlmodel import Session, select
from pae_cobertura.database import engine
from pae_cobertura.models import (
    DocumentType,
    Gender,
    Grade,
    EtnicGroup,
    DisabilityType,
    Department,
    Town,
    BenefitType,
    Institution,
    Campus,
    Beneficiary,
    Coverage
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_data():
    session = Session(engine)
    fake = Faker("es_CO")
    try:
        # DocumentType
        document_types = [
            "registro de nacimiento",
            "documento de identidad",
            "pasaporte",
            "documento extranjero",
        ]
        for name in document_types:
            if not session.exec(select(DocumentType).filter_by(name=name)).first():
                session.add(DocumentType(name=name))

        # Gender
        genders = ["masculino", "femenino", "otro"]
        for name in genders:
            if not session.exec(select(Gender).filter_by(name=name)).first():
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
            if not session.exec(select(Grade).filter_by(name=name)).first():
                session.add(Grade(name=name))

        # EtnicGroup
        etnic_groups = [
            "afro", "indígena", "palenquero", "rom", "mestizo", "otro",
        ]
        for name in etnic_groups:
            if not session.exec(select(EtnicGroup).filter_by(name=name)).first():
                session.add(EtnicGroup(name=name))

        # DisabilityType
        disability_types = [
            "visual", "auditiva", "motora", "intelectual", "multiple",
        ]
        for name in disability_types:
            if not session.exec(select(DisabilityType).filter_by(name=name)).first():
                session.add(DisabilityType(name=name))

        # BenefitType
        benefit_types = ["desayuno", "almuerzo", "refrigerio"]
        for name in benefit_types:
            if not session.exec(select(BenefitType).filter_by(name=name)).first():
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
            department = session.exec(select(Department).filter_by(name=dept_name)).first()
            if not department:
                department = Department(name=dept_name, dane_code=f"{dept_dane_code:02d}")
                session.add(department)
                session.flush() # To get the ID for the towns
                dept_dane_code += 1

            for town_name in towns:
                if not session.exec(select(Town).filter_by(name=town_name)).first():
                    town = Town(name=town_name, dane_code=f"{department.dane_code}{town_dane_code:03d}", department_id=department.id)
                    session.add(town)
                    town_dane_code += 1
        session.commit()

        # Get existing data to create relationships
        towns = session.exec(select(Town)).all()
        document_types = session.exec(select(DocumentType)).all()
        genders = session.exec(select(Gender)).all()
        grades = session.exec(select(Grade)).all()
        etnic_groups = session.exec(select(EtnicGroup)).all()
        disability_types = session.exec(select(DisabilityType)).all()

        # Create Institutions
        fake.unique.clear()
        institutions = session.exec(select(Institution)).all()
        last_institution = session.exec(select(Institution).order_by(Institution.id.desc())).first()
        inst_dane_code = int(last_institution.dane_code[-3:]) + 1 if last_institution else 1

        if len(institutions) < 25:
            for _ in range(25 - len(institutions)):
                town = random.choice(towns)
                name = fake.unique.company()
                if not session.exec(select(Institution).filter_by(name=name)).first():
                    institution = Institution(
                        name=name,
                        dane_code=f"{town.dane_code}{inst_dane_code:03d}",
                        town_id=town.id
                    )
                    session.add(institution)
                    institutions.append(institution)
                    inst_dane_code += 1
            session.commit()
            for institution in institutions:
                session.refresh(institution)


        # Create Campuses
        fake.unique.clear()
        campuses = session.exec(select(Campus)).all()
        last_campus = session.exec(select(Campus).order_by(Campus.id.desc())).first()
        campus_dane_code = int(last_campus.dane_code[-3:]) + 1 if last_campus else 1

        if institutions and len(campuses) < 30:
            for _ in range(30 - len(campuses)):
                institution = random.choice(institutions)
                name = f"Sede {fake.unique.last_name()}"
                if not session.exec(select(Campus).filter_by(name=name)).first():
                    campus = Campus(
                        name=name,
                        dane_code=f"{institution.dane_code}{campus_dane_code:03d}",
                        address=fake.address(),
                        latitude=float(fake.latitude()),
                        longitude=float(fake.longitude()),
                        institution_id=institution.id
                    )
                    session.add(campus)
                    campuses.append(campus)
                    campus_dane_code += 1
            session.commit()
            for campus in campuses:
                session.refresh(campus)

        # Create Beneficiaries
        fake.unique.clear()
        beneficiaries = session.exec(select(Beneficiary)).all()
        if all([document_types, genders, grades]) and len(beneficiaries) < 1000:
            new_beneficiaries = []
            for _ in range(1000 - len(beneficiaries)):
                number_document = fake.unique.ssn()
                if not session.exec(select(Beneficiary).filter_by(number_document=number_document)).first():
                    beneficiary = Beneficiary(
                        document_type_id=random.choice(document_types).id,
                        number_document=number_document,
                        first_name=fake.first_name(),
                        second_name=fake.first_name(),
                        first_surname=fake.last_name(),
                        second_surname=fake.last_name(),
                        birth_date=fake.date_of_birth(minimum_age=5, maximum_age=18),
                        gender_id=random.choice(genders).id,
                        grade_id=random.choice(grades).id,
                        etnic_group_id=random.choice(etnic_groups).id if etnic_groups and random.choice([True, False]) else None,
                        victim_conflict=random.choice([True, False]),
                        disability_type_id=random.choice(disability_types).id if disability_types and random.choice([True, False]) else None,
                    )
                    new_beneficiaries.append(beneficiary)
            session.add_all(new_beneficiaries)
            session.commit()
            beneficiaries.extend(new_beneficiaries)


        # Create Coverages
        coverages = []
        all_campuses = session.exec(select(Campus)).all()
        all_benefit_types = session.exec(select(BenefitType)).all()

        if all_campuses and all_benefit_types:
            for beneficiary in beneficiaries:
                existing_coverage = session.exec(select(Coverage).filter_by(beneficiary_id=beneficiary.id)).first()
                if not existing_coverage:
                    coverage = Coverage(
                        beneficiary_id=beneficiary.id,
                        campus_id=random.choice(all_campuses).id,
                        benefit_type_id=random.choice(all_benefit_types).id,
                        active=True
                    )
                    coverages.append(coverage)
            if coverages:
                session.add_all(coverages)
                session.commit()


        logger.info("Database populated with initial data.")
    except Exception as e:
        logger.error(f"Error populating data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_data()
