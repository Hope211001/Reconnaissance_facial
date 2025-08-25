import logging
logging.getLogger("deepface").setLevel(logging.ERROR)
logging.getLogger("retinaface").setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox
import resumer  # <-- ton fichier resumer.py

# === Chemin vers la base de visages connus ===
KNOWN_DB = "data/known"

# === Fonction de scan visage ===
def scanner_visage():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erreur", "Impossible d'accéder à la webcam")
        return

    utilisateur_trouve = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            results = DeepFace.find(
                img_path=frame,
                db_path=KNOWN_DB,
                model_name="ArcFace",
                enforce_detection=False
            )

            name = "Inconnu"
            if len(results) > 0 and not results[0].empty:
                identity_path = results[0].iloc[0]["identity"]
                name = identity_path.split("/")[-1].split(".")[0]
                utilisateur_trouve = name

            cv2.putText(frame, name, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        except Exception as e:
            print("Erreur :", e)

        cv2.imshow("Scanner le visage (q pour quitter)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or utilisateur_trouve:
            break

    cap.release()
    cv2.destroyAllWindows()

    if utilisateur_trouve:
        # Si un utilisateur est trouvé, on ouvre directement le résumé
        resumer.ouvrir_resumeur()
    else:
        messagebox.showwarning("Utilisateur introuvable", "Aucun visage reconnu !")

# === Interface Tkinter principale ===
def interface():
    root = tk.Tk()
    root.title("Application Résumé + Scan Visage")
    root.geometry("400x250")
    root.configure(bg="#2c3e50")

    # Titre
    titre = tk.Label(root, text="Bienvenue", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
    titre.pack(pady=20)

    # Bouton Scanner
    btn_scan = tk.Button(root, text="Scanner le visage", font=("Arial", 14),
                         bg="#27ae60", fg="white", relief="flat", padx=10, pady=5,
                         command=scanner_visage)
    btn_scan.pack(pady=10)

    # Bouton Fermer
    btn_quit = tk.Button(root, text="Fermer l'application", font=("Arial", 14),
                         bg="#c0392b", fg="white", relief="flat", padx=10, pady=5,
                         command=root.quit)
    btn_quit.pack(pady=10)

    root.mainloop()

# === Lancement de l'application ===
if __name__ == "__main__":
    interface()
