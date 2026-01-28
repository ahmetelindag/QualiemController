# QualiemController 


![Platform](https://img.shields.io/badge/Platform-MacOS%20%7C%20Windows-lightgrey?style=for-the-badge&logo=apple)


Desktop prototype for **PCB & product quality inspection**, built with **Python**.

 **Interface Preview**
![WhatsApp Image 2025-12-25 at 11 33 35](https://github.com/user-attachments/assets/766a28fc-3d85-4120-a5a7-41abf7a5588a)
![WhatsApp Image 2025-12-25 at 11 46 25](https://github.com/user-attachments/assets/0dbe93df-6adb-4d34-b121-a41e218fa7f8)
<img width="1023" height="686" alt="image" src="https://github.com/user-attachments/assets/8a128c8d-d29a-44da-a7d9-fd824b08090b" />


 

**Key Modules:**
1.  **Incoming Quality Control (IQC):** Inspection of bare PCBs for surface scratches and copper defects.
2.  **Final Quality Control (FQC):** Verification of assembled boards (component presence, placement accuracy) using reference image comparison.
3.  **Quality Analytics:** Tracking inspection history and basic defect reporting.
4.  **Interactive Inspection:**
    * Zoomable/Clickable image viewers for detailed defect analysis.
    * Visual "Pass/Fail" feedback loop.

> Note:   this project is mainly for learning and portfolio purposes
---

## 🧱 Tech Stack

- Python 3.12
- PyQt6 (desktop UI)
- OpenCV + NumPy (image processing)
- SQLite (local database)

---

##  Current Scope 

- Desktop GUI with 3 modes:
  1.  bare PCB inspection
  2. Final assembled board inspection
  3. Inspection history & basic reporting

- Basic image processing pipelines for:
  - Edge detection, thresholding, simple defect region detection
  - Reference image differencing for final boards

- SQLite-backed storage for:
  - Inspection results
  - Basic metadata (board code, supplier, result, defect count, etc.)

---

## Future Directions

- Mechanical part inspection (surface defects, dimensional checks)
- Component counting & presence/absence checks
- Barcode / QR / serial number verification
- AI-assisted defect classification
- Supplier quality analytics (defect density, PPM, scorecards)
- Integration with ERP  systems

> Note: Some of these advanced features are planned as **closed-source** and will not be fully exposed in this public repository.

---

*Developed by Ahmet Elindağ*
ahmetelindag@gmail.com
