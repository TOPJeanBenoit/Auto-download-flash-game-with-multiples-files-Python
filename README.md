Programme python pour enregistrer automatiquement des jeux flash qui contiennent plusieurs fichiers (Action Script 3):
  -Parcours des fichiers XML
  -Téléchargement
  -Déplacement dans le dossier et sous dossier

Bibliothèques nécessaires :
os 
requests
shutil


Exécution:
Exécuter la fonction sort_file()


sort_files(
{"nom": Nom du dossier qui va être créé pour installer le jeu,
"lien principal": Lien complet du fichier principal du jeu,
"autres fichiers": Liste des liens relatifs au fichier principal des autres fichiers (XML ou autre, affiché lors de l'exécution du main si nécessaire dans le debugger flash)
})

Note: si l'emplacement d'un fichier XML est indiqué par un autre fichier XML il est possible que le programme ne le détecte pas alors il faut l'ajouter à la liste "autres fichiers"

Pour savoir si un jeu nécessite d'autres fichiers il faut utiliser le Flash Player Standalone Debugger trouvable ici:
https://archive.org/details/adobeflash_debug_downloads

Si le jeu ne fonctionne toujours pas vérifiez le code source du jeu avec le décompileur JPEXS:
https://github.com/jindrapetrik/jpexs-decompiler

Programme écrit en juin 2023.
