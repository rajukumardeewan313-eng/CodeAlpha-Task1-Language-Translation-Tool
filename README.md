# 🌐 Language Translation Tool

> **CodeAlpha Internship — Task 1**  
> A desktop language translation application built with Python and Tkinter, powered by the MyMemory Translation API.

---

## 📸 Overview

A clean, dark-themed desktop app that lets you instantly translate text between 17+ languages. Designed with a focus on smooth user experience — non-blocking API calls, swap buttons, clipboard support, and real-time status feedback.

---

## ✨ Features

- 🌍 **17+ Languages Supported** — English, Urdu, Arabic, Hindi, French, Spanish, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Bengali, Turkish, Tamil, Telugu
- 🔄 **Auto Language Detection** — No need to manually set the source language
- ⇄ **Swap Languages** — Switch source and target with one click
- 📋 **Copy to Clipboard** — Copy the translated result instantly
- ⚡ **Non-Blocking Translation** — Uses Python threading so the UI never freezes
- 🎨 **Dark Mode UI** — Built with Tkinter, styled for a modern look
- ✅ **Error Handling** — Friendly error messages for failed requests or empty input

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language |
| Tkinter | Desktop GUI framework |
| MyMemory API | Free translation API |
| `requests` | HTTP calls to the API |
| `threading` | Background API calls (non-blocking UI) |
| `urllib.parse` | URL encoding for query text |

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/language-translation-tool.git
cd language-translation-tool
```

### 2. Install Dependencies
```bash
pip install requests
```
> Tkinter comes pre-installed with Python. If it's missing, run:  
> `sudo apt-get install python3-tk` (Linux)

### 3. Run the App
```bash
python translation_tool.py
```

---

## 🚀 Usage

1. Select the **source language** (or leave as *Auto Detect*)
2. Select the **target language**
3. Type or paste your text in the **Input Text** box
4. Click **Translate**
5. View the result in the **Translated Text** box
6. Use **Copy Result** to copy the output, or **Clear** to reset

---

## 🌐 Supported Languages

| Language | Code |
|---|---|
| Auto Detect | auto |
| English | en |
| Urdu | ur |
| Arabic | ar |
| Hindi | hi |
| French | fr |
| Spanish | es |
| German | de |
| Italian | it |
| Portuguese | pt |
| Russian | ru |
| Chinese (Simplified) | zh |
| Japanese | ja |
| Korean | ko |
| Bengali | bn |
| Turkish | tr |
| Tamil | ta |
| Telugu | te |

---

## 📁 Project Structure

```
language-translation-tool/
│
├── translation_tool.py   # Main application file
└── README.md             # Project documentation
```

---

## 🔗 API Reference

This project uses the **[MyMemory Translation API](https://mymemory.translated.net/)** — a free, no-auth-required translation API.

**Endpoint used:**
```
GET https://api.mymemory.translated.net/get?q={text}&langpair={src}|{dest}
```

> Free tier allows up to **1000 words/day** per IP address.

---

## ⚠️ Limitations

- Free API tier has a **daily word limit** (1000 words/day per IP)
- Auto Detect defaults to English as the source if detection is uncertain
- Internet connection is required for translation

---

## 🙌 Acknowledgements

- [MyMemory API](https://mymemory.translated.net/) for the free translation service
- [CodeAlpha](https://codealpha.tech/) for the internship opportunity and project task

---

## 👤 Author

**Your Name**  
📧 Email: rajukumardeewan313@gmail.com 
🔗 [LinkedIn](https://www.linkedin.com/in/raju-kumar-ai) | [GitHub](https://github.com/rajukumardeewan313-eng)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
