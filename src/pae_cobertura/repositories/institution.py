from datetime import datetime
from sqlmodel import Session, select, func
from pae_cobertura.models.institution import Institution
from pae_cobertura.models.campus import Campus
from pae_cobertura.schemas.institutions import InstitutionCreate, InstitutionUpdate

class InstitutionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, institution_in: InstitutionCreate) -> dict:
        db_institution = Institution.model_validate(institution_in)
        self.session.add(db_institution)
        self.session.commit()
        self.session.refresh(db_institution)

        institution_dict = db_institution.model_dump()
        institution_dict["number_of_campuses"] = 0

        return institution_dict

    def get_by_id(self, *, institution_id: int) -> dict | None:
        institution = self.session.get(Institution, institution_id)
        if not institution:
            return None

        statement = (
            select(func.count(Campus.id))
            .where(Campus.institution_id == institution_id)
        )
        campus_count = self.session.exec(statement).first()

        institution_dict = institution.model_dump()
        institution_dict["number_of_campuses"] = campus_count or 0

        return institution_dict

    def get_all(self, *, skip: int = 0, limit: int = 100) -> list[dict]:
        campus_count = (
            select(
                Campus.institution_id,
                func.count(Campus.id).label("campus_count")
            )
            .group_by(Campus.institution_id)
            .subquery()
        )

        statement = (
            select(
                Institution.id,
                Institution.dane_code,
                Institution.name,
                Institution.created_at,
                Institution.updated_at,
                Institution.town_id,
                func.coalesce(campus_count.c.campus_count, 0).label("number_of_campuses")
            )
            .outerjoin(campus_count, Institution.id == campus_count.c.institution_id)
            .order_by(Institution.name)
            .offset(skip)
            .limit(limit)
        )

        result = self.session.exec(statement).mappings().all()
        return result

    def update(self, *, db_institution: Institution, institution_in: InstitutionUpdate) -> dict:
        update_data = institution_in.model_dump(exclude_unset=True)
        if 'dane_code' in update_data:
            del update_data['dane_code']

        for key, value in update_data.items():
            setattr(db_institution, key, value)

        db_institution.updated_at = datetime.now()
        self.session.add(db_institution)
        self.session.commit()
        self.session.refresh(db_institution)

        statement = (
            select(func.count(Campus.id))
            .where(Campus.institution_id == db_institution.id)
        )
        campus_count = self.session.exec(statement).first()

        institution_dict = db_institution.model_dump()
        institution_dict["number_of_campuses"] = campus_count or 0

        return institution_dict

    def delete(self, *, db_institution: Institution):
        statement = select(func.count(Campus.id)).where(Campus.institution_id == db_institution.id)
        campus_count = self.session.exec(statement).first()

        if campus_count > 0:
            raise ValueError(f"No se puede eliminar la institucion {db_institution.name} porque tiene {campus_count} sedes asociadas")

        self.session.delete(db_institution)
        self.session.commit()

    def get_by_town(self, *, town_id: int, skip: int = 0, limit: int = 100) -> list[dict]:
        institutions = self.session.exec(
            select(Institution)
            .where(Institution.town_id == town_id)
            .order_by(Institution.name)
            .offset(skip)
            .limit(limit)
        ).all()

        institution_dicts = []
        for institution in institutions:
            statement = (
                select(func.count(Campus.id))
                .where(Campus.institution_id == institution.id)
            )
            campus_count = self.session.exec(statement).first()
            institution_dict = institution.model_dump()
            institution_dict["number_of_campuses"] = campus_count or 0
            institution_dicts.append(institution_dict)

        return institution_dicts
