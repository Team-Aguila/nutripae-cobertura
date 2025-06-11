from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pae_cobertura.database import get_session
from pae_cobertura.models import (
    BenefitType,
    DisabilityType,
    DocumentType,
    EtnicGroup,
    Gender,
    Grade,
)

router = APIRouter()

# BenefitType Endpoints
@router.get("/benefit-types", response_model=List[BenefitType])
def get_benefit_types(session: Session = Depends(get_session)):
    return session.exec(select(BenefitType)).all()

@router.post("/benefit-types", response_model=BenefitType)
def create_benefit_type(benefit_type: BenefitType, session: Session = Depends(get_session)):
    session.add(benefit_type)
    session.commit()
    session.refresh(benefit_type)
    return benefit_type

@router.delete("/benefit-types/{benefit_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_benefit_type(benefit_type_id: int, session: Session = Depends(get_session)):
    benefit_type = session.get(BenefitType, benefit_type_id)
    if not benefit_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BenefitType not found")
    session.delete(benefit_type)
    session.commit()
    return

# Grade Endpoints
@router.get("/grades", response_model=List[Grade])
def get_grades(session: Session = Depends(get_session)):
    return session.exec(select(Grade)).all()

@router.post("/grades", response_model=Grade)
def create_grade(grade: Grade, session: Session = Depends(get_session)):
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade

@router.delete("/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    session.delete(grade)
    session.commit()
    return

# Other Parametric Endpoints
@router.get("/disability-types", response_model=List[DisabilityType])
def get_disability_types(session: Session = Depends(get_session)):
    return session.exec(select(DisabilityType)).all()

@router.get("/document-types", response_model=List[DocumentType])
def get_document_types(session: Session = Depends(get_session)):
    return session.exec(select(DocumentType)).all()

@router.get("/etnic-groups", response_model=List[EtnicGroup])
def get_etnic_groups(session: Session = Depends(get_session)):
    return session.exec(select(EtnicGroup)).all()

@router.get("/genders", response_model=List[Gender])
def get_genders(session: Session = Depends(get_session)):
    return session.exec(select(Gender)).all() 