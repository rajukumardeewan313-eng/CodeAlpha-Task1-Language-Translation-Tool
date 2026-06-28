import tkinter as tk
from tkinter import scrolledtext
import math
import re
import string

# ── FAQ Dataset ───────────────────────────────────────────────
FAQS = [
    {
        "question": "What is Python?",
        "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming."
    },
    {
        "question": "How do I install Python?",
        "answer": "You can install Python by visiting python.org/downloads and downloading the installer for your OS. On Windows, run the .exe installer. On macOS/Linux, use the package manager or the official installer."
    },
    {
        "question": "What is a virtual environment in Python?",
        "answer": "A virtual environment is an isolated Python environment that lets you install packages for a specific project without affecting other projects or the system Python. Create one using: python -m venv myenv"
    },
    {
        "question": "What is pip?",
        "answer": "pip is the package installer for Python. It allows you to install and manage Python libraries from PyPI. Example: pip install requests"
    },
    {
        "question": "What is the difference between a list and a tuple?",
        "answer": "A list is mutable (can be changed after creation) and uses square brackets []. A tuple is immutable (cannot be changed) and uses parentheses (). Tuples are generally faster and used for fixed data."
    },
    {
        "question": "What is a dictionary in Python?",
        "answer": "A dictionary is an unordered collection of key-value pairs. It is mutable and indexed by keys. Example: {'name': 'Alice', 'age': 25}"
    },
    {
        "question": "What is a lambda function?",
        "answer": "A lambda function is a small anonymous function defined with the lambda keyword. It can have any number of arguments but only one expression. Example: add = lambda x, y: x + y"
    },
    {
        "question": "What is object-oriented programming?",
        "answer": "Object-oriented programming (OOP) is a programming paradigm based on objects and classes. Key concepts include encapsulation, inheritance, polymorphism, and abstraction."
    },
    {
        "question": "What is a class in Python?",
        "answer": "A class is a blueprint for creating objects. It defines attributes (data) and methods (functions) that the objects of that class will have. Use the 'class' keyword to define one."
    },
    {
        "question": "What is inheritance in Python?",
        "answer": "Inheritance allows a class (child) to inherit attributes and methods from another class (parent). This promotes code reuse. Example: class Dog(Animal): pass"
    },
    {
        "question": "What are Python decorators?",
        "answer": "Decorators are functions that modify the behavior of another function without changing its source code. They use the @ syntax. Example: @staticmethod, @property, or custom decorators."
    },
    {
        "question": "What is exception handling in Python?",
        "answer": "Exception handling lets you handle runtime errors gracefully using try, except, else, and finally blocks. Example: try: x = 1/0 except ZeroDivisionError: print('Cannot divide by zero')"
    },
    {
        "question": "What is a generator in Python?",
        "answer": "A generator is a function that returns an iterator using the 'yield' keyword. It generates values lazily (one at a time) and is memory-efficient for large datasets."
    },
    {
        "question": "What is list comprehension?",
        "answer": "List comprehension is a concise way to create lists. Example: squares = [x**2 for x in range(10)] creates a list of squares from 0 to 81."
    },
    {
        "question": "What is the difference between == and is?",
        "answer": "'==' checks if two objects have the same value. 'is' checks if two variables point to the same object in memory. Example: [1,2] == [1,2] is True, but [1,2] is [1,2] is False."
    },
    {
        "question": "What is Tkinter?",
        "answer": "Tkinter is Python's standard GUI (Graphical User Interface) library. It provides widgets like buttons, labels, and entry fields to build desktop applications."
    },
    {
        "question": "What is NLP?",
        "answer": "NLP (Natural Language Processing) is a field of AI that enables computers to understand, interpret, and generate human language. Libraries like NLTK and SpaCy are used for NLP in Python."
    },
    {
        "question": "What is cosine similarity?",
        "answer": "Cosine similarity measures the cosine of the angle between two vectors. It's used in NLP to compare text similarity. A value of 1 means identical, 0 means no similarity."
    },
    {
        "question": "What is tokenization?",
        "answer": "Tokenization is the process of splitting text into individual words or sentences (tokens). It's a fundamental step in NLP preprocessing. Example: 'Hello world' → ['Hello', 'world']"
    },
    {
        "question": "What is stopword removal?",
        "answer": "Stopword removal is the process of removing common words (like 'the', 'is', 'at') that add little meaning to text analysis. This improves the accuracy of NLP models."
    },
    {
        "question": "How do I read a file in Python?",
        "answer": "Use the open() function: with open('file.txt', 'r') as f: content = f.read(). The 'with' statement ensures the file is properly closed after use."
    },
    {
        "question": "What is a REST API?",
        "answer": "A REST API is a web service that uses HTTP methods (GET, POST, PUT, DELETE) to perform operations. Python's 'requests' library is commonly used to interact with REST APIs."
    },
    {
        "question": "What is the difference between deep copy and shallow copy?",
        "answer": "A shallow copy creates a new object but references the same nested objects. A deep copy creates a completely independent copy including all nested objects. Use copy.deepcopy() for deep copy."
    },
]

# ── NLP Preprocessing ─────────────────────────────────────────
STOPWORDS = {
    "a","an","the","is","it","in","on","at","to","for","of","and","or","but",
    "not","with","this","that","are","was","were","be","been","being","have",
    "has","had","do","does","did","will","would","could","should","may","might",
    "i","you","he","she","we","they","me","him","her","us","them","my","your",
    "his","our","their","what","how","when","where","why","who","which","can",
    "what's","how's","there","by","from","as","if","so","just","about"
}

def preprocess(text):
    """Tokenize, lowercase, remove punctuation and stopwords."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return tokens

def build_tfidf(faqs):
    """Build a simple TF-IDF-like vector for each FAQ question."""
    corpus = [preprocess(faq["question"] + " " + faq["answer"]) for faq in faqs]
    # Build vocabulary
    vocab = {}
    idx = 0
    for doc in corpus:
        for word in doc:
            if word not in vocab:
                vocab[word] = idx
                idx += 1
    # Document frequency
    df = {}
    N = len(corpus)
    for doc in corpus:
        for word in set(doc):
            df[word] = df.get(word, 0) + 1
    # TF-IDF vectors
    vectors = []
    for doc in corpus:
        vec = [0.0] * len(vocab)
        word_count = len(doc) if doc else 1
        for word in doc:
            if word in vocab:
                tf = doc.count(word) / word_count
                idf = math.log((N + 1) / (df.get(word, 0) + 1)) + 1
                vec[vocab[word]] = tf * idf
        vectors.append(vec)
    return vocab, vectors

def vectorize_query(query, vocab, N, df):
    tokens = preprocess(query)
    vec = [0.0] * len(vocab)
    word_count = len(tokens) if tokens else 1
    for word in tokens:
        if word in vocab:
            tf = tokens.count(word) / word_count
            idf = math.log((N + 1) / (df.get(word, 0) + 1)) + 1
            vec[vocab[word]] = tf * idf
    return vec

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def find_best_match(query, vocab, faq_vectors, threshold=0.08):
    corpus = [preprocess(faq["question"] + " " + faq["answer"]) for faq in FAQS]
    N = len(corpus)
    df = {}
    for doc in corpus:
        for word in set(doc):
            df[word] = df.get(word, 0) + 1

    q_vec = vectorize_query(query, vocab, N, df)
    scores = [(cosine_similarity(q_vec, fv), i) for i, fv in enumerate(faq_vectors)]
    scores.sort(reverse=True)
    best_score, best_idx = scores[0]
    if best_score >= threshold:
        return FAQS[best_idx], best_score, scores[1:4]
    return None, best_score, scores[1:4]

# ── Palette ───────────────────────────────────────────────────
BG       = "#0f0f1a"
SURFACE  = "#1a1a2e"
SURFACE2 = "#22223b"
BORDER   = "#2a2a4a"
TEXT     = "#f0f0ff"
MUTED    = "#8888aa"
ACCENT   = "#60a5fa"
BOT_BG   = "#1a2744"
USER_BG  = "#22223b"
GREEN    = "#34d399"

# ── Chatbot UI ────────────────────────────────────────────────
class FAQChatbot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🤖 FAQ Chatbot")
        self.configure(bg=BG)
        self.state("zoomed")
        try:
            self.attributes("-zoomed", True)
        except Exception:
            pass
        self.minsize(700, 550)
        self.resizable(True, True)

        # Build NLP model
        self.vocab, self.faq_vectors = build_tfidf(FAQS)

        self._build_ui()
        self._bot_message("👋 Hi! I'm your **FAQ Assistant**.\n\nAsk me anything about Python, NLP, OOP, or programming concepts. I'll find the best answer for you!\n\n💡 Try: *\"What is a lambda function?\"* or *\"How do I install Python?\"*")

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self, bg=SURFACE, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🤖  FAQ Chatbot",
                 bg=SURFACE, fg=TEXT,
                 font=("Helvetica", 20, "bold")).pack(side="left", padx=24, pady=16)

        tk.Label(header, text=f"📚 {len(FAQS)} FAQs  ·  NLP Powered  ·  TF-IDF + Cosine Similarity",
                 bg=SURFACE, fg=MUTED,
                 font=("Helvetica", 10)).pack(side="right", padx=24)

        # ── Suggested questions ──
        suggest_frame = tk.Frame(self, bg=BG)
        suggest_frame.pack(fill="x", padx=20, pady=(12, 0))

        tk.Label(suggest_frame, text="💬 Quick questions:",
                 bg=BG, fg=MUTED, font=("Helvetica", 10)).pack(side="left", padx=(0, 8))

        suggestions = ["What is Python?", "What is NLP?", "What is cosine similarity?", "What is a lambda?"]
        for s in suggestions:
            tk.Button(suggest_frame, text=s,
                      bg=SURFACE2, fg=ACCENT,
                      activebackground=BORDER, activeforeground=TEXT,
                      font=("Helvetica", 9), bd=0, padx=10, pady=4,
                      cursor="hand2", relief="flat",
                      command=lambda q=s: self._quick_ask(q)
                      ).pack(side="left", padx=4)

        # ── Chat area ──
        chat_outer = tk.Frame(self, bg=BG)
        chat_outer.pack(fill="both", expand=True, padx=20, pady=12)

        self.chat_canvas = tk.Canvas(chat_outer, bg=BG, bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(chat_outer, orient="vertical",
                                 command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)

        self.msg_frame = tk.Frame(self.chat_canvas, bg=BG)
        self.canvas_win = self.chat_canvas.create_window(
            (0, 0), window=self.msg_frame, anchor="nw")

        self.msg_frame.bind("<Configure>", self._on_msg_configure)
        self.chat_canvas.bind("<Configure>", self._on_canvas_configure)
        self.chat_canvas.bind_all("<MouseWheel>",
            lambda e: self.chat_canvas.yview_scroll(-1*(e.delta//120), "units"))

        # ── Input row ──
        input_outer = tk.Frame(self, bg=SURFACE,
                               highlightbackground=BORDER, highlightthickness=1)
        input_outer.pack(fill="x", padx=20, pady=(0, 16))

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(input_outer,
                              textvariable=self.input_var,
                              bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                              font=("Helvetica", 13),
                              bd=0, highlightthickness=0)
        self.entry.pack(side="left", fill="both", expand=True, padx=16, pady=14)
        self.entry.bind("<Return>", lambda e: self._send())

        tk.Button(input_outer, text="Send ➤",
                  bg=ACCENT, fg="#0f0f1a",
                  activebackground="#93c5fd", activeforeground="#0f0f1a",
                  font=("Helvetica", 12, "bold"),
                  bd=0, padx=20, pady=10, cursor="hand2", relief="flat",
                  command=self._send
                  ).pack(side="right", padx=8, pady=6)

        self.entry.focus()

    def _on_msg_configure(self, e=None):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def _on_canvas_configure(self, e=None):
        self.chat_canvas.itemconfig(self.canvas_win, width=self.chat_canvas.winfo_width())

    def _scroll_bottom(self):
        self.after(100, lambda: self.chat_canvas.yview_moveto(1.0))

    def _user_message(self, text):
        row = tk.Frame(self.msg_frame, bg=BG)
        row.pack(fill="x", pady=4, padx=8)

        bubble = tk.Frame(row, bg=USER_BG,
                          highlightbackground=BORDER, highlightthickness=1)
        bubble.pack(side="right", anchor="e")

        tk.Label(bubble, text="🧑 You", bg=USER_BG, fg=MUTED,
                 font=("Helvetica", 9, "bold")).pack(anchor="w", padx=12, pady=(8, 0))
        tk.Label(bubble, text=text, bg=USER_BG, fg=TEXT,
                 font=("Helvetica", 12), wraplength=550, justify="left"
                 ).pack(anchor="w", padx=12, pady=(2, 10))
        self._scroll_bottom()

    def _bot_message(self, text, score=None, suggestions=None):
        row = tk.Frame(self.msg_frame, bg=BG)
        row.pack(fill="x", pady=4, padx=8)

        bubble = tk.Frame(row, bg=BOT_BG,
                          highlightbackground=ACCENT, highlightthickness=1)
        bubble.pack(side="left", anchor="w")

        header_row = tk.Frame(bubble, bg=BOT_BG)
        header_row.pack(fill="x", padx=12, pady=(8, 0))

        tk.Label(header_row, text="🤖 Bot", bg=BOT_BG, fg=ACCENT,
                 font=("Helvetica", 9, "bold")).pack(side="left")

        if score is not None:
            color = GREEN if score > 0.3 else ACCENT if score > 0.15 else MUTED
            tk.Label(header_row,
                     text=f"  ·  Match: {score*100:.1f}%",
                     bg=BOT_BG, fg=color,
                     font=("Helvetica", 9)).pack(side="left")

        tk.Label(bubble, text=text, bg=BOT_BG, fg=TEXT,
                 font=("Helvetica", 12), wraplength=580, justify="left"
                 ).pack(anchor="w", padx=12, pady=(4, 10))

        if suggestions:
            tk.Label(bubble, text="📎 Related questions:",
                     bg=BOT_BG, fg=MUTED,
                     font=("Helvetica", 9)).pack(anchor="w", padx=12)
            for faq, sc in suggestions:
                tk.Button(bubble, text=f"  ❯  {faq['question']}",
                          bg=SURFACE2, fg=ACCENT,
                          activebackground=BORDER, activeforeground=TEXT,
                          font=("Helvetica", 10), bd=0, padx=10, pady=4,
                          cursor="hand2", relief="flat", anchor="w",
                          command=lambda q=faq['question']: self._quick_ask(q)
                          ).pack(fill="x", padx=12, pady=2)
            tk.Label(bubble, text="", bg=BOT_BG).pack(pady=2)

        self._scroll_bottom()

    def _quick_ask(self, q):
        self.input_var.set(q)
        self._send()

    def _send(self):
        query = self.input_var.get().strip()
        if not query:
            return
        self.input_var.set("")
        self._user_message(query)

        match, score, others = find_best_match(query, self.vocab, self.faq_vectors)

        if match:
            answer = f"❓ {match['question']}\n\n{match['answer']}"
            related = [(FAQS[i], s) for s, i in others if s > 0.05][:2]
            self._bot_message(answer, score=score, suggestions=related if related else None)
        else:
            self._bot_message(
                f"🤔 I couldn't find a good match for your question (confidence: {score*100:.1f}%).\n\n"
                "Try rephrasing or ask about: Python, NLP, OOP, decorators, generators, list comprehension, etc.",
                score=score
            )

if __name__ == "__main__":
    app = FAQChatbot()
    app.mainloop()
