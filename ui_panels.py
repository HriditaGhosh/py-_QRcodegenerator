import tkinter as tk
import customtkinter as ctk

class UIPanels:
    # ── Left panel ────────────────────────────────────────────
    def _build_left_panel(self):
        lp = ctk.CTkFrame(self, width=260, corner_radius=0)
        lp.grid(row=0, column=0, sticky="nsew")
        lp.grid_propagate(False)
        self.left_panel = lp

        ctk.CTkLabel(lp, text="GENERATE QR", font=("Arial", 18, "bold")).pack(pady=(14, 6))

        self.mode_selector = ctk.CTkSegmentedButton(
            lp, values=["Text/URL", "Email", "WiFi", "vCard"],
            command=self.change_mode, width=230)
        self.mode_selector.set("Text/URL")
        self.mode_selector.pack(pady=6, padx=14)

        self.input_frame = ctk.CTkScrollableFrame(lp, height=200, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=14, pady=4)
        self.show_text_inputs()

        ctk.CTkLabel(lp, text="Error level").pack()
        self.error_var = ctk.StringVar(value="H (30%)")
        ctk.CTkOptionMenu(lp, values=["L (7%)", "M (15%)", "Q (25%)", "H (30%)"],
                          variable=self.error_var, width=230).pack(pady=2)

        ctk.CTkLabel(lp, text="Export size").pack()
        self.size_var = ctk.StringVar(value="512 px")
        ctk.CTkOptionMenu(lp, values=["128 px", "256 px", "512 px", "1024 px"],
                          variable=self.size_var, width=230).pack(pady=2)

        btn_row = ctk.CTkFrame(lp, fg_color="transparent")
        btn_row.pack(pady=6)
        self.qr_color_btn = ctk.CTkButton(btn_row, text="QR Color",  width=70,
                                          fg_color="#000000", command=self.pick_qr_color)
        self.qr_color_btn.grid(row=0, column=0, padx=3)
        self.bg_color_btn = ctk.CTkButton(btn_row, text="BG Color",  width=70,
                                          fg_color="#ffffff", text_color="black", command=self.pick_bg_color)
        self.bg_color_btn.grid(row=0, column=1, padx=3)
        ctk.CTkButton(btn_row, text="Logo", width=60,
                      command=self.pick_logo).grid(row=0, column=2, padx=3)

        self.logo_label = ctk.CTkLabel(lp, text="No logo", text_color="gray")
        self.logo_label.pack()

        ctk.CTkButton(lp, text="CREATE QR", fg_color="#2ecc71",
                      command=self.generate_qr, width=230).pack(pady=6, padx=14)

        btn_row2 = ctk.CTkFrame(lp, fg_color="transparent")
        btn_row2.pack(pady=2)
        self.save_png_btn = ctk.CTkButton(btn_row2, text="Save PNG", width=110,
                                          fg_color="#3498db", state="disabled",
                                          command=lambda: self.save_qr("png"))
        self.save_png_btn.grid(row=0, column=0, padx=4)
        self.save_svg_btn = ctk.CTkButton(btn_row2, text="Save SVG", width=110,
                                          fg_color="#9b59b6", state="disabled",
                                          command=lambda: self.save_qr("svg"))
        self.save_svg_btn.grid(row=0, column=1, padx=4)

        ctk.CTkButton(lp, text="Switch Theme", fg_color="transparent",
                      border_width=1, command=self.toggle_theme,
                      width=230).pack(pady=4, padx=14)
        ctk.CTkButton(lp, text="QUIT APP", fg_color="#e74c3c",
                      command=self.on_closing, width=230).pack(side="bottom", pady=14, padx=14)

    # ── Center panel ──────────────────────────────────────────
    def _build_center_panel(self):
        cp = ctk.CTkFrame(self, fg_color="transparent")
        cp.grid(row=0, column=1, sticky="nsew", padx=(15, 10), pady=15)
        cp.grid_columnconfigure(0, weight=1)
        cp.grid_rowconfigure(0, weight=7)
        cp.grid_rowconfigure(1, weight=3)

        self.cam_frame = ctk.CTkFrame(cp, fg_color="black", corner_radius=12)
        self.cam_frame.grid(row=0, column=0, pady=(0, 15), sticky="nsew")
        self.cam_frame.grid_propagate(False)

        self.cam_label = ctk.CTkLabel(self.cam_frame, text="CAMERA STANDBY", fg_color="black")
        self.cam_label.pack(fill="both", expand=True)

        bottom = ctk.CTkFrame(cp, fg_color="transparent")
        bottom.grid(row=1, column=0, sticky="nsew")
        bottom.grid_columnconfigure(1, weight=1)
        bottom.grid_rowconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(bottom, text="QR PREVIEW",
                                          width=180, height=180,
                                          fg_color="#1a1a1a", corner_radius=12)
        self.preview_label.grid(row=0, column=0, padx=(0, 15), sticky="ns")

        ctrl = ctk.CTkFrame(bottom, fg_color="transparent")
        ctrl.grid(row=0, column=1, sticky="nsew")

        lbl_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        lbl_row.pack(anchor="w", fill="x", pady=(5, 5))
        
        self.scanned_lbl = ctk.CTkLabel(lbl_row, text="Scanned: 0", font=("Arial", 14, "bold"))
        self.scanned_lbl.pack(side="left")
        
        self.status_lbl = ctk.CTkLabel(lbl_row, text="", font=("Arial", 12, "italic"), text_color="#2ecc71")
        self.status_lbl.pack(side="left", padx=20)

        cam_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        cam_row.pack(anchor="w", pady=5)
        ctk.CTkLabel(cam_row, text="Camera:", font=("Arial", 12)).pack(side="left")
        self.cam_idx_var = ctk.StringVar(value="0")
        ctk.CTkOptionMenu(cam_row, values=["0", "1", "2"],
                          variable=self.cam_idx_var, width=70,
                          command=lambda v: setattr(self, "camera_index", int(v))
                          ).pack(side="left", padx=10)

        btn_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_row.pack(anchor="w", pady=10)
        self.start_btn = ctk.CTkButton(btn_row, text="START SCANNER",
                                       fg_color="#2ecc71", width=140,
                                       command=self.start_camera)
        self.start_btn.pack(side="left", padx=4)
        self.stop_btn  = ctk.CTkButton(btn_row, text="STOP SCANNER",
                                       fg_color="#e74c3c", width=140,
                                       state="disabled", command=self.stop_camera)
        self.stop_btn.pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Scan from Image", fg_color="#8e44ad",
                      width=140, command=self.scan_from_image).pack(side="left", padx=4)

    # ── Right panel ───────────────────────────────────────────
    def _build_right_panel(self):
        rp = ctk.CTkFrame(self, width=280)
        rp.grid(row=0, column=2, sticky="nsew", padx=(10, 10), pady=15)
        rp.grid_propagate(False)

        ctk.CTkLabel(rp, text="SCANNED LINKS", font=("Arial", 13, "bold")).pack(pady=(10, 2))
        self.links_box = tk.Listbox(rp, bg="#1a1a1a", fg="#00ff88",
                                    selectbackground="#2ecc71", height=5,
                                    relief="flat", borderwidth=0, font=("Consolas", 9))
        self.links_box.pack(fill="x", padx=8, pady=4)
        self.links_box.bind("<Double-Button-1>", self.open_browser)

        ctk.CTkLabel(rp, text="SHARE DATA", font=("Arial", 13, "bold")).pack(pady=(8, 2))
        share_row = ctk.CTkFrame(rp, fg_color="transparent")
        share_row.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkButton(share_row, text="WhatsApp", fg_color="#25D366", hover_color="#20BA5A", 
                      text_color="black", font=("Arial", 11, "bold"), width=120,
                      command=self.share_whatsapp).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        ctk.CTkButton(share_row, text="Facebook", fg_color="#1877F2", hover_color="#145DBF",
                      font=("Arial", 11, "bold"), width=120,
                      command=self.share_facebook).grid(row=0, column=1, padx=(5, 0), sticky="ew")
        share_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(rp, text="FULL HISTORY", font=("Arial", 13, "bold")).pack(pady=(10, 2))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter_history)
        ctk.CTkEntry(rp, placeholder_text="Search history…",
                     textvariable=self.search_var, width=250).pack(padx=8, pady=4)

        self.history_box = tk.Listbox(rp, bg="#111111", fg="white",
                                      selectbackground="#1f538d",
                                      relief="flat", borderwidth=0,
                                      font=("Consolas", 9))
        self.history_box.pack(fill="both", expand=True, padx=8, pady=4)
        self.history_box.bind("<Double-Button-1>", self._copy_history_item)

        ctk.CTkLabel(rp, text="Double click to copy", text_color="gray",
                     font=("Arial", 9)).pack()

        btn_row = ctk.CTkFrame(rp, fg_color="transparent")
        btn_row.pack(pady=8)
        ctk.CTkButton(btn_row, text="CLEAR",      width=75,
                      fg_color="#e74c3c", command=self.clear_all).grid(row=0, column=0, padx=3)
        ctk.CTkButton(btn_row, text="BATCH CSV",  width=80,
                      fg_color="#f39c12", command=self.export_csv).grid(row=0, column=1, padx=3)
        ctk.CTkButton(btn_row, text="EXPORT TXT", width=80,
                      fg_color="#27ae60", command=self.export_txt).grid(row=0, column=2, padx=3)

    # ── Dynamic Input Controls ───────────────────────────────
    def _clear_input_frame(self):
        for w in self.input_frame.winfo_children():
            w.destroy()

    def change_mode(self, value):
        self.mode = value
        self._clear_input_frame()
        {
            "Text/URL": self.show_text_inputs,
            "Email":    self.show_email_inputs,
            "WiFi":     self.show_wifi_inputs,
            "vCard":    self.show_vcard_inputs,
        }[value]()

    def show_text_inputs(self):
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter link or text…", width=230)
        self.url_entry.pack(pady=4)

    def show_email_inputs(self):
        self.email_to    = ctk.CTkEntry(self.input_frame, placeholder_text="To (email)", width=230); self.email_to.pack(pady=3)
        self.email_subj  = ctk.CTkEntry(self.input_frame, placeholder_text="Subject",   width=230); self.email_subj.pack(pady=3)
        self.email_body  = ctk.CTkTextbox(self.input_frame, height=70, width=230);                  self.email_body.pack(pady=3)

    def show_wifi_inputs(self):
        self.wifi_ssid  = ctk.CTkEntry(self.input_frame, placeholder_text="SSID (Network name)", width=230); self.wifi_ssid.pack(pady=3)
        self.wifi_pass  = ctk.CTkEntry(self.input_frame, placeholder_text="Password",             width=230); self.wifi_pass.pack(pady=3)
        self.wifi_type  = ctk.StringVar(value="WPA")
        ctk.CTkOptionMenu(self.input_frame, values=["WPA", "WEP", "nopass"],
                          variable=self.wifi_type, width=230).pack(pady=3)
        self.wifi_hidden = ctk.CTkCheckBox(self.input_frame, text="Hidden network"); self.wifi_hidden.pack(pady=3)

    def show_vcard_inputs(self):
        fields = [("Name",  "name"), ("Phone", "phone"), ("Email", "vemail"),
                  ("Org",   "org"),  ("URL",   "vurl")]
        for ph, attr in fields:
            e = ctk.CTkEntry(self.input_frame, placeholder_text=ph, width=230)
            e.pack(pady=2)
            setattr(self, f"vc_{attr}", e)