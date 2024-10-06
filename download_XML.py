from os.path import exists
from os import getcwd
from os import mkdir

from requests import get

from shutil import move


def file_folder_exists(name:str) -> bool:
    return exists(f"games\{name}")
   

def make_folder(name_folder):
    mkdir(getcwd() + chr(92) + "games" + chr(92) + name_folder)
    print("Le dossier " + name_folder + "a bien été crée dans le dossier games")


def url_get_root_file_filename(url:str):
    #récupérer le nom du fichier
    """Parcours le lien absolu du fichier et récuprère les derniers caracteres corespondant au nom du fchier
    Sortie tuple:
            0:Le lien absolu (pour avoir la racine quand on télécharge plusieurs fichiers)
            1:Le nom du fichier + extension
    """
    mem = None
    for i in range(len(url)):
        if url[i] == "/":
            mem = [url[:i+1], url[i+1:]]
    if mem == None:
        return ["", url]
    return mem


def put_in_folder(file_name:str, relative_destination:str):
    rep_actuel = getcwd() + "/"
    move(rep_actuel + file_name, rep_actuel + relative_destination)
    print("file moove to "+ rep_actuel + relative_destination)



#fonction télécharger XML

def download(url: str):
    filename = url_get_root_file_filename(url)[1]

    response = get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Le fichier a été téléchargé sous le nom  '{filename}'")
    else:
        print(f"Erreur lors de la récupération du fichier à partir de l'URL '{url}'. Code d'état HTTP : {response.status_code}")


def read_file(filename:str):
    f = open(filename,"r")
    return f.read()


#Fonctions récupérer tous les liens en liste

def test_format(n, texte):
    """revoie l'indice de fin du lien, et False si il y a pas de format correct"""
     
    format = [".swf",".xml",".mp3",".mp4",".json"]
    
    n=n+1

    for i in range(len(format)):
            j = 0
            test = True
            for j in range(len(format[i])):
                if test:
                    if texte[n + j-1] != format[i][j]:
                        test = False
            if test:
                 return n + len(format[i]) -1
    return False


def debut_lien(n, texte):
     for i in range(n-1,-1,-1):
          if texte[i] == chr(34) or texte[i] == ">":
               return i + 1

def get_link(debut:int, fin:int, texte):
    link = ""
    for i in range(debut, fin):
          link += texte[i]
    return link

def texte_to_list(texte):
    liste = []
    for i in range(len(texte)):
         if texte[i] == ".":
              if test_format(i, texte) == False:
                   pass
              else:
                   liste.append(get_link(debut_lien(i, texte), test_format(i, texte), texte))
    return liste

#fin Fonctions récupérer tous les liens en liste


def make_folder_in_folder(game_name, link):
    if not file_folder_exists(game_name + chr(92) + link):
        liste = [game_name] + link.split("/")
        liste.pop(-1)

        folder = liste[0]

        if not file_folder_exists(folder):
            make_folder(folder)

        for i in range(1, len(liste)):
            
            folder = folder + chr(92) + liste[i]
            if not file_folder_exists(folder):
                make_folder(folder)

def recherche_format(texte, format_texte:list):
    """Renvoie False si pas de format"""
    n = 0
    for i in range(len(texte)):
        if texte[i] == ".":
            n = i
    

    for i in range(len(format_texte)):
        test = True
        for j in range(len(format_texte[i])):

            #print(texte[n + j])
            #print(format_texte[i][j])

            if texte[n + j] != format_texte[i][j]:
                test = False
        if test:
            return True
    
    return False


def sort_files(jeu):
    

    root = url_get_root_file_filename(jeu["lien principal"])[0]
    
    
    #télécharger main
    
    download(jeu["lien principal"])
    
    
    #télécharger les autres fichers
    
    for i in range(len(jeu["autres fichiers"])):
        download(root + jeu["autres fichiers"][i])
    
    liste = []

    for i in range(len(jeu["autres fichiers"])):
        if recherche_format(jeu["autres fichiers"][i] ,[".xml", "txt"]):
            texte = read_file(url_get_root_file_filename(jeu["autres fichiers"][i])[1])
            liste += texte_to_list(texte)

    
    for i in range(len(liste)):
        download(root + liste[i])
    
    liste += jeu["autres fichiers"] + [url_get_root_file_filename(jeu["lien principal"])[1]]


    print(liste)
    for i in range(len(liste)):
        make_folder_in_folder(jeu["nom"],liste[i])
    
    for i in range(len(liste)):
        put_in_folder(str(url_get_root_file_filename(liste[i])[1]), "games" + chr(92) + jeu["nom"] + chr(92) + liste[i])

    print("done")



#Exemple:

#sort_files({"ID":"6","nom":"Lego Cars escape from profesor Z","logiciel":"flashplayer_32_sa_debug","protection":"setting.sol","lien source":"","lien principal":" http://swfurl.acool.com/upFiles/games/Escape-From-Professor-Z/downloadC229FFB5E0B4D6F2BF90E41481879D05.swf","autres fichiers":["config/filenames.xml","config/language/en.xml"],"wiki":"","code et triche":""})
#sort_files({"ID":"7","nom":"Lego Ninjago","logiciel":"flashplayer_32_sa_debug","protection":"","lien source":"http://swfurl.acool.com/upFiles/games/Escape-From-Professor-Z/load.html","lien principal":"https://media.numuki.com/ninjago/games/ninjago-rush/game.swf","autres fichiers":["config.xml"],"wiki":"","code et triche":""})
#sort_files({"ID":"8","nom":"Lego city Blue diamond chase","logiciel":"flashplayer_32_sa_debug","protection":"setting.sol","lien source":"https://f.kbhgames.com/2014/Blue-Diamond-Chase/","lien principal":"https://f.kbhgames.com/2014/Blue-Diamond-Chase/BlueDiamondChase9.swf","autres fichiers":["PreloaderGame9.swf","assets9.swf","assets/xml/config.xml"],"wiki":"","code et triche":""})
#sort_files({"ID":"9","nom":"Tomahawk","logiciel":"flashplayer_32_sa_debug","protection":"setting.sol","lien source":"https://flash.7k7k.com/cms/cms10/20130611/1156267038/Tomahawk/preloader.html","lien principal":"https://flash.7k7k.com/cms/cms10/20130611/1156267038/Tomahawk/ts.20130428T220401.preloader.swf","autres fichiers":["config.xml","sounds.xml"],"wiki":"","code et triche":""})

