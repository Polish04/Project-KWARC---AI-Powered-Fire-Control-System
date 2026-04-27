# KWARC - AI-Powered Fire Control System

**Project Demo:** [Insert Link to your 20-minute YouTube/Zoom Demo Here]

## Contact
* **Developer**: Bartlomiej Pacyna
* **Project**: CAP 4630 - Intro to Artificial Intelligence
* **Instructor**: Professor Ahmed Imteaj
* **Institution**: Florida Atlantic University
* **Project Link**: [https://github.com/Polish04/Project-KWARC](https://github.com/Polish04/Project-KWARC---AI-Powered-Fire-Control-System)

---

## Table of Contents
* [Overview](#overview)
* [Objectives](#objectives)
* [Model Architecture](#model-architecture)
* [Dataset](#dataset)
* [Performance Metrics](#performance-metrics)
* [Challenges Faced](#challenges-faced)
* [Technologies Used](#technologies-used)
* [Project Structure](#project-structure)
* [Installation & Usage](#installation--usage)
* [References](#references)

---

## Overview
**KWARC** is an advanced tactical fire control system that bridges the gap between computer vision and actionable ballistics intelligence. The application utilizes a hybrid machine learning pipeline to detect armored vehicles in real-time, classify their specific variants, and dynamically calculate firing solutions (Lead and Elevation) based on environmental data and target range. 

The ballistics engine and sensor inputs are modeled assuming integration with the **M1A2 SEPv3 Abrams** platform. All environmental and firing calculations are calibrated to standard 120mm smoothbore ballistics as the default origin.

> **⚠️ AI LIMITATION NOTICE:** The current classification model (`classify_best.pt`) was trained on a custom, hand-built dataset with a limited number of samples. As a result, the AI may occasionally struggle to confidently classify vehicles in fast-moving video feeds, highly obscured environments, or from incomplete angles. This is a known limitation of the training data volume, rather than the system's pipeline architecture.

### Key Features
* 🎯 **Hybrid AI Pipeline**: Separates object detection and image classification to optimize both speed and accuracy.
* 🧮 **Dynamic Ballistics Engine**: Calculates Elevation and Lead using custom inputs. 
* 🖥️ **GUI**: Modern tactical display built natively with CustomTkinter.
* 🛡️ **Safe-AI Verification**: Built-in confidence thresholds (`p_conf`) to ensure reliable intelligence reporting.
* 📚 **External Intelligence Database**: Links visual classification to a custom database (`Tactical_database.py`) for vehicle specifications and threat levels.

---

## Objectives

### What is the problem you are solving?
In tactical environments, operators suffer from information overload. Identifying the specific model of an armored threat (e.g., T-72 vs. T-90) takes critical seconds, and manually calculating firing solutions based on wind, temperature, and range introduces human error. KWARC automates the cognitive load of vehicle recognition and ballistics math, providing immediate, actionable data.

### Why is this problem important?
* **Crew Reduction & Automation**: By handling complex identification and targeting calculations, KWARC paves the way for reducing crew size requirements in next-generation armor platforms. It automates tasks traditionally managed by a dedicated gunner or vehicle commander.
* **Situational Awareness**: Differentiating between allied and adversary vehicle variants in split seconds prevents friendly fire and dictates immediate engagement tactics.
* **Processing Trade-offs**: Standard AI models struggle to do *both* real-time tracking and high-fidelity classification simultaneously. KWARC solves this via its hybrid approach.

---

## Model Architecture

KWARC employs a **Dual-Stage YOLOv8 Hybrid** architecture to balance real-time tracking with high-fidelity recognition:

### Stage 1: The Spotter (Object Detection)
* **Base Model**: YOLOv8 Nano (`YOLOv8n`)
* **Role**: Optimized to locate the general shape of armored vehicles and draw bounding boxes.
* **Input Size**: Standard video frame resolution (scaled to 640×640)
* **Feature Extraction**: Lightweight CSPDarknet backbone.
* **Model Size**: ~6 MB (ideal for edge deployment).
* **Inference Time**: Ultra-low latency for real-time continuous video feeds.

### Stage 2: The Classifier (Specific Recognition)
* **Base Model**: YOLOv8 Small Classification (`YOLOv8s-cls`)
* **Role**: Analyzes the cropped bounding box provided by the Spotter to determine the specific vehicle chassis.
* **Input Size**: Resized to 224×224 RGB.
* **Output Layer**: Softmax probability distribution across 12 custom vehicle classes.
* **Model Size**: ~10 MB.

---

## Dataset

The training data was split into two distinct datasets. The classifier dataset was aggregated via web-scraping:

### Stage 1: Spotter Dataset (Object Detection)
* **[INSERT NUMBER] images** of general combat footage and vehicles.
* **Target Class**: 1 primary class ("Armored Vehicle").

### Stage 2: Classifier Dataset (Specific Recognition)
* **[INSERT NUMBER] cropped images** focusing exclusively on vehicle chassis geometry.
* **Target Classes**: 12 distinct vehicle classes such as:

---

## Performance Metrics

### Stage 1: Detection Performance (The Spotter)
* **mAP50 (Mean Average Precision)**: [e.g., 92.4%] 
* **Average Precision (P)**: [e.g., 0.89]
* **Average Recall (R)**: [e.g., 0.91]
* **Inference Time**: < 10ms per frame (60+ FPS tracking).

### Stage 2: Classification Performance (The Classifier)
* **Top-1 Accuracy**: [e.g., 88.7%] 
* **Training Epochs**: [e.g., 50] 
* **Inference Time**: < 5ms per target crop.
* *(Note: Accuracy may drop on variants with highly similar chassis, such as T-72 vs. T-90 at long distances).*

---

### Challenges Faced

1. **Overfitting to Pigmentation vs. Geometry**
   * *Challenge*: During early training phases, the classification model began to rely on pixel pigmentation rather than learning the actual geometric shape and structural features of the tanks due to falthy datasets.
   * *Impact*: The model would falsely classify a completely different vehicle just because it shared the same color palette as the training data.
   * *Solution*: Retrain a model on a custom handpicked dataset using "download all images" google extension. 



2. **Dataset Limitations & Motion Blur**

   * *Challenge*: Because the training dataset had to be entirely handpicked and manually annotated, the overall sample volume is relatively low for deep learning standards. 
   * *Impact*: The classification model occasionally struggles to classify fast-moving targets (due to motion blur) or when viewing the vehicle from heavily obscured/incomplete angles.
   * *Mitigation*: Implemented the Safe-AI confidence threshold (`p_conf`) so the system defaults to "Unknown Target" rather than guessing wildly during high-motion frames. 

---

## Technologies Used

* **Deep Learning**: Ultralytics YOLOv8 (PyTorch)
* **Computer Vision**: OpenCV (`opencv-python`)
* **GUI Framework**: CustomTkinter
* **Image Processing**: Pillow (`PIL`)
* **Development Environment**: Python 3.10+, PyCharm

---

## Project Structure

Project_KWARC/
* ├── Kwartz_GUI.py             # Main application script & GUI loop
+ ├── Tactical_database.py      # Vehicle intelligence and spec database
* ├── KWARTZ_Spotter.pt         # Stage 1: YOLOv8n object detection weights
* ├── classify_best.pt          # Stage 2: YOLOv8s-cls classification weights
* ├── requirements.txt          # Python dependencies
* ├── .gitignore                # Excluded cache and IDE files
* └── README.md                 # Project documentation

---

## Installation & Usage

1. Clone the repository:
   git clone https://github.com/Polish04/Project-KWARC---AI-Powered-Fire-Control-System
   cd Project-KWARC---AI-Powered-Fire-Control-System

2. Install dependencies:
   pip install -r requirements.txt

3. Run the system:
   python Kwartz_GUI.py

---

## References

1. Ultralytics YOLOv8 Documentation - https://docs.ultralytics.com
2. CustomTkinter UI Library - https://customtkinter.tomschimansky.com
3. OpenCV Python Documentation - https://docs.opencv.org
4. Dataset Aggregation - "Download All Images" browser extension.
5. AI Tool: Google Gemini (Model: Gemini 3 Pro)
