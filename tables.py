import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Operation(Base):
    __tablename__ = "operations"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    date = sqlalchemy.Column(sqlalchemy.Date)
    kind = sqlalchemy.Column(sqlalchemy.String)
    amount = sqlalchemy.Column(sqlalchemy.Numeric(10, 2)) #точность 10 знаков после запятой
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True) #необязательный параметр