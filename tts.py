import customtkinter as ctk
import asyncio
import os
from tkinter import filedialog, messagebox

# Edge-TTS funksiyasi
async def generate_audio(text, rate, pitch, output_file):
    voice = "en-US-AndrewNeural"
    # Foizni edge-tts formatiga o'tkazish (masalan: +8%)
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    
    command = f'edge-tts --voice {voice} --text "{text}" --rate={rate_str} --pitch={pitch_str} --write-media "{output_file}"'
    os.system(command)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Audio Generator (Edge-TTS)")
        self.geometry("500x450")

        # Matn kiritish maydoni
        self.label = ctk.CTkLabel(self, text="Matnni kiriting:")
        self.label.pack(pady=10)
        
        self.text_area = ctk.CTkTextbox(self, width=400, height=150)
        self.text_area.pack(pady=10)

        # Tezlik (Rate) - Slider
        self.rate_label = ctk.CTkLabel(self, text="Tezlik (Rate): +8%")
        self.rate_label.pack()
        self.rate_slider = ctk.CTkSlider(self, from_=-50, to=50, command=self.update_rate_label)
        self.rate_slider.set(8)
        self.rate_slider.pack(pady=5)

        # Aylantirish tugmasi
        self.button = ctk.CTkButton(self, text="Ovozga aylantirish va Saqlash", command=self.start_conversion)
        self.button.pack(pady=20)

    def update_rate_label(self, value):
        self.rate_label.configure(text=f"Tezlik (Rate): {int(value):+d}%")

    def start_conversion(self):
        text = self.text_area.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Xato", "Iltimos, matn kiriting!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            rate = int(self.rate_slider.get())
            # Edge-TTS ni ishga tushirish
            try:
                asyncio.run(generate_audio(text, rate, -5, file_path))
                messagebox.showinfo("Tayyor", f"Fayl saqlandi: {file_path}")
            except Exception as e:
                messagebox.showerror("Xato", f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()