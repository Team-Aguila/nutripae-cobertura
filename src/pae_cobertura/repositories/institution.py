from sqlmodel import Session, select
from pae_cobertura.models.institution import Institution
from pae_cobertura.schemas.institutions import InstitutionCreate, InstitutionUpdate

def create_institution(*, session: Session, institution_in: InstitutionCreate) -> Institution:
    db_institution = Institution.model_validate(institution_in)
    session.add(db_institution)
    session.commit()
    session.refresh(db_institution)
    return db_institution

def get_institution_by_id(*, session: Session, institution_id: int) -> Institution:
    return session.get(Institution, institution_id)

def get_all_institutions(*, session: Session, skip: int = 0, limit: int = 100):
    statement = select(Institution).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_institution(*, session: Session, db_institution: Institution, institution_in: InstitutionUpdate) -> Institution:
    institution_data = institution_in.model_dump(exclude_unset=True)
    for key, value in institution_data.items():
        setattr(db_institution, key, value)
    session.add(db_institution)
    session.commit()
    session.refresh(db_institution)
    return db_institution

def delete_institution(*, session: Session, db_institution: Institution):
    session.delete(db_institution)
    session.commit()
