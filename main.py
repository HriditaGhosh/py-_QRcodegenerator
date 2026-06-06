import cv2
import customtkinter as ctk
from qr_logic import QRLogic
from ui_panels import UIPanels

class UltimateQRPro(UIPanels, QRLogic, ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate QR Pro")
        self.geometry("1340x720")
        self.minsize(1200, 650)

        # ── State ──────────────────────────────────────────────
        self.history_data  = self.load_history()   
        self.camera_running = False
        self.cap            = None
        self.qr_color       = "#000000"
        self.bg_color       = "#ffffff"
        self.logo_path      = None
        self.last_scanned   = ""
        self.current_img    = None
        self.mode           = "Text/URL"
        self.camera_index   = 0
        self.scanned_count  = 0
        self.qr_detector    = cv2.QRCodeDetector()
        self.status_timer_id = None

        # UI Setup (From UIPanels)
        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_left_panel()
        self._build_center_panel()
        self._build_right_panel()
        self.refresh_ui_logs()

if __name__ == "__main__":
    app = UltimateQRPro()
    app.mainloop()