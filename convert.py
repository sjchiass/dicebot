import tensorflow as tf

# Load model
model = tf.keras.models.load_model("./save_at_25.h5")

# Convert the model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)
