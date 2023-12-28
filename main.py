from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import uvicorn
from sqlmodel import SQLModel, Session, select
from models import gem_models
import populate
from repos import gem_repository
from db.db import engine
from typing import List, Optional

app = FastAPI()



def create_db_and_tables():
    try:
        print("Creando base de datos...")
        gem_models.meta.create_all(engine)
        print("Base de datos creada")
    except Exception as e:
        raise RuntimeError(e)

@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/gems")
def gems():
    all_gems = gem_repository.select_all_gems(engine)
    return {"gems": all_gems}


@app.get("/gem/{id}")
def gems(id:int):
    gem = gem_repository.select_gem_by_id(engine, id)
    return {"gem": gem}


@app.post('/gems')
def create_gem(gem: List[gem_models.GemComplete]):
    result = gem_repository.insert_gem(engine, gem)
    if result is None:
        raise HTTPException(status_code=404, detail="Gem not created")
    return result


@app.put('/gem')
def update_gem(id: int, gem: gem_models.GemComplete):
    result = gem_repository.update_gem(engine, id, gem)
    if result is None:
        raise HTTPException(status_code=404, detail="Gem not updated")
    return result


# @app.delete()


@app.get("/populate")
def populate_db():
    populate.create_gems_db(engine)
    return {"message": "populate"}


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
