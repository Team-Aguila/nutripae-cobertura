from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from models.beneficiary import Beneficiary
from repositories.beneficiary import BeneficiaryRepository
from schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate
import logging

class BeneficiaryService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = BeneficiaryRepository(session)

    def create_beneficiary(self, beneficiary_in: BeneficiaryCreate) -> Beneficiary:
        logging.info(f"Creating beneficiary: {beneficiary_in}")
        existing_beneficiary = self.session.exec(
            select(Beneficiary).where(Beneficiary.number_document == beneficiary_in.number_document)
        ).first()

        if existing_beneficiary:
            raise ValueError(f"A beneficiary with document number {beneficiary_in.number_document} already exists.")

        return self.repository.create(beneficiary_in=beneficiary_in)

    def get_beneficiary(self, beneficiary_id: UUID) -> Optional[Beneficiary]:
        logging.info(f"Getting beneficiary: {beneficiary_id}")
        return self.repository.get_by_id(beneficiary_id=beneficiary_id)

    def get_beneficiaries(self, skip: int = 0, limit: int = 100) -> List[Beneficiary]:
        logging.info(f"Getting beneficiaries: {skip}, {limit}")
        return self.repository.get_all(skip=skip, limit=limit)

    def update_beneficiary(
        self, beneficiary_id: UUID, beneficiary_in: BeneficiaryUpdate
    ) -> Beneficiary:
        logging.info(f"Updating beneficiary: {beneficiary_id}")
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
        logging.info(f"Deleting beneficiary: {beneficiary_id}")
        db_beneficiary = self.session.get(Beneficiary, beneficiary_id)
        if not db_beneficiary:
            logging.error(f"Beneficiary with id {beneficiary_id} not found")
            raise ValueError(f"Beneficiary with id {beneficiary_id} not found")

        # Soft delete could be implemented here by setting deleted_at
        # but for now we do a hard delete as per repository.
        # If soft delete is needed, repository should be changed.

        # Before deleting, check for related coverages
        if db_beneficiary.coverage:
            logging.error(f"Cannot delete beneficiary with associated coverages: {beneficiary_id}")
            raise ValueError("Cannot delete beneficiary with associated coverages.")

        self.repository.delete(db_beneficiary=db_beneficiary)
        return True
