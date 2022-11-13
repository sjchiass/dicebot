import tensorflow as tf
from tensorflow import keras
import numpy as np
import argparse
from PIL import Image

from pathlib import Path

data = []
labels = []
working_dir = Path()
for path in working_dir.glob("./raw_pics/**/*.jpg"):
    img_array = np.asarray(Image.open(path).convert("L"))
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    data.append(img_array)
    labels.append(int(str(path).split("/")[-2]))

model = keras.models.load_model("./save_at_50.h5")

# Combine all images together
data = np.concatenate(data, axis=0)

# Make predictions
predictions = model.predict(data)

# Keep track of correct guesses
correct_guesses = 0
errors = []
print(f"| Correct | Guess | Difference |")
print(f"|---------|-------|------------|")
for o, l in zip(range(predictions.shape[0]), labels):
    # Slice predictions array for one time along axis 0 (the observations)
    obs = predictions[o, :]
    # Make a pretty box for current word and include what should be the 
    # correct number of vowels
    # Extract the model's guess from the predictions
    guess = np.argmax(obs.flatten()) + 6 # Does it maybe start guessing at 0?
    if guess == l:
        correct_guesses += 1
        good_guess = True
    else:
        good_guess = False
    print(f"| {l:7d} | {guess:5d} | {guess-l:10d} |")
    errors.append(guess-l)
print(f"|---------|-------|------------|")
# Count number of correct guesses, out of all words given
mse = sum([x**2 for x in errors])/len(errors)
score = f"%%% SCORE: {correct_guesses:2}/{len(labels):2} ({correct_guesses/len(labels):.2%}) MSE: {mse:5.2f} %%%"
if correct_guesses == len(labels):
    score = score.replace(" %%%", " GOOD BOI! %%%")
print(len(score)*"%")
print(score)
print(len(score)*"%")
