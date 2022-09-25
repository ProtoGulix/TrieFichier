# Script de trie des photo en fonction de la date de prise de vue
# --- Utilisation des données Exif
# --- Si aucune date n'est trouvé on fait un trie: Sans Exif, Pas de date ou Illisible


from calendar import c
from PIL.ExifTags import TAGS
import os


def ImageValide(racine):
    import imghdr
    import os

    _, ext = os.path.splitext(racine)
    try:
        t_fichier = imghdr.what(racine)

        f_valide = ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']

        if ext[1:].lower() in f_valide and t_fichier in f_valide:
            return t_fichier
    except OSError:
        print('erreur')


def ExifDatetime(c_fichier):

    from PIL import Image

    try:
        img = Image.open(c_fichier)
        img_exif = img.getexif()

        for tagid in img_exif:
            tagname = TAGS.get(tagid, tagid)
            value = img_exif.get(tagid)
            if tagname == 'DateTime':
                return value
    except OSError:
        print('erreur')


def MoveFile(source, destination):
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


chemin = input('Repertoire photo à Trier:')
no_lisible = '0 - Incconnue'
no_date = '1 - Pas de Date'
no_exif = '2 - Sans Exif'
f_invalide = []
f_valide = []

checker = open('manifest.txt', 'w')

for dossier in list(os.walk(chemin)):

    c_dossier = os.path.join(chemin, dossier[0])
    print(c_dossier)

    for fichier in dossier[2]:

        c_fichier = os.path.join(c_dossier, str(fichier))

        if os.path.isfile(c_fichier):

            if ImageValide(c_fichier):
                date = ExifDatetime(c_fichier)
                if date is not None:
                    print(f"Fichier valide {c_fichier} - {date}")
                    json = {'move': False, 'date': date, 'path': c_fichier}

                    checker.write(f"{json}\n")

            else:
                f_invalide.append(c_fichier)
        else:
            print('Pas un fichier')


"""
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

"""
