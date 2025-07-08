from datetime import datetime
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from models.beneficiary import Beneficiary
from schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate

class BeneficiaryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, beneficiary_in: BeneficiaryCreate) -> Beneficiary:
        db_beneficiary = Beneficiary.model_validate(beneficiary_in)
        self.session.add(db_beneficiary)
        self.session.commit()
        self.session.refresh(db_beneficiary)
        return db_beneficiary

    def get_by_id(self, *, beneficiary_id: UUID) -> Beneficiary | None:
        statement = (
            select(Beneficiary)
            .where(Beneficiary.id == beneficiary_id)
            .options(
                selectinload(Beneficiary.document_type),
                selectinload(Beneficiary.gender),
                selectinload(Beneficiary.grade),
                selectinload(Beneficiary.etnic_group),
                selectinload(Beneficiary.disability_type),
                selectinload(Beneficiary.coverage)
            )
        )
        return self.session.exec(statement).first()

    def get_all(self, *, skip: int = 0, limit: int = 100) -> list[Beneficiary]:
        statement = (
            select(Beneficiary)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Beneficiary.document_type),
                selectinload(Beneficiary.gender),
                selectinload(Beneficiary.grade),
                selectinload(Beneficiary.etnic_group),
                selectinload(Beneficiary.disability_type)
            )
        )
        return self.session.exec(statement).all()

    def update(
        self, *, db_beneficiary: Beneficiary, beneficiary_in: BeneficiaryUpdate
    ) -> Beneficiary:
        update_data = beneficiary_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_beneficiary, key, value)

        db_beneficiary.updated_at = datetime.now()
        self.session.add(db_beneficiary)
        self.session.commit()
        self.session.refresh(db_beneficiary)
        return db_beneficiary

    def delete(self, *, db_beneficiary: Beneficiary):
        self.session.delete(db_beneficiary)
        self.session.commit()
        return True
