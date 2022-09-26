# Script de trie des photo en fonction de la date de prise de vue
# --- Utilisation des données Exif
# --- Si aucune date n'est trouvé on fait un trie: Sans Exif, Pas de date ou Illisible


from calendar import c
from genericpath import isfile
from PIL.ExifTags import TAGS
import os
import json


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


f_manifest = 'manifest.json'
no_lisible = '0 - Incconnue'
no_date = '1 - Pas de Date'
no_exif = '2 - Sans Exif'
f_invalide = []
f_valide = []


if not os.path.isfile(f_manifest):

    manifest = open(f_manifest, 'w')

    chemin = input('Repertoire photo à Trier:')

    data_json = []
    i = 1

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

                        # Données fichier valide
                        data_json.append({"id": i, "move": False,
                                          "date": date, "path": c_fichier})

                        # Serializing json
                        json_object = json.dumps(data_json, indent=4)

                        # Writing to sample.json
                        with open(f_manifest, "w") as outfile:
                            outfile.write(json_object)

                        # ID
                        i = i + 1

                else:
                    f_invalide.append(c_fichier)
            else:
                print('Pas un fichier')


else:

    data_manifest = open(f_manifest, 'r')
    data = json.load(data_manifest)
    for d in data:
        print(d['path'])
    print('manifest')


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
