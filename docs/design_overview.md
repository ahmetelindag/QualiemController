# System Design Overview 

## 1. Architectural Pattern
QualiemController follows a modular **Layered Architecture**, separating the user interface (Presentation), business logic (Application), and data management (Persistence). This ensures maintainability and scalability.

### High-Level Architecture Diagram
```text
+-----------------------+       +-------------------------+       +---------------------+
|   Presentation Layer  |       |    Application Layer    |       |     Data Layer      |
|      (PyQt6 UI)       | <---> |    (Core Logic / CV)    | <---> |   (SQLite / Files)  |
+-----------------------+       +-------------------------+       +---------------------+
| - MainWindow          |       | - ImageProcessor        |       | - DatabaseManager   |
| - InspectionPage      |       |   (OpenCV + NumPy)      |       | - inspection.db     |
| - QualityPage         |       | - Align & Subtract      |       | - Image Files       |
| - HistoryPage         |       | - Defect Detection      |       |                     |
+-----------------------+       +-------------------------+       +---------------------+
```
2. Component Details
A. Presentation Layer (UI)

The interface is built using PyQt6 with a custom dark theme (styles.py).

MainWindow: Acts as the main container using QStackedWidget to switch between different functional pages.

Pages:

DashboardPage: High-level summary and shortcuts.

InspectionPage: The core operational screen for loading images and running tests.

QualityPage: SPC (Statistical Process Control) charts using Matplotlib embedded in Qt.

HistoryPage: A tabular view of past inspection logs.

B. Application Layer (Core Logic)

This is the brain of the system, located in src/core/image_processor.py.

Image Alignment (Registration):

Uses ORB (Oriented FAST and Rotated BRIEF) to detect keypoints in both Reference and Test images.

Computes a Homography matrix to warp the Test image onto the Reference coordinate system.

Defect Detection:

Absolute Difference: Calculates |Reference - Test|.

Thresholding: Converts the difference map to binary (Black/White).

Morphology: Applies Opening (Erosion followed by Dilation) to remove noise (dust, lighting artifacts).

C. Data Layer (Persistence)

Database: A lightweight SQLite database (inspection.db) is used to store logs.

Schema: Stores filename, timestamp, defect_count, and status (PASS/FAIL).

3. Data Flow Pipeline
Input: User loads a "Golden Sample" (Reference) and a "Defective Unit" (Test).

Preprocessing: Both images are converted to Grayscale to reduce computational load.

Registration: The system calculates the geometric transformation required to align the Test image.

Comparison: The aligned test image is subtracted from the reference.

Analysis: The resulting "Difference Map" is analyzed for white pixel blobs (defects).

Output:

Visual Result displayed on UI.

Defect count logged to Database.

Real-time statistics updated on Dashboard.

