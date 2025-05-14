import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import os

# Step 1: Set dataset path and parameters
dataset_path = 'augements/'  # Make sure your dataset is organized into subfolders by class
image_size = (224, 224)
batch_size = 32
num_classes = len(os.listdir(dataset_path))  # Assumes each subfolder is a class

# Step 2: Data augmentation and loading
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Step 3: Load pre-trained model and build classification model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze the base model layers

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

# Step 4: Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# Step 5: Train the model
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)
# Step 6: Save the model
model.save('banana_plant_classifier.h5')
print("✅ Model trained and saved as 'banana_plant_classifier.h5'")
