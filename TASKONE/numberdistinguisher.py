import tensorflow as tf
import matplotlib.pyplot as plt

# Download from Keras
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalizing
x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32")  / 255.0

# Display shapes
print("Training data shape:", x_train.shape)
print("Training labels shape:", y_train.shape)
print("Test data shape:", x_test.shape)
print("Test labels shape:", y_test.shape)

# Display first image
plt.imshow(x_train[677], cmap="gray")  
plt.title(str(y_train[677]))
plt.show