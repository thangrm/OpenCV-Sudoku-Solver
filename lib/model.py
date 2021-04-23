import numpy as np
import os
from tensorflow import keras
from tensorflow.keras import layers
from cv2 import cv2


class Model:
    def __init__(self):
        # Model / data parameters
        self.num_classes = 10
        self.input_shape = (28, 28, 1)

        self.model = keras.Sequential(
        [
            keras.Input(shape=self.input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation="softmax"),
        ]
        )

        self.model.summary()

    def train_model(self):
        # Lấy dữ liệu chia làm 2 phần
        # Train có 60000
        # Test có 10000
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

        # Chia tỷ lệ hình ảnh theo phạm vi [0, 1]
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255

        # Đảm bảo hình ảnh có hình dạng (28, 28, 1)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)
        print("x_train shape:", x_train.shape)
        print(x_train.shape[0], "train samples")
        print(x_test.shape[0], "test samples")


        # chuyển đổi các lớp vector thành ma trận nhị phân
        y_train = keras.utils.to_categorical(y_train, self.num_classes)
        y_test = keras.utils.to_categorical(y_test, self.num_classes)

        """
        ## Train cho model
        """

        self.batch_size = 128
        self.epochs = 15

        self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

        self.model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs, validation_split=0.1)

        """
        ## Tính toán độ chính xác với dữ liệu test
        """

        score = self.model.evaluate(x_test, y_test, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])

        """
        ## Lưu lại file model
        """
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path,'digitalModel.h5')
        self.save_model(path)

    def save_model(self,path):
        self.model.save_weights(path)

    def load_model_from_file(self,path):
        self.model.load_weights(path)

if __name__ == "__main__":
    model = Model()
    model.train_model()

