# Ultimate QR Pro 🚀

Ultimate QR Pro is a feature-rich, high-performance desktop application designed for seamless QR Code generation, real-time scanning, and history management. Built with a modern dark-themed UI using **CustomTkinter**, it integrates **OpenCV** for lightning-fast camera decoding and **qrcode** for high-resolution vector and raster outputs.

---

## ✨ Key Features

### 🎨 Advanced QR Generation
* **Multiple Modes:** Supports Text/URLs, WiFi configurations (SSID, Password, Encryption, Hidden), Emails (To, Subject, Body), and vCards (Contact info).
* **High-Res Export:** Save QR codes in sharp **PNG** or native vector **SVG** formats up to 1024px.
* **Custom Styling:** Full control over foreground and background colors.
* **Branding:** Seamlessly embed custom logos/avatars in the center of the QR code with smart aspect-ratio handling.

### 📷 Smart Scanning & Decoding
* **Live Camera Stream:** High-speed real-time webcam scanning with auto-bounding boxes and success beep indicators.
* **Image Decoder:** Extract QR data directly from local images (`.png`, `.jpg`, `.jpeg`, etc.).
* **Multi-Camera Support:** Switch dynamically between index 0, 1, or 2 (Webcams/External cams).

### 🗄️ Data Management & Sharing
* **Live History Log:** Tracks every generated/scanned QR item with precise timestamps and instant search filters.
* **Clipboard Integration:** Double-click any history item to copy its raw contents instantly.
* **Batch Export:** Export your local history database anytime into standard **CSV** or **TXT** formats.
* **Instant Social Share:** Quick web-redirects to share extracted text via WhatsApp and Facebook.

---

## 🛠️ Tech Stack & Dependencies

The project is built entirely in Python using the following modules:
* **UI Framework:** `customtkinter` (Modern UI wrapper over Tkinter)
* **Computer Vision:** `opencv-python` (For fast camera frame capturing and QR decoding)
* **Core Logic:** `qrcode` & `pillow` (For custom QR generation and logo pasting)
* **Standard Libraries:** `json`, `csv`, `threading`, `urllib`, `webbrowser`, `winsound`

---

## 📂 Project Architecture

The application follows a clean, decoupled modular structure:

```text
UltimateQRPro/
│
├── main.py              # Application Entry Point & Core Class Initialization
├── config.py            # Theme Settings, App Paths, and Global Configurations
├── ui_panels.py         # UI Layouts (Left Settings, Center Camera, Right History)
└── qr_logic.py          # Backend Logic (Generation, Scanning, Sharing, and IO Operations)
----
## 🚀 Getting Started

### Option 1: Running from Source Code (For Developers)

1. **Clone the repository:**
```bash
   git clone [https://github.com/YOUR_USERNAME/ultimate-qr-pro.git](https://github.com/YOUR_USERNAME/ultimate-qr-pro.git)
   cd ultimate-qr-pro

2. Install required dependencies:pip install customtkinter opencv-python qrcode pillow
3.Run the application:
---
Option 2: Running the Executable App (For Users)
No Python setup required!

Head over to the Releases section.

Download Ultimate-QR-Pro-v1.0.zip.

Extract the ZIP file and run main.exe.
---
📸 Screenshots

