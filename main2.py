import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import exc
import pandas as pd
import psycopg2

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


class Service(Base):
    __tablename__ = 'service'
    PassengerId = Column(String, ForeignKey('passenger.PassengerId'), primary_key=True)
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


def QueryPerClass(homePlanet,engine):
    query = '''
        SELECT 
            p."PassengerId",
            p."Name",
            s."Spa" AS "SpaSpent"
        FROM 
            passenger p
        JOIN 
            service s
        ON 
            p."PassengerId" = s."PassengerId"
        WHERE 
            p."HomePlanet" = %(homePlanet)s;
    '''
    queryParameters = {'homePlanet': homePlanet}

    data_query = pd.read_sql_query(query, con=engine, params=queryParameters)
    return data_query

if __name__ == '__main__':
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'
    database_name = 'spaceship_titanic'

    create_database(database_name, user, password, host, port)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database_name}')

    try:
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        df = pd.read_csv('./resources/test.csv')

        df_pasajero = df[['PassengerId', 'HomePlanet', 'CryoSleep', 'Cabin', 'Destination', 'Age', 'VIP', 'Name']]
        df_servicios = df[['PassengerId', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']]

        df_pasajero.to_sql('passenger', engine, if_exists='append', index=False)
        df_servicios.to_sql('service', engine, if_exists='append', index=False)

    except exc.IntegrityError as e:
        print(f"Error de integridad de datos: {e._message}")
    except exc.SQLAlchemyError as e:
        print(f"Error en SQLAlchemy: {e._message}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:

        session.close()
    print(QueryPerClass('Earth',engine))
