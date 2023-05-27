from sklearn import svm
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import pickle
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import pandas as pd

from passenger_predictor import PassengerPredictor


class PassengerTrainer:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.le = LabelEncoder()
        self.scaler = StandardScaler()
        self.clf = svm.SVC()

    def load_data(self):
        # Cargar las tablas
        passenger = Table('passenger', self.metadata, autoload_with=self.engine)
        services = Table('services', self.metadata, autoload_with=self.engine)

        print(passenger.columns.keys())

        # Crear una sesión
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # Realizar la consulta
        query = select('*').select_from(passenger.join(services, passenger.c.passengerid == services.c.passengerid))
        result = session.execute(query)

        # Convertir el resultado en un dataframe de pandas
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Cerrar la sesión
        session.close()

        return df

    def preprocess_data(self, df):
        # Codificar variables categóricas con LabelEncoder
        df['homeplanet'] = self.le.fit_transform(df['homeplanet'])
        df['cabin'] = self.le.fit_transform(df['cabin'])
        df['destination'] = self.le.fit_transform(df['destination'])
        df['name'] = self.le.fit_transform(df['name'])
        df['cryosleep'] = self.le.fit_transform(df['cryosleep'])
        df['vip'] = self.le.fit_transform(df['vip'])

        # Dividir los datos en conjuntos de entrenamiento y prueba
        y = df.pop('transported')
        X = df
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Identificar las características numéricas
        num_features = ['age', 'roomservice', 'foodcourt', 'shoppingmall', 'spa', 'vrdeck']

        # Convertir las columnas numéricas a float
        for feature in num_features:
            X_train[feature] = X_train[feature].astype(float)
            X_test[feature] = X_test[feature].astype(float)

        # Escalar solo las características numéricas
        X_train[num_features] = self.scaler.fit_transform(X_train[num_features])
        X_test[num_features] = self.scaler.transform(X_test[num_features])

        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train):
        # Entrenar el modelo SVM
        self.clf.fit(X_train, y_train)

        # Realizar la validación cruzada
        scores = cross_val_score(self.clf, X_train, y_train, cv=5)
        print(f"Puntuaciones de validación cruzada: {scores}")
        print(f"Precisión media de validación cruzada: {scores.mean()}")

        # Guardar el modelo entrenado y el escalador
        with open('./models/model.pkl', 'wb') as f:
            pickle.dump(self.clf, f)
        with open('./models/scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)

        print("Modelo y escalador guardados en 'model.pkl' y 'scaler.pkl' respectivamente")

    def predict(self, X):
        # Cargar el modelo y el escalador
        with open('./models/model.pkl', 'rb') as f:
            clf_loaded = pickle.load(f)
        with open('./models/scaler.pkl', 'rb') as f:
            scaler_loaded = pickle.load(f)

        # Estandarizar las características
        num_features = ['age', 'roomservice', 'foodcourt', 'shoppingmall', 'spa', 'vrdeck']
        X[num_features] = scaler_loaded.transform(X[num_features])

        # Hacer predicciones
        y_pred = clf_loaded.predict(X)

        return y_pred

    def run(self):
        # Cargar los datos
        df = self.load_data()

        # Preprocesar los datos
        X_train, X_test, y_train, y_test = self.preprocess_data(df)

        # Entrenar el modelo SVM
        self.train_model(X_train, y_train)

        passenger_predictor = PassengerPredictor()

        # Hacer predicciones
        y_pred = passenger_predictor.predict(X_test)
        print(f"Predicciones: {y_pred}")

        # Calcular la precisión
        print(f"Precisión: {accuracy_score(y_test, y_pred)}")

