# Real-Time-Optical-Character-Recognition
This project involves the development of a real-time Optical Character Recognition (OCR) system using Tesseract, OpenCV, and machine learning algorithms. The system is capable of accurately extracting text from various types of documents and images.

## Overview

This project was developed during a six-week summer internship at GAIL (India) Ltd. The primary objective was to create a robust OCR system that can preprocess images, reduce noise, and accurately convert them into machine-readable text.


## Features
- Real-time OCR processing
- Image preprocessing (noise reduction, thresholding, edge detection)
- Integration of machine learning models to enhance OCR accuracy


## Technologies Used
- Tesseract
- OpenCV
- Python


## Prerequisites 

- **Tesseract installed:**
  
  Install tesseract from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
  
  > pip install pytesseract

- **OpenCV installed:**
  
  > pip install opencv

- **NumPy installed:**

  > pip install numpy


## Usage 

To run the OCR system (via command line), use the following command :

> _python Main.py -t "path to tesseract executable file"_

Replace "path to tesseract executable file" with the actual path to your Tesseract executable.

Path example (Windows): "C:\Program Files (x86)\Tesseract\tesseract.exe"


## Screenshots

- **Command Line Input:**
  
  ![Command Line Input](https://github.com/user-attachments/assets/752c191e-a70f-4a86-acba-467816bfb4cf)


- **OCR:**

  ![OCR](https://github.com/user-attachments/assets/83441c59-1a06-44c4-a820-8e2d6a160c8e)


- **Text Capture from OCR Detection**

  ![Text Capture from OCR Detection](https://github.com/user-attachments/assets/3ae063a6-4c11-4657-9a3a-75e25f3c6d0f)


