import random
import string
from sqlmodel import Session
from models.gem_models import Gem, GemProperties, GemTypes, GemColors


# color_grades = string.ascii_uppercase[3:9]

color_multiplier = {
    'D': 1.8,
    'E': 1.6,
    'F': 1.4,
    'G': 1.2,
    'H': 1,
    'I': 0.8
}

def calculate_gem_price(gem:Gem, gem_prop:GemProperties):
    price = 1000
    if gem.type == 'Ruby':
        price = 400
    elif gem.type == 'Emerald':
        price = 650
        
    if gem_prop.clarity == 1:
        price *= 0.75
    elif gem_prop.clarity == 3:
        price *= 1.25
    elif gem_prop.clarity == 4:
        price *= 1.50
    
    price = price * (gem_prop.size**3)
    
    if gem.type == 'Diamond':
        multiplier = color_multiplier[gem_prop.color]
        price *= multiplier
    
    price = round(price, 2)
    return price


def create_gem_props(): 
    size = random.randint(3,70)/10
    color = random.choice(GemColors.list())
    clarity = random.randint(1,4)
    gem_p = GemProperties(size=size, clarity=clarity, color=color)
    return gem_p


def create_gem(gem_p:GemProperties):
    type = random.choice(GemTypes.list())
    gem = Gem(available=True, gem_properties_id=gem_p.id, type=type)
    price = calculate_gem_price(gem, gem_p)
    gem.price = price
    return gem


def create_gems_db(engine):
    gem_ps = [create_gem_props() for x in range(10)]
    with Session(engine) as session:
        session.add_all(gem_ps)
        session.commit()
        gems = [create_gem(gem_ps[x]) for x in range(5)]
        session.add_all(gems)
        session.commit()
        print(gems)
