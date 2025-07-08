from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import (
    BenefitType,
    DisabilityType,
    DocumentType,
    EtnicGroup,
    Gender,
    Grade,
)
import logging
from core.dependencies import require_list, require_create, require_delete

router = APIRouter(
    prefix="/parametrics",
    tags=["Parametrics"],
)

# BenefitType Endpoints
@router.get("/benefit-types", response_model=List[BenefitType])
def get_benefit_types(session: Session = Depends(get_session), current_user: dict = Depends(require_list())):
    logging.info("Getting benefit types")
    return session.exec(select(BenefitType)).all()

@router.post("/benefit-types", response_model=BenefitType)
def create_benefit_type(benefit_type: BenefitType, session: Session = Depends(get_session), current_user: dict = Depends(require_create())):
    logging.info(f"Creating benefit type: {benefit_type}")
    session.add(benefit_type)
    session.commit()
    session.refresh(benefit_type)
    return benefit_type

@router.delete("/benefit-types/{benefit_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_benefit_type(benefit_type_id: int, session: Session = Depends(get_session), current_user: dict = Depends(require_delete())):
    logging.info(f"Deleting benefit type: {benefit_type_id}")
    benefit_type = session.get(BenefitType, benefit_type_id)
    if not benefit_type:
        logging.error(f"Benefit type not found: {benefit_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BenefitType not found")
    session.delete(benefit_type)
    session.commit()
    return

# Grade Endpoints
@router.get("/grades", response_model=List[Grade])
def get_grades(session: Session = Depends(get_session), current_user: dict = Depends(require_list())):
    logging.info("Getting grades")
    return session.exec(select(Grade)).all()

@router.post("/grades", response_model=Grade)
def create_grade(grade: Grade, session: Session = Depends(get_session), current_user: dict = Depends(require_create())):
    logging.info(f"Creating grade: {grade}")
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade

@router.delete("/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, session: Session = Depends(get_session), current_user: dict = Depends(require_delete())):
    logging.info(f"Deleting grade: {grade_id}")
    grade = session.get(Grade, grade_id)
    if not grade:
        logging.error(f"Grade not found: {grade_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    session.delete(grade)
    session.commit()
    return

# Other Parametric Endpoints
@router.get("/disability-types", response_model=List[DisabilityType])
def get_disability_types(session: Session = Depends(get_session), current_user: dict = Depends(require_list())):
    logging.info("Getting disability types")
    return session.exec(select(DisabilityType)).all()

@router.get("/document-types", response_model=List[DocumentType])
def get_document_types(session: Session = Depends(get_session), current_user: dict = Depends(require_list())):
    logging.info("Getting document types")
    return session.exec(select(DocumentType)).all()

@router.get("/etnic-groups", response_model=List[EtnicGroup])
def get_etnic_groups(session: Session = Depends(get_session), current_user: dict = Depends(require_list())):
    logging.info("Getting etnic groups")
    return session.exec(select(EtnicGroup)).all()

@router.get("/genders", response_model=List[Gender])
def get_genders(session: Session = Depends(get_session), current_user: dict = Depends(require_list())):
    logging.info("Getting genders")
    return session.exec(select(Gender)).all()
