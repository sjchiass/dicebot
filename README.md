# Dicelot the Dicebot

## Cardboard-based random number generator

This project shakes dice with a servo motor and then takes a photo to count the dice for you.

The ML part uses synthetic data with augmentation to get extra value out of a small training set. The model is right roughly 80% of the time on the test set. When it's wrong it's usually by 1.

![dice_shaking.gif](A GIF of the robot shaking dice)

![inference_example.jpg](The robot's guess)

## Workflow

There a bit of data collection to get started, but 

  * Data preparation
    * Take 100+ photos of dice, label them by their total 6d6 value, and then keep these as your test set (so that you know how well the robot does with real photos).
    * Prepare your fake data
      * Take 10+ images of the botle without dice to act as a background
      * Take a few more images with dice, cut out each die separately, and organize them all by value.
      * Run the `generate_images.py` script to generate nearly 60,000 permutations of dice photos
  * Run the model: `ml.py` trains a generic convolution neural network on the fake data, while rotating and flipping photos to push the data a bit further.
  * Use `convert.py` to transform the final model into a light `tflite` version so that it runs on the Raspberry Pi
  * Use the bot!
    * Run `ShakeDice.py` to shake some dice!
    * Use `raspistill` to take a new photo!
    * Run `pi_infer.py` to evaluate the model on the new photo!

## Hardware

This is all made with Raspberry Pi and Python There's a Raspberry Pi 2B with `tflite` to run `tensorflow` models and a Raspberry Pi Pico running circuitpython to control the servo motor.

The chassis (if you can call it that) is a cut-up cardboard box, some wooden sticks, and some hot glue. It's all surprisingly rigid.

## Data Generation

This is what real dice look like. It's a 100x100 jpg converted to grayscale when read by Python.

![real_dice_example.jpg](An example of real dice)

Pillow takes some photos of the empty bottle and pastes on top some cut-outs of dice. By changing the position and value of the dice, a lot of fake data can be made.

This is what a fake image looks like.

![fake_dice_example.jpg](An example of fake dice)

