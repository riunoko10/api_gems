from sqlmodel import Relationship, SQLModel, Field, MetaData
from typing import Optional
from enum import Enum, IntEnum

meta = MetaData(schema="Gemas")


class Enum_(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class GemClarity(IntEnum):
    SI = 1
    VS = 2
    VVS = 3
    FL = 4

class GemTypes(str, Enum_):
    DIAMOND = 'DIAMOND'
    EMERALD = 'EMERALD'
    RUBY = 'RUBY'    

class GemColors(str, Enum_):
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'


class BaseGem(SQLModel):
    metadata = meta
    price: float = 1000
    available: bool = Field(default=True)
    type: Optional[GemTypes] = GemTypes.DIAMOND


class GemComplete(BaseGem):
    size: float = 1
    clarity: Optional[GemClarity] = Field(default=None)
    color: Optional[GemColors] = Field(default=None)

class GemProperties(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    size: float = 1
    clarity: Optional[GemClarity] = Field(default=None)
    color: Optional[GemColors] = Field(default=None)
    gem: Optional['Gem'] = Relationship(back_populates="gem_properties")




class Gem(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float = 1000
    available: bool = Field(default=True)
    type: Optional[GemTypes] = GemTypes.DIAMOND

    gem_properties_id: Optional[int] = Field(default=None, foreign_key="gemproperties.id")
    gem_properties: Optional[GemProperties] = Relationship(back_populates="gem")


