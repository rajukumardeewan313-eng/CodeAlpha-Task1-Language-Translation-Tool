import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import urllib.parse

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese (Simplified)": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Bengali": "bn",
    "Turkish": "tr",
    "Tamil": "ta",
    "Telugu": "te",
}

LANG_NAMES = list(LANGUAGES.keys())

def translate_text(text, src_code, dest_code):
    if src_code == "auto":
        src_code = "en"
    lang_pair = f"{src_code}|{dest_code}"
    url = (
        "https://api.mymemory.translated.net/get"
        f"?q={urllib.parse.quote(text)}&langpair={lang_pair}"
    )
    response = requests.get(url, timeout=10)
    data = response.json()
    if data["responseStatus"] == 200:
        return data["responseData"]["translatedText"]
    else:
        raise Exception("Translation failed. Please try again.")

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation Tool — CodeAlpha")
        self.root.geometry("900x620")
        self.root.configure(bg="#0f1117")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1d2e")
        header.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            header,
            text="🌐 Language Translation Tool",
            bg="#1a1d2e",
            fg="#a78bfa",
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=15)

        tk.Label(
            header,
            text="Powered by MyMemory API — CodeAlpha Task 1",
            bg="#1a1d2e",
            fg="#6b7280",
            font=("Segoe UI", 10),
        ).pack(pady=(0, 10))

        # Language selection row
        lang_frame = tk.Frame(self.root, bg="#0f1117")
        lang_frame.pack(fill=tk.X, padx=30, pady=10)

        # Source language
        tk.Label(lang_frame, text="From:", bg="#0f1117", fg="#e5e7eb",
                 font=("Segoe UI", 11)).grid(row=0, column=0, padx=5)

        self.src_var = tk.StringVar(value="Auto Detect")
        src_menu = ttk.Combobox(lang_frame, textvariable=self.src_var,
                                values=LANG_NAMES, state="readonly", width=20,
                                font=("Segoe UI", 11))
        src_menu.grid(row=0, column=1, padx=10)

        # Swap button
        swap_btn = tk.Button(lang_frame, text="⇄", bg="#4f46e5", fg="white",
                             font=("Segoe UI", 13, "bold"), relief=tk.FLAT,
                             cursor="hand2", command=self._swap_languages,
                             padx=10)
        swap_btn.grid(row=0, column=2, padx=10)

        # Target language
        tk.Label(lang_frame, text="To:", bg="#0f1117", fg="#e5e7eb",
                 font=("Segoe UI", 11)).grid(row=0, column=3, padx=5)

        self.dest_var = tk.StringVar(value="Urdu")
        dest_menu = ttk.Combobox(lang_frame, textvariable=self.dest_var,
                                 values=LANG_NAMES, state="readonly", width=20,
                                 font=("Segoe UI", 11))
        dest_menu.grid(row=0, column=4, padx=10)

        # Text areas
        text_frame = tk.Frame(self.root, bg="#0f1117")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Input
        tk.Label(text_frame, text="Input Text:", bg="#0f1117", fg="#a78bfa",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")

        self.input_text = tk.Text(text_frame, height=10, bg="#1a1d2e", fg="#e5e7eb",
                                  font=("Segoe UI", 12), relief=tk.FLAT,
                                  insertbackground="white", wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

        # Output
        tk.Label(text_frame, text="Translated Text:", bg="#0f1117", fg="#a78bfa",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=1, sticky="w")

        self.output_text = tk.Text(text_frame, height=10, bg="#1a1d2e", fg="#34d399",
                                   font=("Segoe UI", 12), relief=tk.FLAT,
                                   state=tk.DISABLED, wrap=tk.WORD)
        self.output_text.grid(row=1, column=1, padx=(10, 0), sticky="nsew")

        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(1, weight=1)
        text_frame.rowconfigure(1, weight=1)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0f1117")
        btn_frame.pack(pady=15)

        self.translate_btn = tk.Button(
            btn_frame, text="Translate", bg="#4f46e5", fg="white",
            font=("Segoe UI", 13, "bold"), relief=tk.FLAT, cursor="hand2",
            padx=30, pady=8, command=self._start_translation
        )
        self.translate_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame, text="Clear", bg="#374151", fg="white",
            font=("Segoe UI", 13), relief=tk.FLAT, cursor="hand2",
            padx=20, pady=8, command=self._clear
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame, text="Copy Result", bg="#374151", fg="white",
            font=("Segoe UI", 13), relief=tk.FLAT, cursor="hand2",
            padx=20, pady=8, command=self._copy_result
        ).pack(side=tk.LEFT, padx=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bg="#0f1117",
                 fg="#6b7280", font=("Segoe UI", 10)).pack(pady=5)

    def _swap_languages(self):
        src = self.src_var.get()
        dest = self.dest_var.get()
        if src != "Auto Detect":
            self.src_var.set(dest)
            self.dest_var.set(src)

    def _clear(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_var.set("Ready")

    def _copy_result(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_var.set("Copied to clipboard!")
        else:
            messagebox.showwarning("Nothing to copy", "No translated text to copy.")

    def _start_translation(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter text to translate.")
            return
        src_code = LANGUAGES[self.src_var.get()]
        dest_code = LANGUAGES[self.dest_var.get()]
        self.translate_btn.config(state=tk.DISABLED, text="Translating...")
        self.status_var.set("Translating...")
        threading.Thread(target=self._do_translate,
                         args=(text, src_code, dest_code), daemon=True).start()

    def _do_translate(self, text, src_code, dest_code):
        try:
            result = translate_text(text, src_code, dest_code)
            self.root.after(0, self._show_result, result)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))

    def _show_result(self, result):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)
        self.output_text.config(state=tk.DISABLED)
        self.translate_btn.config(state=tk.NORMAL, text="Translate")
        self.status_var.set("Translation complete!")

    def _show_error(self, error):
        messagebox.showerror("Error", error)
        self.translate_btn.config(state=tk.NORMAL, text="Translate")
        self.status_var.set("Error occurred.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
