import cv2
import os
import pyautogui

class Outils : 
    """
    Cette classe permet de : 
    1- Recuperer les images qui constituent une video.
    2- Stocker ces images dans un repertoire.
    3- Redimensionner les images.
    4- Passer l'image au model qui predit la classe ; si la classe de l image precedente est similaire il enregistre qu une seule 
    des deux predictions, pourquoi ? La fonction recupere toutes les images qui constituent la video, donc si la main n a pas changer
    de signe cela peut poser probleme, on n aura donc des erreur d orthographe quand on voudra traduire un mot qui contient des lettres
    doublees.
    5- Suppression des images du repertoire.
    """
    def __init__(self, cheminVideo, cheminStockage, dimensions, modele):
        self.cheminVideo = cheminVideo 
        self.cheminStockage = cheminStockage
        self.dimensions = dimensions
        self.modele = modele
    
    def extraction_et_traduction(self):
        # Lecture de la vidéo
        video_capture = cv2.VideoCapture(self.cheminVideo)

        # Liste pour stocker les prédictions
        predictions = []
        derniere_prediction = None

        # Initialiser le compteur de frames
        numero_capture = 0

        # Parcours de toutes les images dans la vidéo
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Enregistrer la frame dans un répertoire
            nom_fichier = "nourchen{}.png".format(numero_capture)
            chemin_fichier = os.path.join(self.cheminStockage, nom_fichier)
            
            # Redimensionner
            hauteur, largeur = self.dimensions
            image_redimensionnee = cv2.resize(frame, (largeur, hauteur))

            # Stockage
            cv2.imwrite(chemin_fichier, image_redimensionnee)

            # Passer l'image au modèle pour prédire la classe
            prediction = self.modele.predict()

            # Supprimer l'image après l'avoir traduite

            # Vérifier si la prédiction est différente de la précédente
            if prediction != derniere_prediction:
                predictions.append(prediction)
                derniere_prediction = prediction

            # Incrémenter le compteur de frames
            numero_capture += 1

        return predictions

class Modele : 
    def __init__(self, lettre):
        self.lettre = lettre
    
    def predict(self):
        return self.lettre

outil = Outils("./nourchen_test.mp4","./Images", (400,400), Modele("N"))
print(outil.extraction_et_traduction())