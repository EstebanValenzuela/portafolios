import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np

class ColorAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Box")
        self.cap = None
        self.prev_running = False
        self.zoom_scale = 1.0
        self.zoom_step = 0.1

        self.image = None
        self.current_frame = None
        self.selected_part = None
        self.colors = {"pelo": [], "ojos": [], "cara": [], "boca": []}

        self.create_widgets()

        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.root.bind("<plus>", lambda e: self.zoom_in())
        self.root.bind("<minus>", lambda e: self.zoom_out())

    def on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.zoom_in()
        elif event.num == 5 or event.delta < 0:
            self.zoom_out()


    def create_widgets(self):
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        for part in ["pelo", "ojos", "cara", "boca"]:
            b = ttk.Button(self.button_frame, text=part.capitalize(), command=lambda p=part: self.select_part(p))
            b.pack(side=tk.LEFT, padx=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.pre_btn = ttk.Button(btn_frame, text="Iniciar vista de cámara", command=self.capture_photo)
        self.pre_btn.pack(side="left", padx=5)

        self.take_photo_btn = ttk.Button(btn_frame, text="Tomar foto", command=self.take_snapshot)
        self.take_photo_btn.pack(side="left", padx=5)

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_image_click)

        self.bars = {}
        for part in ["pelo", "ojos", "cara", "boca"]:
            frame = ttk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=2)
            label = ttk.Label(frame, text=part.capitalize(), width=10)
            label.pack(side="left")
            canvas = tk.Canvas(frame, height=20, width=200)
            canvas.pack(side="left")
            self.bars[part] = canvas

    def take_snapshot(self):
        if self.prev_running and self.cap is not None:
            self.image = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            self.display_image()
            self.cap.release()
            self.prev_running = False
            self.cap = None

    def select_part(self, part):
        self.selected_part = part
        print(f"Modo activo: {part}")

    def update_color_bar(self, part):
        canvas = self.bars[part]
        canvas.delete("all")
        if self.colors[part]:
            avg_color = np.mean(self.colors[part], axis=0).astype(int)
            hex_color = '#%02x%02x%02x' % tuple(avg_color)
            canvas.create_rectangle(0, 0, 200, 20, fill=hex_color, outline="black")

    def capture_photo(self): 
        if self.prev_running:
            return

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "No se puede abrir la cámara")
            return
        
        self.prev_running = True
        self.update_preview()

    def update_preview(self):
        if not self.prev_running or self.cap is None:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        self.current_frame = frame

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = img.resize((640, 480))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.root.after(10, self.update_preview)

    def display_image(self):
        if self.image is None:
            return

    # Escala la imagen original según el nivel de zoom
        h, w, _ = self.image.shape
        zoomed_w = int(w * self.zoom_scale)
        zoomed_h = int(h * self.zoom_scale)

    # Resize manteniendo calidad
        resized = cv2.resize(self.image, (zoomed_w, zoomed_h), interpolation=cv2.INTER_LINEAR)

    # Asegurarse de no recortar más allá de la imagen
        crop_w = min(640, zoomed_w)
        crop_h = min(480, zoomed_h)

    # Obtener una sección central de la imagen escalada
        x_start = (zoomed_w - crop_w) // 2
        y_start = (zoomed_h - crop_h) // 2
        cropped = resized[y_start:y_start+crop_h, x_start:x_start+crop_w]

    # Convertir y mostrar en el canvas
        img = Image.fromarray(cropped)
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.config(width=crop_w, height=crop_h)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)


    def zoom_in(self, event = None):
        self.zoom_scale += self.zoom_step
        self.display_image()

    def zoom_out(self, event = None):
        self.zoom_scale = max(0.1, self.zoom_scale - self.zoom_step)
        self.display_image()

    def on_image_click(self, event):
        if self.image is None or self.selected_part is None:
            return

        x = int(event.x * self.image.shape[1] / 640)
        y = int(event.y * self.image.shape[0] / 480)
        color = self.image[y, x]
        self.colors[self.selected_part].append(color)
        print(f"Muestra en {self.selected_part}: {color}")
        self.update_color_bar(self.selected_part)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorAnalyzerApp(root)
    root.mainloop()
