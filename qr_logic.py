import os
import json
import csv
import threading
import urllib.parse
import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
from PIL import Image
import cv2
import qrcode
import qrcode.image.svg
import config

class QRLogic:
    def load_history(self):
        if os.path.exists(config.HISTORY_FILE):
            try:
                with open(config.HISTORY_FILE, "r") as f:
                    data = json.load(f)
                    if data and isinstance(data[0], str):
                        migrated = []
                        for old_item in data:
                            migrated.append({"timestamp": "Legacy", "data": old_item})
                        return migrated
                    return data
            except Exception:
                pass
        return []

    def save_history(self):
        try:
            with open(config.HISTORY_FILE, "w") as f:
                json.dump(self.history_data, f, indent=2)
        except Exception as e:
            print(f"Error saving history file payload: {e}")

    def _escape_wifi_str(self, string):
        escaped = ""
        for char in string:
            if char in ['\\', ';', ',', ':']:
                escaped += '\\' + char
            else:
                escaped += char
        return escaped

    def _build_qr_data(self):
        if self.mode == "Text/URL":
            return self.url_entry.get().strip()
        elif self.mode == "Email":
            to   = self.email_to.get().strip()
            subj = self.email_subj.get().strip()
            body = self.email_body.get("1.0", "end").strip()
            return f"MATMSG:TO:{to};SUB:{subj};BODY:{body};;"
        elif self.mode == "WiFi":
            ssid   = self._escape_wifi_str(self.wifi_ssid.get().strip())
            pwd    = self._escape_wifi_str(self.wifi_pass.get().strip())
            enc    = self.wifi_type.get()
            hidden = "true" if self.wifi_hidden.get() else "false"
            return f"WIFI:T:{enc};S:{ssid};P:{pwd};H:{hidden};;"
        elif self.mode == "vCard":
            n  = getattr(self, "vc_name",  None);  n  = n.get().strip()  if n  else ""
            p  = getattr(self, "vc_phone", None);  p  = p.get().strip()  if p  else ""
            em = getattr(self, "vc_vemail",None);  em = em.get().strip() if em else ""
            og = getattr(self, "vc_org",   None);  og = og.get().strip() if og else ""
            ur = getattr(self, "vc_vurl",  None);  ur = ur.get().strip() if ur else ""
            return (f"BEGIN:VCARD\nVERSION:3.0\nFN:{n}\nTEL:{p}\n"
                    f"EMAIL:{em}\nORG:{og}\nURL:{ur}\nEND:VCARD")
        return ""

    def generate_qr(self):
        import customtkinter as ctk
        data = self._build_qr_data()
        if not data:
            messagebox.showwarning("Empty", "Please enter some data first.")
            return

        ec_map = {"L (7%)": qrcode.constants.ERROR_CORRECT_L,
                  "M (15%)": qrcode.constants.ERROR_CORRECT_M,
                  "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
                  "H (30%)": qrcode.constants.ERROR_CORRECT_H}
        ec = ec_map.get(self.error_var.get(), qrcode.constants.ERROR_CORRECT_H)

        qr = qrcode.QRCode(error_correction=ec, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color).convert("RGBA")

        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image.open(self.logo_path).convert("RGBA")
                qr_w, qr_h = img.size
                logo_size = qr_w // 4
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
                img.paste(logo, pos, logo)
            except Exception as e:
                print(f"Logo error: {e}")

        px = int(self.size_var.get().split()[0])
        self.current_img = img.resize((px, px), Image.LANCZOS)

        thumb = self.current_img.resize((180, 180), Image.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=thumb, dark_image=thumb, size=(180, 180))
        self.preview_label.configure(image=ctk_img, text="")
        self.preview_label.image = ctk_img

        self.save_png_btn.configure(state="normal")
        self.save_svg_btn.configure(state="normal")

    def save_qr(self, fmt="png"):
        data = self._build_qr_data()
        if fmt == "svg" and not data:
            data = self.last_scanned if self.last_scanned else "Ultimate QR Pro"

        ext  = f".{fmt}"
        path = filedialog.asksaveasfilename(defaultextension=ext,
                                            filetypes=[(f"{fmt.upper()} files", f"*{ext}")])
        if not path:
            return

        if fmt == "svg":
            try:
                ec_map = {"L (7%)": qrcode.constants.ERROR_CORRECT_L,
                          "M (15%)": qrcode.constants.ERROR_CORRECT_M,
                          "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
                          "H (30%)": qrcode.constants.ERROR_CORRECT_H}
                ec = ec_map.get(self.error_var.get(), qrcode.constants.ERROR_CORRECT_H)
                
                factory = qrcode.image.svg.SvgPathImage
                svg_qr = qrcode.QRCode(error_correction=ec, box_size=10, border=4)
                svg_qr.add_data(data)
                svg_qr.make(fit=True)
                
                svg_img = svg_qr.make_image(image_factory=factory, fill_color=self.qr_color, back_color=self.bg_color)
                svg_img.save(path)
                self.show_status_msg("SVG QR Saved successfully!")
            except Exception as e:
                messagebox.showerror("SVG Error", f"Could not export native SVG: {e}")
        else:
            if self.current_img:
                self.current_img.convert("RGB").save(path)
                self.show_status_msg("PNG QR Saved successfully!")

    def start_camera(self):
        if self.camera_running:
            return
        self.start_btn.configure(state="disabled", text="Opening...")
        self.cam_label.configure(text="LOADING CAMERA BUS...")
        
        threading.Thread(target=self._async_camera_open, daemon=True).start()

    def _async_camera_open(self):
        cap = cv2.VideoCapture(self.camera_index + cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(self.camera_index)
            
        if not cap.isOpened():
            self.after(0, lambda: messagebox.showerror("Camera", f"Cannot open camera index {self.camera_index}"))
            self.after(0, lambda: self.start_btn.configure(state="normal", text="START SCANNER"))
            self.after(0, lambda: self.cam_label.configure(text="CAMERA STANDBY"))
            return
            
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.cap = cap
        self.camera_running = True
        self.after(0, self._on_camera_ready)

    def _on_camera_ready(self):
        self.start_btn.configure(state="disabled", text="START SCANNER")
        self.stop_btn.configure(state="normal")
        self._update_scanner()

    def _update_scanner(self):
        import customtkinter as ctk
        if not self.camera_running or self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            data, bbox, _ = self.qr_detector.detectAndDecode(frame)
            if data and data != self.last_scanned:
                self.last_scanned = data
                self.scanned_count += 1
                self.scanned_lbl.configure(text=f"Scanned: {self.scanned_count}")
                self._beep()
                self.add_to_history(data)
                self.show_status_msg(f"Scanned: {data[:20]}...")

            if bbox is not None:
                pts = bbox[0].astype(int)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            w = self.cam_frame.winfo_width()
            h = self.cam_frame.winfo_height()
            if w < 10 or h < 10: 
                w, h = 760, 420 
                
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            
            ctk_cam_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(w, h))
            self.cam_label.configure(image=ctk_cam_img, text="")
            self.cam_label.image = ctk_cam_img

        self.after(30, self._update_scanner)

    def stop_camera(self):
        self.camera_running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = None
        self.cam_label.configure(image="", text="CAMERA STANDBY")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def scan_from_image(self):
        import customtkinter as ctk
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not path:
            return
        frame = cv2.imread(path)
        if frame is None:
            messagebox.showerror("Error", "Could not read image.")
            return
        data, _, _ = self.qr_detector.detectAndDecode(frame)
        if data:
            self.scanned_count += 1
            self.scanned_lbl.configure(text=f"Scanned: {self.scanned_count}")
            self.add_to_history(data)
            self.show_status_msg("QR Code loaded from image successfully.")
            
            w = self.cam_frame.winfo_width()
            h = self.cam_frame.winfo_height()
            if w < 10 or h < 10: w, h = 760, 420
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            ctk_load_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(w, h))
            self.cam_label.configure(image=ctk_load_img, text="")
            self.cam_label.image = ctk_load_img
        else:
            messagebox.showwarning("No QR", "No QR code found in image.")

    def show_status_msg(self, msg):
        if self.status_timer_id:
            self.after_cancel(self.status_timer_id)
        self.status_lbl.configure(text=msg)
        self.status_timer_id = self.after(3000, lambda: self.status_lbl.configure(text=""))

    def pick_qr_color(self):
        c = colorchooser.askcolor(initialcolor=self.qr_color)[1]
        if c:
            self.qr_color = c
            self.qr_color_btn.configure(fg_color=c)

    def pick_bg_color(self):
        c = colorchooser.askcolor(initialcolor=self.bg_color)[1]
        if c:
            self.bg_color = c
            self.bg_color_btn.configure(fg_color=c)

    def pick_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.svg")])
        if path:
            self.logo_path = path
            self.logo_label.configure(text=os.path.basename(path), text_color="white")

    def add_to_history(self, data):
        if not any(item['data'] == data for item in self.history_data):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_data.insert(0, {"timestamp": timestamp, "data": data})
            self.save_history()
            self.refresh_ui_logs()

    def refresh_ui_logs(self):
        self.history_box.delete(0, tk.END)
        self.links_box.delete(0, tk.END)
        for item in self.history_data:
            display_text = f"[{item['timestamp']}] {item['data']}"
            self.history_box.insert(tk.END, display_text)
            if any(s in str(item['data']) for s in ["http", "WIFI:", "MATMSG:", "BEGIN:VCARD"]):
                self.links_box.insert(tk.END, item['data'])

    def _filter_history(self, *_):
        q = self.search_var.get().lower()
        self.history_box.delete(0, tk.END)
        for item in self.history_data:
            display_text = f"[{item['timestamp']}] {item['data']}"
            if q in item['data'].lower() or q in item['timestamp']:
                self.history_box.insert(tk.END, display_text)

    def _copy_history_item(self, event):
        sel = self.history_box.curselection()
        if sel:
            raw_val = self.history_box.get(sel[0])
            if "]" in raw_val:
                val = raw_val.split("]", 1)[1].strip()
            else:
                val = raw_val
                
            self.clipboard_clear()
            self.clipboard_append(val)
            self.show_status_msg("Copied to clipboard!")

    def clear_all(self):
        if messagebox.askyesno("Clear", "Clear all history?"):
            self.history_data = []
            self.last_scanned = ""
            self.scanned_count = 0
            self.scanned_lbl.configure(text="Scanned: 0")
            self.save_history()
            self.refresh_ui_logs()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["#", "Timestamp", "Data"])
                for i, item in enumerate(self.history_data, 1):
                    w.writerow([i, item['timestamp'], item['data']])
            messagebox.showinfo("Exported", f"Saved {len(self.history_data)} rows to CSV.")

    def export_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                lines = [f"[{item['timestamp']}] {item['data']}" for item in self.history_data]
                f.write("\n".join(lines))
            messagebox.showinfo("Exported", f"Saved {len(self.history_data)} entries.")

    def _get_selected_share_data(self):
        sel_link = self.links_box.curselection()
        if sel_link:
            return self.links_box.get(sel_link[0])
            
        sel_hist = self.history_box.curselection()
        if sel_hist:
            raw_val = self.history_box.get(sel_hist[0])
            if "]" in raw_val:
                return raw_val.split("]", 1)[1].strip()
            return raw_val
            
        if self.last_scanned:
            return self.last_scanned
        return None

    def share_whatsapp(self):
        data = self._get_selected_share_data()
        if not data:
            messagebox.showwarning("Share", "Please select an item from history or scan a QR first.")
            return
        
        encoded_text = urllib.parse.quote(data)
        whatsapp_url = f"https://wa.me/?text={encoded_text}"
        webbrowser.open(whatsapp_url)

    def share_facebook(self):
        data = self._get_selected_share_data()
        if not data:
            messagebox.showwarning("Share", "Please select an item from history or scan a QR first.")
            return

        encoded_url = urllib.parse.quote(data)
        if data.startswith("http://") or data.startswith("https://"):
            fb_url = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
        else:
            fb_url = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote('https://google.com')}&quote={encoded_url}"
            
        webbrowser.open(fb_url)

    def open_browser(self, event):
        sel = self.links_box.curselection()
        if sel:
            val = self.links_box.get(sel[0])
            if val.startswith("http://") or val.startswith("https://"):
                webbrowser.open(val)
            else:
                webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(val)}")

    def toggle_theme(self):
        import customtkinter as ctk
        new = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(new)

    def _beep(self):
        if config.HAS_WINSOUND:
            import winsound
            threading.Thread(target=lambda: winsound.Beep(1000, 150), daemon=True).start()

    def on_closing(self):
        self.camera_running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.destroy()