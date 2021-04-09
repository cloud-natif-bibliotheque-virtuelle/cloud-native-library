# cloud_natif_bibliotheque_virtuelle


**Main.py (Script upload) :**

Pour upload le livre dans le blob , lui donner un titre, lui ajouter des informations, un url et les mots que le livre contient.

Pour l'activer 'python main.py upload "chemin du fichier"'




**Blob trigger final :**

Se déclenche à chaque action. Via la def main qui se connecte à la base de données (MYSQL) et compte le nombre de mots et les insère dans la colonne 'nombre de mots'.

Pour l'activer : F5 en local ou la flèche dans Azure pour deploy.




**HTTP TRIGGER INIT : **

Pour afficher la liste des livres via la def main reliée à la database. Est relié avec la page HTML ' index 1' pour lister les livres en liens cliquable.

Pour l'activer : F5 en local ou la flèche dans Azure pour deploy.




**HTTP TRIGGER INIT : **

Via le liens cliquable, récupère les informations dans la database, va afficher les informations du livre (titre, informations, URL, liste de mots que le livre contient).

Est relié avec la page HTML ' index 2' pour lister les livres en liens cliquable.

Pour l'activer : F5 en local ou la flèche dans Azure pour deploy.




**Variables d'environnement :**

Servent à cacher des informations sensibles, elles sont à rentrer dans votre pc et sur Azure (fonction> Paramètres> Configuration> Nouveaux paramètres d'APP).

**MYSQL :**

N'oubliez pas d'entrer votre adresse IP sur Azure, à chaque fois que vous vous connectez sur un nouveau réseau.
