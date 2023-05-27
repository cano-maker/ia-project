import pickle


class PassengerPredictor:

    def __init__(self):
        pass

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
