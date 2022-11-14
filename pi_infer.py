import tflite_runtime.interpreter as tflite
from PIL import Image
import numpy as np


# Load the TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load data into model
input_shape = input_details[0]['shape']
input_data = np.asarray(Image.open("test.jpg").convert("L"))
input_data = np.expand_dims(input_data, 0)
input_data = np.expand_dims(input_data, 3)
input_data = input_data.astype("float32")
#print(input_data)
#print(input_data.shape)

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
#print(output_data)

guess = np.argmax(output_data.flatten())
certainty = np.max(output_data.flatten())
output = f"### [DICELOT] BLEEP BLORP 6d6 => {guess+6} ({certainty:.1%} certain) ###"
print(len(output)*"#")
print(len(output)*"#")
print(output)
print(len(output)*"#")
print(len(output)*"#")
