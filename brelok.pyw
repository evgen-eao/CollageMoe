# ♡〜٩( ╹▿╹ )۶〜♡ ~ Импортируем всю магию для создания кавайного интерфейса
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD  # Для перетаскивания файлов как в макосочке
from PIL import Image, ImageTk, ImageOps, ImageDraw  # Волшебная палочка для работы с картинками

class KawaiiWindow(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("CollageMoe (✧ω✧)♪")
        self.configure(bg="#FFF9FB")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.create_title_bar()
        self.bind("<B1-Motion>", self.move_window)
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        
    def create_title_bar(self):
        gradient_image = self.create_gradient_image(width=self.winfo_screenwidth(), height=30)
        self.gradient_photo = ImageTk.PhotoImage(gradient_image)
        self.title_bar = tk.Canvas(self, width=self.winfo_screenwidth(), height=30, highlightthickness=0)
        self.title_bar.create_image(0, 0, anchor=tk.NW, image=self.gradient_photo)
        self.title_bar.pack(fill=tk.X)
        self.title_bar.create_text(15, 12, anchor=tk.W, text="CollageMoe (✧ω✧)♪", font=('Tahoma', 12, 'bold'), fill='white')
        close_btn = tk.Button(self.title_bar, text="✕", font=('Arial', 10, 'bold'), fg='white', 
                            bg="#FF99CC", activebackground="#FFCCDD", borderwidth=0, 
                            highlightthickness=0, cursor="hand2", padx=5, pady=0)
        close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        close_btn.bind("<Button-1>", lambda e: self.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#FFCCDD"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#FF99CC"))

    def create_gradient_image(self, width, height):
        base = Image.new('RGB', (width, height), "#ff6c87")
        top = Image.new('RGB', (width, height), "#FFFFFF")
        mask = Image.new('L', (width, height))
        mask_data = [int(512 * (x / width)) for x in range(width)] * height
        mask.putdata(mask_data)
        return Image.composite(top, base, mask)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        self._x = None
        self._y = None

    def move_window(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")


class KawaiiCollageMaker:
    def __init__(self, root):
        self.root = root
        self.canvas_size = (2480, 3508)
        self.image_size = (593, 415)
        self.max_images = 32
        self.images = []  # Храним обработанные изображения
        self.window_width = 600
        self.window_height = 910
        self.root.geometry(f"{self.window_width}x{self.window_height}+50+50")
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.nya_drop)
        self.draw_ui()

    def draw_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.window_width,
                               height=self.window_height - 0,
                               bg="#ffeaf1", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_rectangle(17, 17, self.window_width - 19, 
                                   self.window_height - 97,
                                   outline="#FFB3C6", width=3, dash=(5,5))

        btn_style = {
            'bg': '#FFB3C6',
            'fg': '#A8377F',
            'font': ('Tahoma', 12, 'bold'),
            'relief': 'flat',
            'activebackground': '#FFB3C6',
            'cursor': 'heart',
            'borderwidth': 0,
            'highlightthickness': 0
        }

        btn_frame = tk.Frame(self.root, bg="#ffeaf1")
        btn_frame.place(relx=0.5, rely=0.96, anchor='center')
        tk.Button(btn_frame, text="☆⌒(ゝ。∂) Очистить ~ ♡", command=self.puru_clear, **btn_style).pack(side=tk.LEFT, padx=7, pady=3)
        tk.Button(btn_frame, text="✿✼ Сохранить (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", command=self.save_kawaii, **btn_style).pack(side=tk.LEFT, padx=7, pady=3)

        for btn in btn_frame.winfo_children():
            btn.bind("<Enter>", lambda e: e.widget.config(bg='#FFD1E0'))
            btn.bind("<Leave>", lambda e: e.widget.config(bg='#FFB3C6'))

        self.update_display()

    def nya_drop(self, event):
        # (ノ*°▽°*) Обрабатываем перетаскивание файлов
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if len(self.images) >= self.max_images:
                messagebox.showwarning("(>_<) Ой!", f"Можно только {self.max_images} картинок!")
                break
            if f.lower().endswith(('.png','.jpg','.jpeg','.bmp','.gif')):
                try:
                    with Image.open(f) as img:
                        processed_img = self.process_image(img)
                        self.images.append(processed_img)  # Сразу добавляем обработанное изображение
                    self.update_display()
                    self.root.title(f"CollageMoe (✧ω✧)♪ {len(self.images)}/{self.max_images}")
                except Exception as e:
                    print(f"(╥﹏╥) Ошибка в {f}: {e}")

    def process_image(self, img):
        # (´･ᴗ･`) Поворачиваем картинку если она в портретной ориентации
        img_ratio = img.width / img.height
        target_ratio = self.image_size[0] / self.image_size[1]

        if (img_ratio > 1) != (target_ratio > 1):
            img = img.rotate(90, expand=True)

        # ～(^∇^〜） Обрезаем картинку по заданному размеру с высоким качеством
        return ImageOps.fit(img, self.image_size, method=Image.LANCZOS, centering=(0.5, 0.5))

    def update_display(self):
        # (◕ᴗ◕✿) Обновляем превью коллажа
        self.canvas.delete("preview")
        self.temp_canvas = Image.new('RGB', self.canvas_size, (255, 255, 255))
        draw = ImageDraw.Draw(self.temp_canvas)

        if self.images:
            max_per_row = self.canvas_size[0] // self.image_size[0]
            num_rows = (len(self.images) + max_per_row - 1) // max_per_row
            start_y = (self.canvas_size[1] - num_rows * self.image_size[1]) // 2

            for i, processed_img in enumerate(self.images):
                row = i // max_per_row
                per_row = min(max_per_row, len(self.images) - row * max_per_row)
                start_x = (self.canvas_size[0] - (per_row * self.image_size[0] - (per_row - 1))) // 2
                x = start_x + (i % max_per_row) * (self.image_size[0] - 1)
                y = start_y + row * (self.image_size[1] - 1)

                self.temp_canvas.paste(processed_img, (x, y))
                border_width = 1
                draw.rectangle(
                    [(x, y), (x + self.image_size[0] - 1, y + self.image_size[1] - 1)],
                    outline="#c0c0c0", width=border_width
                )

        # (๑˃ᴗ˂)ﻭ Масштабируем превью с высоким качеством
        preview_width = self.window_width - 40
        preview_height = int(self.temp_canvas.height * (preview_width / self.temp_canvas.width))
        preview_img = self.temp_canvas.resize((preview_width, preview_height), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(preview_img)
        pos_x = (self.window_width - preview_width) // 2
        pos_y = 20
        self.canvas.create_image(pos_x, pos_y, anchor=tk.NW, image=self.tk_img, tags="preview")

    def save_kawaii(self):
        if not self.images:
            messagebox.showwarning("(•ิ_•ิ)?", "Добавь картинки сначала!")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        if not output_path:
            return

        if hasattr(self, 'temp_canvas'):
            try:
                img = self.temp_canvas.convert('RGB')
                save_kwargs = {"quality": 100, "subsampling": 0, "dpi": (300, 300), "icc_profile": None}
                img.save(output_path, **save_kwargs)
            except Exception as e:
                messagebox.showerror("(>_<) Ошибка!", f"Не удалось сохранить: {str(e)}")
        else:
            messagebox.showwarning("(>_<)", "Ничего не найдено для сохранения!")

    def puru_clear(self):
        self.images = []
        self.update_display()
        self.root.title("(◕‿◕) Коллаж-тян")

if __name__ == "__main__":
    root = KawaiiWindow()
    app = KawaiiCollageMaker(root)
    root.mainloop()