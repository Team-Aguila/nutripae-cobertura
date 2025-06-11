from datetime import datetime
from sqlmodel import Session, select, func
from pae_cobertura.models.town import Town
from pae_cobertura.models.institution import Institution
from pae_cobertura.schemas.towns import TownCreate, TownUpdate

class TownRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, town_in: TownCreate) -> dict:
        db_town = Town.model_validate(town_in)
        self.session.add(db_town)
        self.session.commit()
        self.session.refresh(db_town)
        
        town_dict = db_town.model_dump()
        town_dict["number_of_institutions"] = 0
        
        return town_dict

    def get_by_id(self, *, town_id: int) -> dict | None:
        town = self.session.get(Town, town_id)
        if not town:
            return None
            
        statement = (
            select(func.count(Institution.id))
            .where(Institution.town_id == town_id)
        )
        institution_count = self.session.exec(statement).first()
        
        town_dict = town.model_dump()
        town_dict["number_of_institutions"] = institution_count or 0
        
        return town_dict

    def get_all(self, *, skip: int = 0, limit: int = 100) -> list[dict]:
        institution_count = (
            select(
                Institution.town_id,
                func.count(Institution.id).label("institution_count")
            )
            .group_by(Institution.town_id)
            .subquery()
        )
        
        statement = (
            select(
                Town.id,
                Town.dane_code,
                Town.name,
                Town.created_at,
                Town.updated_at,
                Town.department_id,
                func.coalesce(institution_count.c.institution_count, 0).label("number_of_institutions")
            )
            .outerjoin(institution_count, Town.id == institution_count.c.town_id)
            .order_by(Town.name)
            .offset(skip)
            .limit(limit)
        )
        
        result = self.session.exec(statement).mappings().all()
        return result

    def update(self, *, db_town: Town, town_in: TownUpdate) -> dict:
        update_data = town_in.model_dump(exclude_unset=True)
        if 'dane_code' in update_data:
            del update_data['dane_code']
            
        for key, value in update_data.items():
            setattr(db_town, key, value)
            
        db_town.updated_at = datetime.now()
        self.session.add(db_town)
        self.session.commit()
        self.session.refresh(db_town)
        
        statement = (
            select(func.count(Institution.id))
            .where(Institution.town_id == db_town.id)
        )
        institution_count = self.session.exec(statement).first()
        
        town_dict = db_town.model_dump()
        town_dict["number_of_institutions"] = institution_count or 0
        
        return town_dict

    def delete(self, *, db_town: Town):
        statement = select(func.count(Institution.id)).where(Institution.town_id == db_town.id)
        institution_count = self.session.exec(statement).first()
        
        if institution_count > 0:
            raise ValueError(f"No se puede eliminar el municipio {db_town.name} porque tiene {institution_count} instituciones asociadas")
            
        self.session.delete(db_town)
        self.session.commit()
