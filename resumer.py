
import tkinter as tk
from tkinter import scrolledtext, messagebox
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def resume_texte(texte):
    try:
        parser = PlaintextParser.from_string(texte, Tokenizer("french"))
        summarizer = LsaSummarizer()
        total_phrases = len(list(parser.document.sentences))
        nb_phrases = max(1, total_phrases // 3)
        resume = summarizer(parser.document, nb_phrases)
        return " ".join(str(phrase) for phrase in resume)
    except Exception as e:
        return f"Erreur: {e}"


def ouvrir_resumeur():
    def generer_resume():
        texte = input_text.get("1.0", tk.END).strip()
        if not texte:
            messagebox.showwarning("Attention", "Veuillez entrer un texte à résumer.")
            return

        resume = resume_texte(texte)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, resume)

    root = tk.Toplevel()  # Nouvelle fenêtre au lieu de root = Tk()
    root.title("📝 Résumeur de texte (automatique)")
    root.geometry("800x600")
    root.configure(bg="#f4f4f9")

    label1 = tk.Label(root, text="Collez votre texte :", font=("Arial", 12, "bold"), bg="#f4f4f9")
    label1.pack(pady=5)

    input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=12, font=("Arial", 11))
    input_text.pack(padx=10, pady=5)

    btn_resumer = tk.Button(root, text="✨ Générer le résumé", command=generer_resume,
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="raised")
    btn_resumer.pack(pady=10)

    label3 = tk.Label(root, text="Résumé :", font=("Arial", 12, "bold"), bg="#f4f4f9")
    label3.pack(pady=5)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, font=("Arial", 11), fg="#333")
    output_text.pack(padx=10, pady=5)

    root.mainloop()
