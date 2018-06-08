# GrandPy bot
## Installation
* Récupérer le projet : En ligne de commande, dans le répertoire souhaité, lancer la commande : "https://github.com/msadour/oc-grandpybot.git"
* Installer les dépendances : Une fois le projet récupéré, en ligne de commande, placer vous dans le dossier du projet et lancer la commande suivante : "pip install -r requirements.txt".

## Lancement
* en local,  le programme se lance en ligne de coommande via le fichier app.py (se trouvant à la racine du projet) avec la commande suivante : python app.py. Une fois lancé, allez sur votre navigateur et entrez l'url suivante : http://127.0.0.1:5000/ ;
* En ligne, allez sur l'adresse suivante : https://oc-grandpybot.herokuapp.com/

## Utilisation
Au sein du formulaire, posez votre question à GrandPy et cliquez sur le bouton "Racontes moi !". 

## 4 cas possible
* L'application vous retourne une description wikipedia et son emplacement sur google maps ;
* L'application vous retourne uniquement la description sans l'emplacement (un message d'erreur relatif à l'emplacement apparaitra) ;
* L'application vous retourne uniquement l'emplacement sans la description (un message d'erreur relatif à la description apparaitra) ;
* L'application vous retourne aucun resultat et un message d'erreur apparaitra vous indiquant qu'il n'a trouvé ni l'emplacement ni la description.