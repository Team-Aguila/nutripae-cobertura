from sqlmodel import Session, select
from pae_cobertura.models.town import Town
from pae_cobertura.schemas.towns import TownCreate, TownUpdate

def create_town(*, session: Session, town_in: TownCreate) -> Town:
    db_town = Town.model_validate(town_in)
    session.add(db_town)
    session.commit()
    session.refresh(db_town)
    return db_town

def get_town_by_id(*, session: Session, town_id: int) -> Town:
    return session.get(Town, town_id)

def get_all_towns(*, session: Session, skip: int = 0, limit: int = 100):
    statement = select(Town).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_town(*, session: Session, db_town: Town, town_in: TownUpdate) -> Town:
    town_data = town_in.model_dump(exclude_unset=True)
    for key, value in town_data.items():
        setattr(db_town, key, value)
    session.add(db_town)
    session.commit()
    session.refresh(db_town)
    return db_town

def delete_town(*, session: Session, db_town: Town):
    session.delete(db_town)
    session.commit()
