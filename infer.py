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

model = keras.models.load_model("./save_at_14.h5")

# Combine all images together
data = np.concatenate(data, axis=0)

# Make predictions
predictions = model.predict(data)

# Keep track of correct guesses
correct_guesses = 0
for o, l in zip(range(predictions.shape[0]), labels):
    # Slice predictions array for one time along axis 0 (the observations)
    obs = predictions[o, :]
    # Make a pretty box for current word and include what should be the 
    # correct number of vowels
    reference = f"*** has {l} ***"
    print(len(reference)*"*")
    print(reference)
    # Extract the model's guess from the predictions
    guess = np.argmax(obs.flatten()) + 6 # Does it maybe start guessing at 0?
    if guess == l:
        correct_guesses += 1
        good_guess = True
    else:
        good_guess = False
    print(f"==> Best guess is  {guess:2} {'PASS' if good_guess  else 'FAIL'}   <==")
    # Print guess as long as they're greater than a hundreth of a percent
    for n, i in enumerate(obs.flatten()):
        if f"{i:.0%}" != "0%":
            print(f"`-> % certain that {l} has {n+6} vowels: {i:3.0%}")
# Count number of correct guesses, out of all words given
score = f"%%% SCORE: {correct_guesses:2}/{len(labels):2} ({correct_guesses/len(labels):.2%}) %%%"
if correct_guesses == len(labels):
    score = score.replace(" %%%", " GOOD BOI! %%%")
print(len(score)*"%")
print(score)
print(len(score)*"%")
