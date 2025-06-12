from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from pae_cobertura.models.coverage import Coverage
from pae_cobertura.repositories.coverage import CoverageRepository
from pae_cobertura.schemas.coverage import CoverageCreate, CoverageUpdate

class CoverageService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = CoverageRepository(session)

    def create_coverage(self, coverage_in: CoverageCreate) -> Coverage:
        # Check for uniqueness: A beneficiary should not have the same benefit type twice for the same campus.
        existing_coverage = self.session.exec(
            select(Coverage)
            .where(Coverage.beneficiary_id == coverage_in.beneficiary_id)
            .where(Coverage.benefit_type_id == coverage_in.benefit_type_id)
            .where(Coverage.campus_id == coverage_in.campus_id)
        ).first()

        if existing_coverage:
            raise ValueError("This coverage (beneficiary, benefit type, campus) already exists.")

        return self.repository.create(coverage_in=coverage_in)

    def get_coverage(self, coverage_id: UUID) -> Optional[Coverage]:
        return self.repository.get_by_id(coverage_id=coverage_id)

    def get_all_coverages(self, skip: int = 0, limit: int = 100) -> List[Coverage]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_coverage(
        self, coverage_id: UUID, coverage_in: CoverageUpdate
    ) -> Coverage:
        db_coverage = self.session.get(Coverage, coverage_id)
        if not db_coverage:
            raise ValueError(f"Coverage with id {coverage_id} not found")

        # Check for uniqueness on update if relevant fields are changed
        if (
            coverage_in.beneficiary_id is not None or
            coverage_in.benefit_type_id is not None or
            coverage_in.campus_id is not None
        ):
            beneficiary_id = coverage_in.beneficiary_id or db_coverage.beneficiary_id
            benefit_type_id = coverage_in.benefit_type_id or db_coverage.benefit_type_id
            campus_id = coverage_in.campus_id or db_coverage.campus_id

            existing_coverage = self.session.exec(
                select(Coverage)
                .where(Coverage.beneficiary_id == beneficiary_id)
                .where(Coverage.benefit_type_id == benefit_type_id)
                .where(Coverage.campus_id == campus_id)
                .where(Coverage.id != coverage_id)
            ).first()

            if existing_coverage:
                raise ValueError("This coverage (beneficiary, benefit type, campus) already exists.")

        return self.repository.update(
            db_coverage=db_coverage, coverage_in=coverage_in
        )

    def delete_coverage(self, coverage_id: UUID):
        db_coverage = self.session.get(Coverage, coverage_id)
        if not db_coverage:
            raise ValueError(f"Coverage with id {coverage_id} not found")

        self.repository.delete(db_coverage=db_coverage)
        return True 