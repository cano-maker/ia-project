"""
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import pandas as pd

class PassengerPredictor:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.le = LabelEncoder()

    def load_data(self):
        # Cargar las tablas
        passenger = Table('passenger', self.metadata, autoload_with=self.engine)
        service = Table('service', self.metadata, autoload_with=self.engine)

        # Crear una sesión
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # Realizar la consulta
        query = select([passenger, service]).where(passenger.c.PassengerId == service.c.PassengerId)
        result = session.execute(query)

        # Convertir el resultado en un dataframe de pandas
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Cerrar la sesión
        session.close()

        return df

    def preprocess_data(self, df):
        # Codificar variables categóricas
        df['HomePlanet'] = self.le.fit_transform(df['HomePlanet'])
        df['Cabin'] = self.le.fit_transform(df['Cabin'])
        df['Destination'] = self.le.fit_transform(df['Destination'])

        # Dividir los datos en conjuntos de entrenamiento y prueba
        y = df.pop('VIP')
        X = df
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train):
        # Entrenar el modelo SVM
        clf = svm.SVC()
        clf.fit(X_train, y_train)

        # Guardar el modelo entrenado
        with open('model.pkl', 'wb') as f:
            pickle.dump(clf, f)

        print("Modelo guardado en 'model.pkl'")

    def run(self):
        df = self.load_data()
        X_train, X_test, y_train, y_test = self.preprocess_data(df)
        self.train_model(X_train, y_train)
"""