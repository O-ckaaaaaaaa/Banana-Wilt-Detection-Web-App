# 🍌 Banana Wilt Detection Mobile App

An offline AI-powered Android application that helps farmers detect **Banana Bacterial Wilt (BBW)** from plant images using a locally deployed machine learning model. Built with **Java and XML**, this app runs completely offline—ideal for rural and remote agricultural settings.

---

## 📱 Features

- 📷 **Capture or Upload Images**  
  Detect banana wilt from real-time camera input or gallery images.

- 🤖 **Offline Detection with ML**  
  A lightweight machine learning model runs on-device using **TensorFlow Lite**, requiring no internet connection.

- 🩺 **Instant Diagnosis**  
  The app analyzes images and gives results within seconds, with confidence scores.

- 📚 **Educational Info**  
  Learn about BBW symptoms, prevention, and treatment methods within the app.

---

## 🌾 Why This App?

Banana Bacterial Wilt (BBW) is one of the most devastating diseases affecting banana plantations in East and Central Africa. Early detection is critical to minimize spread and loss, but many rural areas lack expert access or connectivity.

This app bridges that gap by offering:
- 📡 **Zero dependency on internet or cloud**
- 💰 **Cost-effective solution for smallholder farmers**
- 📊 **Data-driven insights at your fingertips**

---

## 🛠️ Technical Overview

- **Frontend:** Java & XML (Android SDK)
- **Machine Learning Model:** TensorFlow / PyTorch → TensorFlow Lite (.tflite)
- **Storage:** Local file system for saving diagnosis history and images
- **Dependencies:**  
  - TensorFlow Lite
  - AndroidX libraries
  - Glide or Picasso (for image handling)

---

## 🚀 How It Works

1. Launch the app and take or upload a banana plant image.
2. The image is processed by the offline AI model.
3. Results show whether the plant is healthy or infected with BBW.
4. Access more info on disease prevention and treatment.

---

## 🧪 Model Training (Brief)

- Dataset: Annotated images of healthy and BBW-infected banana plants
- Model Type: CNN-based classifier (e.g., MobileNetV2)
- Optimized & converted to `.tflite` format for Android integration

---

## 👥 Target Audience

- Banana farmers in rural and semi-urban areas
- Agricultural extension workers
- NGOs and environmental bodies
- Educators and researchers in smart farming

---

## 📦 Future Improvements

- 🌍 Geotagging of infected areas
- 📊 Disease report dashboard
- 🗣️ Multi-language support (English, Luganda, more)
- 🔁 Model update feature via APK

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and open a pull request.

---

## 🧑‍💻 Developer

**[Murungi Oscar]**  
Email: murungioscar2022@gmail.com  
GitHub: (https://github.com/o-ckaaaaaaaa)

