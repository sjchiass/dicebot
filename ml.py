import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# The code is from these two guides:
# flow: https://keras.io/examples/vision/image_classification_from_scratch/
# model: https://keras.io/examples/vision/mnist_convnet/

image_size = (100, 100)
batch_size = 32
classes = [str(x) for x in range(6, 36+1)]

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "./training_data",
    labels="inferred",
    label_mode="int",
    class_names=classes,
    color_mode="grayscale",
    image_size=image_size,
    batch_size=batch_size,
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "./raw_pics",
    labels="inferred",
    label_mode="int",
    class_names=classes,
    color_mode="grayscale",
    image_size=image_size,
    batch_size=batch_size,
)

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

# Unlike my vowel counter, this requires a slightly stronger model
def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    
    x = layers.Rescaling(1.0 / 255)(inputs)
    # Augmentation
    x = layers.RandomFlip()(x)
    x = layers.RandomRotation(0.3)(x)
    # Convolutions
    x = layers.Conv2D(128, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    previous_block_activation = x  # Set aside residual
    for size in [256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)
        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual
    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.5)(x)
    
    outputs = layers.Dense(len(classes), activation="softmax")(x)
    return keras.Model(inputs, outputs)


model = make_model(input_shape=image_size + (1,), num_classes=len(classes))

epochs = 50

# Save the models to use with infer.py
callbacks = [
    keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
]

model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.fit(
    train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
)
