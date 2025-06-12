from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from pae_cobertura.models.beneficiary import Beneficiary
from pae_cobertura.repositories.beneficiary import BeneficiaryRepository
from pae_cobertura.schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate

class BeneficiaryService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = BeneficiaryRepository(session)

    def create_beneficiary(self, beneficiary_in: BeneficiaryCreate) -> Beneficiary:
        existing_beneficiary = self.session.exec(
            select(Beneficiary).where(Beneficiary.number_document == beneficiary_in.number_document)
        ).first()

        if existing_beneficiary:
            raise ValueError(f"A beneficiary with document number {beneficiary_in.number_document} already exists.")

        return self.repository.create(beneficiary_in=beneficiary_in)

    def get_beneficiary(self, beneficiary_id: UUID) -> Optional[Beneficiary]:
        return self.repository.get_by_id(beneficiary_id=beneficiary_id)

    def get_beneficiaries(self, skip: int = 0, limit: int = 100) -> List[Beneficiary]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_beneficiary(
        self, beneficiary_id: UUID, beneficiary_in: BeneficiaryUpdate
    ) -> Beneficiary:
        db_beneficiary = self.session.get(Beneficiary, beneficiary_id)
        if not db_beneficiary:
            raise ValueError(f"Beneficiary with id {beneficiary_id} not found")

        if beneficiary_in.number_document is not None:
            existing_beneficiary = self.session.exec(
                select(Beneficiary)
                .where(Beneficiary.number_document == beneficiary_in.number_document)
                .where(Beneficiary.id != beneficiary_id)
            ).first()
            if existing_beneficiary:
                raise ValueError(
                    f"A beneficiary with document number {beneficiary_in.number_document} already exists."
                )

        return self.repository.update(
            db_beneficiary=db_beneficiary, beneficiary_in=beneficiary_in
        )

    def delete_beneficiary(self, beneficiary_id: UUID):
        db_beneficiary = self.session.get(Beneficiary, beneficiary_id)
        if not db_beneficiary:
            raise ValueError(f"Beneficiary with id {beneficiary_id} not found")

        # Soft delete could be implemented here by setting deleted_at
        # but for now we do a hard delete as per repository.
        # If soft delete is needed, repository should be changed.

        # Before deleting, check for related coverages
        if db_beneficiary.coverage:
            raise ValueError("Cannot delete beneficiary with associated coverages.")

        self.repository.delete(db_beneficiary=db_beneficiary)
        return True
