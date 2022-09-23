import os
import mimetypes
import shutil

def TypeFile(MimeType):

    with open('MimeTypeAllow', 'r') as f:
        liste = [(liste.strip('\n')).lower() for liste in f.readlines()]
        if MimeType.lower() in liste:
            return True
        else:
            return False


dir = "C:/Users/Quentin/Desktop/Pictures"

for dossier, sous_dossiers, fichiers in os.walk(dir):
    if fichiers :
        for fichier in fichiers:
            path = os.path.join(dossier, fichier)
            type = mimetypes.guess_type(path)

            if type[0] and TypeFile(type[0]):
                print('')
                print('{} [{}]'.format(path, str(type[0])))

                dir_out = os.path.join('E:/Sauvegarde',str(type[0]))
                path_out = os.path.join(dir_out,str(fichier))

                try:
                    print('==>', dir_out)
                    os.makedirs(dir_out)
                except OSError:
                    if not os.path.isdir(dir_out):
                        Raise

                if os.path.isfile(path_out) == False:
                    shutil.copy(path,path_out)
                    print('==> '+ path_out)
                else:
                    print('==> Le fichier existe dèjà !')
