from datetime import datetime
from sqlmodel import Session, select, func
from pae_cobertura.models.campus import Campus
from pae_cobertura.models.coverage import Coverage
from pae_cobertura.schemas.campus import CampusCreate, CampusUpdate

class CampusRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, campus_in: CampusCreate) -> dict:
        db_campus = Campus.model_validate(campus_in)
        self.session.add(db_campus)
        self.session.commit()
        self.session.refresh(db_campus)

        campus_dict = db_campus.model_dump()
        campus_dict["number_of_coverages"] = 0

        return campus_dict

    def get_by_id(self, *, campus_id: int) -> dict | None:
        campus = self.session.get(Campus, campus_id)
        if not campus:
            return None

        statement = (
            select(func.count(Coverage.id))
            .where(Coverage.campus_id == campus_id)
        )
        coverage_count = self.session.exec(statement).first()

        campus_dict = campus.model_dump()
        campus_dict["number_of_coverages"] = coverage_count or 0

        return campus_dict

    def get_all(self, *, skip: int = 0, limit: int = 100) -> list[dict]:
        coverage_count_sq = (
            select(
                Coverage.campus_id,
                func.count(Coverage.id).label("coverage_count")
            )
            .group_by(Coverage.campus_id)
            .subquery()
        )

        statement = (
            select(
                Campus.id,
                Campus.dane_code,
                Campus.name,
                Campus.address,
                Campus.latitude,
                Campus.longitude,
                Campus.created_at,
                Campus.updated_at,
                Campus.institution_id,
                func.coalesce(coverage_count_sq.c.coverage_count, 0).label("number_of_coverages")
            )
            .outerjoin(coverage_count_sq, Campus.id == coverage_count_sq.c.campus_id)
            .order_by(Campus.name)
            .offset(skip)
            .limit(limit)
        )

        result = self.session.exec(statement).mappings().all()
        return result

    def update(self, *, db_campus: Campus, campus_in: CampusUpdate) -> dict:
        update_data = campus_in.model_dump(exclude_unset=True)
        if 'dane_code' in update_data:
            del update_data['dane_code']

        for key, value in update_data.items():
            setattr(db_campus, key, value)

        db_campus.updated_at = datetime.now()
        self.session.add(db_campus)
        self.session.commit()
        self.session.refresh(db_campus)

        statement = (
            select(func.count(Coverage.id))
            .where(Coverage.campus_id == db_campus.id)
        )
        coverage_count = self.session.exec(statement).first()

        campus_dict = db_campus.model_dump()
        campus_dict["number_of_coverages"] = coverage_count or 0

        return campus_dict

    def delete(self, *, db_campus: Campus):
        statement = select(func.count(Coverage.id)).where(Coverage.campus_id == db_campus.id)
        coverage_count = self.session.exec(statement).first()

        if coverage_count > 0:
            raise ValueError(f"No se puede eliminar el campus {db_campus.name} porque tiene {coverage_count} coberturas asociadas")

        self.session.delete(db_campus)
        self.session.commit()

    def get_by_institution(self, *, institution_id: int, skip: int = 0, limit: int = 100) -> list[dict]:
        campuses = self.session.exec(
            select(Campus)
            .where(Campus.institution_id == institution_id)
            .order_by(Campus.name)
            .offset(skip)
            .limit(limit)
        ).all()

        campus_dicts = []
        for campus in campuses:
            statement = (
                select(func.count(Coverage.id))
                .where(Coverage.campus_id == campus.id)
            )
            coverage_count = self.session.exec(statement).first()
            campus_dict = campus.model_dump()
            campus_dict["number_of_coverages"] = coverage_count or 0
            campus_dicts.append(campus_dict)

        return campus_dicts
