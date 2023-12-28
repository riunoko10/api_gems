from models.gem_models import Gem, GemProperties, GemComplete, GemResponse
from sqlmodel import Session, select
import populate
from fastapi import HTTPException


def select_all_gems(engine):
    res = []
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)
        result = session.exec(statement)
        
        gem: Gem
        properties: GemProperties
        for gem, properties in result:
            respose_new = GemResponse(id=gem.id, 
                        price=gem.price, 
                        available=gem.available, 
                        type=gem.type, 
                        size=properties.size, 
                        color=properties.color, 
                        clarity=properties.clarity
            )
            res.append(respose_new)
    return res


def select_gem_by_id(engine, id_gem):
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties).where(Gem.id == id_gem)
        result = session.exec(statement)
        print(result.first())
        res = []
        for gem, properties in result:
            res.append({"gem": gem, "properties": properties})
        return res


def insert_gem(engine, gems: GemComplete):
    if gems is not None:
        all_save = []
        for gem in gems:
            with Session(engine) as session:
                gem_pro_save = GemProperties(size=gem.size, color=gem.color, clarity=gem.clarity,)
                session.add(gem_pro_save)
                session.commit()
                gem_save = Gem(price=gem.price, available=gem.available, type=gem.type, gem_properties_id=gem_pro_save.id)
                price = populate.calculate_gem_price(gem_save, gem_pro_save)
                gem_save.price = price
                session.add(gem_save)
                session.commit()
                session.refresh(gem_pro_save)
                session.refresh(gem_save)
                response = {"gem": gem_save, "properties": gem_pro_save}
                all_save.append(response)
        return all_save


def update_gem(engine, id:int, gem: GemComplete):
    with Session(engine) as session:
        gem_found = session.get(Gem, id)
        
        if gem_found is not None:
            properties_found = session.get(GemProperties, gem_found.gem_properties_id)
            gem_found.price = gem.price
            gem_found.available = gem.available
            gem_found.type = gem.type
            session.add(gem_found)
            session.commit()
            properties_found.size = gem.size
            properties_found.color = gem.color
            properties_found.clarity = gem.clarity
            session.add(properties_found)
            session.commit()
            session.refresh(gem_found)
            session.refresh(properties_found)
            return {"gem": gem_found, "properties": properties_found}
        raise HTTPException(status_code=404, detail=f"Gem id {id} not updated")

