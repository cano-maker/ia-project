import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import exc
import pandas as pd
import psycopg2

Base = declarative_base()


class Pasajero(Base):
    __tablename__ = 'pasajero'
    PassengerId = Column(String, primary_key=True)
    HomePlanet = Column(String)
    CryoSleep = Column(Boolean)
    Cabin = Column(String)
    Destination = Column(String)
    Age = Column(Integer)
    VIP = Column(Boolean)
    Name = Column(String)


class Servicios(Base):
    __tablename__ = 'servicios'
    PassengerId = Column(String, ForeignKey('pasajero.PassengerId'), primary_key=True)
    RoomService = Column(Integer)
    FoodCourt = Column(Integer)
    ShoppingMall = Column(Integer)
    Spa = Column(Integer)
    VRDeck = Column(Integer)


def create_database(database_name, user, password, host, port):
    try:
        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {database_name};")
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error al crear la base de datos: {e}")


if __name__ == '__main__':
    # Cambia los siguientes datos con tus credenciales de Postgres y el nombre de tu base de datos
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'
    database_name = 'spaceship_titanic'

    # Crea la base de datos
    create_database(database_name, user, password, host, port)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database_name}')

    try:
        # Crea todas las tablas en la base de datos
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

    except exc.IntegrityError as e:
        print(f"Error de integridad de datos: {e}")
    except exc.SQLAlchemyError as e:
        print(f"Error en SQLAlchemy: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # Cierra la sesión
        session.close()
