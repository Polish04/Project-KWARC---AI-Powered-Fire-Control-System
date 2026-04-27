# KWARC - AI-Powered Fire Control System

**Project Demo:** [Insert Link to your 20-minute YouTube/Zoom Demo Here]

## Contact
**Developer**: Bartlomiej Pacyna
**Project**: CAP 4630 - Intro to Artificial Intelligence
**Instructor**: Professor Ahmed Imteaj
**Institution**: Florida Atlantic University
**Project Link**: https://github.com/Polish04/Project-KWARC---AI-Powered-Fire-Control-System

---

## Table of Contents
* [Overview](#overview)
* [Objectives](#objectives)
* [System Architecture](#system-architecture)
* [Methodology & Pipeline](#methodology--pipeline)
* [Implementation Results](#implementation-results)
* [Project Structure](#project-structure)
* [Installation & Usage](#installation--usage)
* [Future Improvements](#future-improvements)
* [AI Disclosure](#ai-disclosure)

---

## Overview
**KWARC** (Kinetic Weapon AI Recognition & Calculation) is an advanced tactical fire control system that bridges the gap between computer vision and actionable ballistics intelligence. The application utilizes a hybrid machine learning pipeline to detect armored vehicles in real-time, classify their specific variants, and dynamically calculate firing solutions (Lead and Elevation) based on environmental data and target range.

### Key Features
* 🎯 **Hybrid AI Pipeline**: Separates object detection and image classification to optimize both speed and accuracy.
* 🧮 **Dynamic Ballistics Engine**: Calculates Elevation and Lead (in MILs) using real-time inputs.
* 🖥️ **Tactical GUI**: A modern, low-light Heads-Up Display built natively with CustomTkinter.
* 🛡️ **Safe-AI Verification**: Built-in confidence thresholds (`p_conf`) to ensure reliable intelligence reporting.
* 📚 **External Intelligence Database**: Links visual classification to a custom database (`Tactical_database.py`) for vehicle specifications and threat levels.

---

## Objectives

### What is the problem you are solving?
In tactical environments, operators suffer from information overload. Identifying the specific model of an armored threat (e.g., T-72 vs. T-90) takes critical seconds, and manually calculating firing solutions based on wind, temperature, and range introduces human error. KWARC automates the cognitive load of vehicle recognition and ballistics math, providing immediate, actionable data.

### Why is this problem important?
* **Situational Awareness**: Differentiating between allied and adversary vehicle variants prevents friendly fire and dictates engagement tactics.
* **Processing Trade-offs**: Standard AI models struggle to do *both* real-time tracking and high-fidelity classification simultaneously without dropping frame rates. KWARC solves this via its hybrid approach.

---

## System Architecture

KWARC evaluates the environment using the **PEAS Framework** (Performance, Environment, Actuators, Sensors):
* **Performance**: Detection frame rate (FPS), classification accuracy, calculation precision.
* **Environment**: Combat footage, dynamic weather conditions (Wind, Temp, Pressure), varying ranges.
* **Actuators**: GUI visual updates, targeting brackets, real-time firing solution readouts.
* **Sensors**: OpenCV video processing (simulated optics), user input fields.

---

## Methodology & Pipeline

To balance processing speed with high accuracy, KWARC utilizes a **Two-Stage Machine Learning Pipeline**:

### Stage 1: The Spotter (Object Detection)
* **Model**: YOLOv8 Nano (`KWARTZ_Spotter.pt`)
* **Size**: 6MB
* **Role**: A highly optimized, lightweight model trained solely to locate the general shape of armored vehicles and draw bounding boxes. Its small size ensures high FPS for real-time video tracking.

### Stage 2: The Classifier (Specific Recognition)
* **Model**: YOLOv8 Small - Classification (`classify_best.pt`)
* **Size**: 10MB
* **Role**: A deeper neural network that analyzes the cropped bounding box provided by the Spotter. It uses heavier feature extraction to determine the specific vehicle chassis (e.g., M1 Abrams, Leopard 2).

---

## Implementation Results

### Key Observations
* ✅ **High Frame Rate Maintenance**: By offloading classification to a secondary model, the primary detection loop maintains smooth video playback.
* ✅ **Reliable Integration**: OpenCV successfully interfaces with CustomTkinter without thread-blocking.
* ✅ **Modular Data**: Utilizing an external `Tactical_database.py` allows for intelligence updates without needing to retrain the neural networks.

### Challenges Faced
1. **Model Bloat vs. Speed**
   * *Challenge*: Trying to train one massive model to do both detection and classification caused severe lag.
   * *Solution*: Implemented the two-stage hybrid pipeline (Nano Spotter + Small Classifier).
2. **GUI Mainloop Conflicts**
   * *Challenge*: Standard Tkinter froze when running infinite video processing loops.
   * *Solution*: Optimized OpenCV frame updates using recursive `.after()` calls in CustomTkinter.
3. **Environment Setup**
   * *Challenge*: Dependency conflicts across different machines.
   * *Solution*: Standardized the build using a strict `requirements.txt` to ensure cross-platform compatibility.

---

## Project Structure

```text
Project_KWARC/
├── Kwartz_GUI.py             # Main application script & GUI loop
├── Tactical_database.py      # Vehicle intelligence and spec database
├── KWARTZ_Spotter.pt         # Stage 1: YOLOv8n object detection weights
├── classify_best.pt          # Stage 2: YOLOv8s-cls classification weights
├── requirements.txt          # Python dependencies
├── .gitignore                # Excluded cache and IDE files
└── README.md                 # Project documentation
