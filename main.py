import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

Base = declarative_base()


class Passenger(Base):
    __tablename__ = 'passenger'
    PassengerId = Column(String, primary_key=True)
    HomePlanet = Column(String)
    CryoSleep = Column(Boolean)
    Cabin = Column(String)
    Destination = Column(String)
    Age = Column(Integer)
    VIP = Column(Boolean)
    Name = Column(String)


class Services(Base):
    __tablename__ = 'services'
    PassengerId = Column(String, ForeignKey('passenger.PassengerId'), primary_key=True)
    RoomService = Column(Integer)
    FoodCourt = Column(Integer)
    ShoppingMall = Column(Integer)
    Spa = Column(Integer)
    VRDeck = Column(Integer)


def QueryPerClass(engine):
    query = 'SELECT * FROM Passenger'
    data_query = pd.read_sql_query(query, con=engine)
    return data_query


if __name__ == '__main__':
    # Cambia los siguientes datos con tus credenciales de Postgres y el nombre de tu base de datos
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/spaceship_titanic')

    # print(QueryPerClass(engine))
    #Crea todas las tablas en la base de datos
    Base.metadata.create_all(engine)

    # Crea una nueva sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Lee el archivo CSV
    df = pd.read_csv('./resources/test.csv')

    # Normaliza la información en dos DataFrames
    df_pasajero = df[['PassengerId', 'HomePlanet', 'CryoSleep', 'Cabin', 'Destination', 'Age', 'VIP', 'Name']]
    df_servicios = df[['PassengerId', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']]

    # Inserta la información en las tablas
    df_pasajero.to_sql('pasajero', engine, if_exists='append', index=False)
    df_servicios.to_sql('servicios', engine, if_exists='append', index=False)

    # Cierra la sesión
    session.close()
