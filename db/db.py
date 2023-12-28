from sqlmodel import create_engine


DATABASE_URL = "postgresql://admin:admin12345@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)