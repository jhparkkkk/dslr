import numpy as np
import matplotlib.pyplot as plt

class LogisticRegression:
    def __init__(self, learning_rate=0.05, max_iterations=1500, weights=[], bias=0, batch_size=None):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.weights = weights
        self.bias = bias
        self.batch_size = batch_size

    def one_hot_encode(self, y) -> np.array:
        """
        Encodes each category (Hogwart Houses) as a binary vector
        
        Args:
            y (np.array): Array of labels

        Returns:
            np.array: One-hot encoded labels
        """
        one_hot_y = np.zeros((len(y), len(np.unique(y))))
        for i in range(len(y)):
            one_hot_y[i, y[i]] = 1
        return one_hot_y

    def softmax(self, x) -> np.array:
        """
        Compute the probabilities of each class,
        ensuring that the sum of probabilities across all classes equals 1.

        Args:
            X (np.array): features input

        Returns:
            np.array: probabilities of each class
        """
        #z = np.dot(x, self.weights) + self.bias
        #exp_z = np.exp(z)
        #return exp_z / np.sum(exp_z, axis=1, keepdims=True)

        z = np.dot(x, self.weights) + self.bias
        exp_z = np.exp(-z)
        return 1 / (1 + exp_z)

    def cross_entropy_loss(self, y_true, y_pred) -> np.array:
        """
        Compute the cross-entropy loss for multinomial logistic regression

        Args:
            y_true (numpy.ndarray): Array of true labels in one-hot encoded format.
            y_pred (numpy.ndarray): Array of predicted probabilities for each class.

        Returns:
            float: cross-entropy loss.
        """
        num_samples = y_true.shape[0]
        # to avoid div by zero
        epsilon = 1e-15
        # to avoid log(0)
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -np.sum(y_true * np.log(y_pred)) / num_samples
        return loss

    def fit(self, x:np.ndarray, y:np.ndarray) -> np.ndarray:
        """
        Train the multinomial logistic regression model

        Args:
            X (np.ndarray): input features
            y (np.ndarray): labels

        Returns:
            np.ndarray: Tuple containing the trained weights and bias
        """
        m, n = x.shape
        y_encoded = self.one_hot_encode(y)

        self.weights = np.zeros((n, y_encoded.shape[1]))
        self.bias = 0

        costs = []
        for i in range(self.max_iterations):
            if self.batch_size is None:
                x_batch = x
                y_batch = y_encoded
            elif self.batch_size == 1:
                random_index = np.random.randint(0, m)

                x_batch = x[random_index].reshape(1, -1)
                y_batch = y_encoded[random_index].reshape(1, -1)
            else:
                np.random.seed(i)

                # Combining x and y
                combined_data = list(zip(x, y_encoded))
                np.random.shuffle(combined_data)
                x_shuffled, y_shuffled = zip(*combined_data)

                x_shuffled = np.array(x_shuffled)
                y_shuffled = np.array(y_shuffled)

                x_batch = x_shuffled[:self.batch_size]
                y_batch = y_shuffled[:self.batch_size]

            y_prediction = self.softmax(x_batch)

            dw = (1 / len(x_batch)) * np.dot(x_batch.T, (y_prediction - y_batch))
            db = (1 / len(x_batch)) * np.sum(y_prediction - y_batch, axis=0)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            cost = self.cross_entropy_loss(y_batch, y_prediction)
            costs.append(cost)

        print(f'Cost : [{costs[0]}] -> [{costs[-1]}]')

        plt.plot(range(1, self.max_iterations + 1), costs)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.title('Cost vs Iterations')
        plt.show()
        return self.weights, self.bias

    def predict(self, X):
        """
        Makes predictions using the trained weights and bias

        Args:
            X (np.array): input features

        Returns:
            np.array: predicted labels
        """
        y_pred = self.softmax(X)
        return np.argmax(y_pred, axis=1)
