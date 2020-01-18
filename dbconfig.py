from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Server(Base):
    __tablename__ = 'servers'

    project = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    app_prod_ip = Column(String(250))
    app_stage_ip = Column(String(250))
    db_prod_ip = Column(String(250))
    db_stage_ip = Column(String(250))

engine = create_engine('sqlite:///guide.db')


Base.metadata.create_all(engine)
