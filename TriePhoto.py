# Script de trie des photo en fonction de la date de prise de vue
# --- Utilisation des données Exif
# --- Si aucune date n'est trouvé on fait un trie: Sans Exif, Pas de date ou Illisible


import os
from exif import Image

chemin = input('Repertoire photo à Trier:')
no_lisible = '0 - Incconnue'
no_date = '1 - Pas de Date'
no_exif = '2 - Sans Exif'


def ImageLisible(racine):
    # Controle si l'image n'est pas corompue
    import cv2  # Lib OpenCV

    if os.path.isfile(racine):
        image = cv2.imread(racine)  # Ouverture de l'image avec OpenCV
        return image is not None
    else:
        return False  # Image n'est pas un fichier


def ExifDatetime(c_fichier):
    from exif import Image
    with open(c_fichier, 'rb') as image_file:
        my_image = Image(image_file)
        for attribu in chemin(my_image):
            return attribu == 'datetime'
    image_file.close()


def MoveImage(source, destination):
    import os
    import shutil

    if not os.path.ischemin(destination) or os.path.isfile(source):
        try:
            os.makechemins(destination)
        except OSError:
            if not os.path.ischemin(destination):
                Raise
        try:
            shutil.move(source, destination)
            print(f'==> {destination}')
        except shutil.Error:
            print('Oups !!')


for dossier in list(os.walk(chemin)):

    for fichier in dossier[2]:

        c_dossier = os.path.join(chemin, dossier[0])
        c_fichier = os.path.join(c_dossier, str(fichier))

        if os.path.isfile(c_fichier):

            image_file = open(c_fichier, 'rb')
            # if ImageLisible(c_fichier):
            try:
                print(c_fichier)
                my_image = Image(image_file)

                if my_image.has_exif:
                    try:
                        date = f'{my_image.datetime[:4]}-{my_image.datetime[5:7]}-{my_image.datetime[8:10]}'
                        repertoire = f'{my_image.datetime[:4]}/{date}'
                        print(f'-> {my_image.datetime}')
                        c_fichier_out = os.path.join(chemin, repertoire)
                        MoveImage(c_fichier, c_fichier_out)

                    except AttributeError:
                        MoveImage(c_fichier, os.path.join(chemin, no_date))

                else:
                    MoveImage(c_fichier, os.path.join(chemin, no_exif))
            except Exception:
                image_file.close()
                print('Illisible')
                MoveImage(c_fichier, os.path.join(chemin, no_lisible))
        else:
            print('Pas un fichier')
