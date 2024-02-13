import sys as sys
import numpy as np
import pandas as pd

from src.data_process import data_process
from src.data_process import data_spliter
from src.LogisticRegression import LogisticRegression
from src.file_management import save_parameters_to_file

house_names = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']

if __name__ == "__main__":
    try:
        assert len(sys.argv) == 2, "1 argument required"

        dataset = pd.read_csv(sys.argv[1])
        x, y = data_process(dataset, 'train model')
        x_train, x_test, y_train, y_test = data_spliter(x, y, 0.8)

        # model
        model = LogisticRegression()

        # Training
        weights, bias = model.fit(x_train, y_train)

        # Test
        y_house_predictions = model.predict(x_test)
        y_house_accuracy = np.mean(y_house_predictions == y_test)
        print(f"Predictions: {y_house_predictions.flatten()}")
        print(f"Accuracy: {y_house_accuracy * 100:.2f}%")

        # Saving thetas
        save_parameters_to_file({
            'weights': weights,
            'bias': bias
        }, 'weights')

    except Exception as error:
        print(f"error: {error}")