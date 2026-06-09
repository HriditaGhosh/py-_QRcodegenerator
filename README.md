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
## 📁 Project Structure

```text
UltimateQRPro/
│
├── main.py              # Main application source code
├── qr_pro_data.json     # Scan history database (auto-generated)
├── requirements.txt     # Project dependencies
├── screenshots/         # Application screenshots
│   ├── home.png
│   ├── scanner.png
│   └── generator.png
│
└── README.md
```

---

## 🚀 Getting Started

### Option 1: Running from Source Code (For Developers)

#### 1. Clone the repository

```bash
git clone https://github.com/HriditaGhosh/UltimateQRPro.git
cd UltimateQRPro
```

#### 2. Install required dependencies

```bash
pip install customtkinter opencv-python qrcode pillow
```

#### 3. Run the application

```bash
python main.py
```

---

### Option 2: Running the Executable App (For Users)

No Python installation required.

1. Go to the **Releases** section.
2. Download **Ultimate-QR-Pro-v1.0.zip**.
3. Extract the ZIP file.
4. Run **main.exe**.

---

## 📸 Screenshots
<img width="1919" height="1007" alt="Screenshot 2026-06-06 151042" src="https://github.com/user-attachments/assets/90ad93ea-ed65-4018-9986-cd7c49f9c1d1" />
<img width="1919" height="1016" alt="Screenshot 2026-06-06 151826" src="https://github.com/user-attachments/assets/8864713c-e7dd-4585-b2ae-ef8b25922a52" />
<img width="1404" height="1001" alt="Screenshot 2026-06-06 151555" src="https://github.com/user-attachments/assets/e8f31239-5af2-4649-af6d-0c95cf4a06ae" />
<img width="1177" height="1013" alt="Screenshot 2026-06-06 151532" src="https://github.com/user-attachments/assets/0e65cc4f-32d1-4739-91e4-2b1515f26e31" />
<img width="1903" height="1000" alt="Screenshot 2026-06-06 151303" src="https://github.com/user-attachments/assets/3c69b4b6-a7c0-47f3-84c6-5d547ff0fc39" />








