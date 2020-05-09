import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Activation
import pickle

X = pickle.load(open("X.pickle","rb"))
y = pickle.load(open("y.pickle","rb"))

model = Sequential()

model.add(Conv2D(16,(3,3), activation = "relu",input_shape=X.shape[1:]))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3), activation = "relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3), activation = "relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(128,(3,3), activation = "relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(units = 32,activation = "relu"))
model.add(Dense(units = 10,activation = "softmax"))

model.compile(loss="sparse_categorical_crossentropy" , optimizer="adam", metrics=["accuracy"])
model.fit(X, y, batch_size=20 , validation_split=0.2, epochs=20)

#tensorflow.keras.models.save_model(model,"C:/Users/Leslie/Desktop/Sketch/brain.model")
model.save("brain")
print("Done building the model")
print(model.summary())
input()



"""model.compile(loss="sparse_categorical_crossentropy" , optimizer="adam", metrics=["accuracy"])
model.fit(X, y, batch_size=30 , validation_split=0.2, epochs=15)
tensorflow.keras.models.save_model(model,"brain.model")
print("Done building the model")
print(model.summary())
input()"""
