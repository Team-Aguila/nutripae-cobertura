from datetime import datetime
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from pae_cobertura.models.coverage import Coverage
from pae_cobertura.schemas.coverage import CoverageCreate, CoverageUpdate

class CoverageRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, coverage_in: CoverageCreate) -> Coverage:
        db_coverage = Coverage.model_validate(coverage_in)
        self.session.add(db_coverage)
        self.session.commit()
        self.session.refresh(db_coverage)
        return db_coverage

    def get_by_id(self, *, coverage_id: UUID) -> Coverage | None:
        statement = (
            select(Coverage)
            .where(Coverage.id == coverage_id)
            .options(
                selectinload(Coverage.benefit_type),
                selectinload(Coverage.campus),
                selectinload(Coverage.beneficiary)
            )
        )
        return self.session.exec(statement).first()

    def get_all(self, *, skip: int = 0, limit: int = 100) -> list[Coverage]:
        statement = (
            select(Coverage)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Coverage.benefit_type),
                selectinload(Coverage.campus),
                selectinload(Coverage.beneficiary)
            )
        )
        return self.session.exec(statement).all()

    def update(
        self, *, db_coverage: Coverage, coverage_in: CoverageUpdate
    ) -> Coverage:
        update_data = coverage_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_coverage, key, value)

        db_coverage.updated_at = datetime.now()
        self.session.add(db_coverage)
        self.session.commit()
        self.session.refresh(db_coverage)
        return db_coverage

    def delete(self, *, db_coverage: Coverage):
        self.session.delete(db_coverage)
        self.session.commit()
        return True

    def get_by_campus(self, *, campus_id: int, skip: int = 0, limit: int = 100) -> list[Coverage]:
        statement = (
            select(Coverage)
            .where(Coverage.campus_id == campus_id)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Coverage.benefit_type),
                selectinload(Coverage.campus),
                selectinload(Coverage.beneficiary)
            )
        )
        return self.session.exec(statement).all()
