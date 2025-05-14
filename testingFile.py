from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

from augement import train_generator

# Load the saved model
model = load_model('banana_plant_classifier.h5')

# Load and preprocess the test image
img_path = '6.jpg'  # Replace this with your actual image path
img = image.load_img(img_path, target_size=(224, 224))  # ✅ Resize to 224x224
img_array = image.img_to_array(img)
img_array = img_array / 255.0  # Normalize
img_array = np.expand_dims(img_array, axis=0)  # Shape becomes (1, 224, 224, 3)

# Predict
result = model.predict(img_array)

# Get class label
class_indices = train_generator.class_indices  # From training script
class_names = list(class_indices.keys())
predicted_class = class_names[np.argmax(result)]

print("Predicted class:", predicted_class)

