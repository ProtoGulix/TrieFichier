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

    if not os.path.isdir(destination) or os.path.isfile(source):
        try:
            os.makedirs(destination)
        except OSError:
            if not os.path.isdir(destination):
                Raise
        try:
            shutil.copy(source, destination)
            print(f'==> {destination}')
        except shutil.Error:
            print('Oups !!')


f_manifest = 'manifest.json'
no_lisible = '0 - Incconnue'
no_date = '1 - Pas de Date'
no_exif = '2 - Sans Exif'
f_invalide = []
f_valide = []


chemin_in = input('Repertoire photo à Trier:')

if not os.path.isdir(chemin_in):
    chemin_in = input('Repertoire photo à Trier:')

chemin_out = input('Repertoire de Sortie:')

if not os.path.isdir(chemin_out):
    chemin_out = input('Repertoire de Sortie:')

if not os.path.isfile(f_manifest):

    manifest = open(f_manifest, 'w')

    data_json = []
    i = 1

    for dossier in list(os.walk(chemin_in)):

        c_dossier = os.path.join(chemin_in, dossier[0])
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
        try:
            date = f"{d['date'][:4]}-{d['date'][5:7]}-{d['date'][8:10]}"
            repertoire = f"{d['date'][:4]}/{date}"
            c_fichier_out = os.path.join(chemin_out, repertoire)

            print(f"{d['path']} --> {c_fichier_out}")

            MoveFile(d['path'], c_fichier_out)

        except AttributeError:
            MoveFile(d['path'], os.path.join(chemin_in, no_date))
        print(d['path'])
    print('manifest')
