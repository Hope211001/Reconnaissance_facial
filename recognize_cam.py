import logging
logging.getLogger("deepface").setLevel(logging.ERROR)
logging.getLogger("retinaface").setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import cv2
from deepface import DeepFace

KNOWN_DB = "data/known"

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la webcam")
        return

    print("Appuyez sur 'q' pour quitter")

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

            cv2.putText(frame, name, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        except Exception as e:
            print("Erreur :", e)

        cv2.imshow("Reconnaissance faciale (q pour quitter)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
