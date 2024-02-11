from sqlalchemy import Column, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TrainingData(Base):
    """
    Represents the TrainingData table in the database.
    """
    __tablename__ = 'training_data'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)

class IdealFunctions(Base):
    """
    Represents the IdealFunctions table in the database.
    """
    __tablename__ = 'ideal_functions'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    # Generating Y columns for each ideal function
    for i in range(1, 51):
        locals()[f"y{i}"] = Column(Float)

class TestData(Base):
    """
    Represents the TestData table in the database.
    """
    __tablename__ = 'test_data'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    DeltaY = Column(Float)
    IdealFunctionNumber = Column(Integer)

def create_session(database_url='sqlite:///output/database/data_analysis.db'):
    """
    Creates and returns a session for the specified database.
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
