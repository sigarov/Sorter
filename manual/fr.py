"""Manuel français — traduction de l'original allemand manual/de.py."""

FR = {
    "title": "Mode d'emploi",
    "sections": [
        {
            "id": "intro",
            "title": "1. Ce que fait le programme",
            "text": (
                "Le trieur de médias classe les images et les vidéos dans une structure de "
                "dossiers fixe, puis aide à supprimer les doublons de noms.\n\n"
                "Vous choisissez une ou deux sources (dossiers ou disques entiers) et un "
                "dossier cible. Le programme lit toutes les images et vidéos, détermine la "
                "date de prise de vue et copie chaque fichier dans le dossier de l'année, du "
                "mois et du jour correspondants.\n\n"
                "Bon à savoir :\n"
                "• Les sources sont seulement lues, jamais modifiées.\n"
                '• Rien n\'est supprimé. Les doublons vont dans le dossier "Duplicates".\n'
                "• Les noms des dossiers de la cible sont toujours en anglais (Pictures, "
                "Videos, _No_Date). La structure reste ainsi stable lors d'un changement de "
                "langue.\n"
                "• L'interface est disponible en sept langues. Ce manuel s'affiche dans la "
                "langue choisie dès qu'une traduction existe — en attendant, en allemand."
            ),
        },
        {
            "id": "start",
            "title": "2. Premiers pas",
            "text": (
                "1. Choisissez la langue en haut à gauche — l'affichage change immédiatement.\n"
                "2. Choisissez la source 1 : dossier ou disque. Ajoutez éventuellement la "
                "source 2.\n"
                "3. Choisissez la cible : c'est là que le tri sera effectué.\n"
                "4. Activez éventuellement l'essai à blanc pour simuler le déroulement.\n"
                '5. Cliquez sur "▶  Démarrer" (ou appuyez sur F5).\n\n'
                "Pendant l'exécution, deux barres de progression indiquent l'état : d'abord "
                'l\'indexation de la cible, puis le tri. Le bouton "■  Arrêter" (ou Échap) '
                "interrompt le travail ; les fichiers déjà copiés sont conservés.\n\n"
                "L'onglet \"Nettoyer\" n'est déverrouillé qu'après un vrai tri dans la cible "
                "choisie."
            ),
        },
        {
            "id": "sort",
            "title": "3. Tri et structure des dossiers",
            "text": (
                "Le tri comporte deux phases :\n"
                "1. Le dossier cible est indexé. La taille, la date de modification et la "
                "somme de contrôle (hash) de tous les fichiers existants sont enregistrées.\n"
                "2. Chaque fichier source est vérifié et copié dans le dossier cible.\n\n"
                "La date est déterminée dans cet ordre :\n"
                "• Date de prise de vue EXIF de l'image (nécessite Pillow)\n"
                "• Métadonnées de la vidéo (nécessite ffprobe dans le PATH)\n"
                "• Date tirée du nom du fichier, par ex. 2020-05-17, 20200517 ou "
                "20200517_143025\n\n"
                "La date du système de fichiers n'est volontairement pas utilisée : les "
                "fichiers sans véritable horodatage doivent aller dans le dossier _No_Date "
                "plutôt que d'être mal classés selon leur date de copie.\n\n"
                "Structure dans la cible (exemple) :\n"
                "• Pictures/2020/05/17/vacances.jpg\n"
                "• Videos/2020/05/17/vacances.mp4\n"
                "• _No_Date/Pictures/inconnu.jpg\n\n"
                "Si un fichier cible existe déjà et que le contenu est identique, le fichier "
                "source est ignoré. Si le nom est identique mais le contenu différent, des "
                "fichiers _1, _2, etc. sont créés. Avant la copie, le programme vérifie "
                "l'espace disque libre et compare la taille du fichier après la copie."
            ),
        },
        {
            "id": "names",
            "title": "4. Noms de fichiers",
            "text": (
                "Six variantes de nouveaux noms de fichiers (exemple : vacances.jpg du "
                "17/05/2020, 14:30:25) :\n\n"
                "• Original : vacances.jpg\n"
                "• Date_Nom : 20200517_vacances.jpg\n"
                "• Date_Heure_Nom : 20200517_143025_vacances.jpg\n"
                "• Année-Mois-Jour_Nom : 2020-05-17_vacances.jpg\n"
                "• Numéro : 00001.jpg\n"
                "• Date_Numéro : 20200517_0001.jpg\n\n"
                'Sans date, "Numéro" n\'attribue que le numéro courant ; pour toutes les '
                "autres variantes, le nom d'origine est conservé. L'extension est toujours en "
                "minuscules. En cas de nom identique, le programme ajoute _1, _2, ..."
            ),
        },
        {
            "id": "structure",
            "title": "5. Structure : séparée ou commune",
            "text": (
                "Séparée (par défaut) : les images et les vidéos sont dans des arborescences "
                "distinctes.\n"
                "  Pictures/2020/05/17/... et Videos/2020/05/17/...\n"
                "Commune : les deux vont dans le même dossier année/mois/jour.\n"
                "  2020/05/17/...\n\n"
                "Granularité :\n"
                "• Année : 2020/\n"
                "• Mois : 2020/05/\n"
                "• Jour : 2020/05/17/\n\n"
                'Les fichiers sans date vont dans _No_Date — avec "Séparée", en plus sous '
                "Pictures ou Videos. Là, le fichier _liste.txt répertorie tous les fichiers "
                "concernés."
            ),
        },
        {
            "id": "filters",
            "title": "6. Filtrer les dossiers",
            "text": (
                "Le champ de filtre limite les sous-dossiers de la source à parcourir.\n"
                "• Séparez plusieurs termes par des virgules : Photos, Pictures, DCIM\n"
                "• Seuls les noms de dossiers comptent, pas les extensions de fichiers.\n"
                "• La casse n'a pas d'importance.\n"
                "• Une correspondance s'applique aussi à tous les sous-dossiers.\n"
                "• Champ vide = source entière.\n\n"
                'Exemple : D:\\Backup contient "Photos", "Documents" et "Vidéos". Avec le '
                'filtre "Photos, Vidéos", seuls ces deux dossiers sont lus.\n\n'
                "L'onglet \"Nettoyer\" n'a pas de filtre : c'est toujours tout le dossier cible "
                "qui est vérifié."
            ),
        },
        {
            "id": "dryrun",
            "title": "7. Essai à blanc et cache d'index",
            "text": (
                "L'essai à blanc montre ce qui se passerait sans rien modifier :\n"
                "• Rien n'est copié, déplacé ni renommé.\n"
                "• Aucun fichier _index.txt n'est créé ; un essai à blanc ne déverrouille donc "
                'pas l\'onglet "Nettoyer".\n'
                "• Les actions prévues figurent dans le journal et dans _log_dry.txt.\n\n"
                "L'essai à blanc lit néanmoins le dossier cible et enregistre un cache de "
                "hash dans le dossier de l'application. Le prochain vrai passage utilise ce "
                "cache puis le supprime. Cela fait gagner beaucoup de temps lors du deuxième "
                "passage."
            ),
        },
        {
            "id": "dedup",
            "title": "8. Nettoyer les doublons",
            "text": (
                'L\'onglet "Nettoyer" élimine les doublons de noms apparus lors du tri. Il '
                "travaille exclusivement dans le dossier cible et n'est déverrouillé qu'après "
                "un vrai tri dans ce dossier (reconnaissable à _index.txt).\n\n"
                "Groupes : NAME.jpg, NAME_1.jpg, NAME_2.jpg ... vont ensemble.\n\n"
                "Règle standard :\n"
                "• Si un fichier _1, _2 est identique octet par octet au fichier de base, il "
                "est déplacé vers Duplicates. Le fichier de base reste dans le dossier cible.\n"
                "• Le fichier de base est copié une fois par groupe vers Duplicates afin que "
                "vous puissiez comparer directement les deux versions.\n"
                "• Si le contenu diffère, le fichier reste inchangé.\n\n"
                "Règle étendue (Force) :\n"
                "• Les fichiers _1, _2 au contenu différent sont eux aussi déplacés vers "
                "Duplicates — sans comparaison du contenu. Le programme demande d'abord "
                "confirmation.\n"
                "• Prévu pour les sauvegardes portant le même nom et pour deux appareils photo "
                "ayant par hasard le même nom de fichier.\n\n"
                "Si le fichier de base manque, le plus petit numéro est renommé en nom de base "
                "(IMG_1.jpg -> IMG.jpg). Le fichier reste dans le dossier cible.\n\n"
                "Rien n'est supprimé : Duplicates reproduit la structure des dossiers et est "
                "ignoré lors du prochain tri. C'est à vous de faire le nettoyage. L'essai à "
                "blanc fonctionne aussi ici et n'écrit que dans le journal de l'essai."
            ),
        },
        {
            "id": "skip",
            "title": "9. Ignorer les fichiers existants",
            "text": (
                '"Ignorer les fichiers existants" empêche la création de fichiers _1, _2 : si '
                "le fichier cible existe déjà, il reste inchangé et le fichier source est "
                "ignoré.\n\n"
                "Cette option est prévue pour les sauvegardes enregistrées avec des horodatages "
                "différents : au lieu de créer une seconde version sous forme de fichier _1, "
                "la première est conservée. Dans le journal, ces fichiers apparaissent comme "
                "SKIP (existe) et comptent comme doublons.\n\n"
                "Sans cette option, des fichiers de même nom deviennent des fichiers _1, _2, "
                'que vous pourrez vérifier plus tard dans l\'onglet "Nettoyer".'
            ),
        },
        {
            "id": "log",
            "title": "10. Fenêtre du journal",
            "text": (
                "Le journal affiche toutes les actions du passage, avec un code couleur :\n"
                "• bleu : informations\n"
                "• jaune : avertissements\n"
                "• rouge : erreurs\n"
                "• vert : rapport/résumé\n\n"
                "Commandes :\n"
                '• "Erreurs seulement" : masque tout le reste.\n'
                '• "Défilement auto" : va automatiquement à la fin.\n'
                "• Champ de recherche + Entrée : passe à la correspondance suivante (casse "
                "ignorée).\n"
                '• "Effacer" (Ctrl+L), "Enregistrer" (Ctrl+S), "Ouvrir".\n\n'
                "Le journal est limité à 50 000 lignes pour que les longs passages ne saturent "
                "pas la mémoire. Le dossier cible contient en plus _log.txt ; lors d'un essai "
                "à blanc, _log_dry.txt à la place."
            ),
        },
        {
            "id": "settings",
            "title": "11. Réglages, emplacement et langue",
            "text": (
                "Les données sont enregistrées dans le répertoire utilisateur sous "
                "~/.medien_sortierer :\n"
                "• settings.json : taille de la fenêtre, langue et derniers dossiers choisis\n"
                "• app.log : journal technique du programme\n\n"
                "Les réglages sont écrits à la fermeture et rechargés au prochain démarrage. "
                "La langue s'applique immédiatement, sans redémarrage.\n\n"
                "Après un vrai passage, le dossier cible contient :\n"
                "• _index.txt : index des fichiers pour accélérer les passages suivants et "
                'marqueur "déjà trié" (déverrouille l\'onglet "Nettoyer")\n'
                "• _log.txt : journal du passage\n"
                "• Duplicates : doublons de noms mis de côté\n\n"
                "Si la source est identique à la cible, le programme trie automatiquement dans "
                "le sous-dossier Sorted. Le dossier cible lui-même n'est jamais parcouru comme "
                "source."
            ),
        },
        {
            "id": "keys",
            "title": "12. Raccourcis clavier et dépannage",
            "text": (
                "Raccourcis clavier :\n"
                "• F1 — ouvrir ce manuel\n"
                "• F5 — démarrer le passage\n"
                "• Échap — arrêter le passage\n"
                "• Ctrl+L — effacer le journal\n"
                "• Ctrl+S — enregistrer le journal\n\n"
                "Les petits boutons ? à côté des groupes affichent de courtes indications sur "
                "la zone concernée.\n\n"
                "Si quelque chose ne se passe pas comme prévu :\n"
                "• Tout finit dans _No_Date : aucune date n'a été trouvée. Installez Pillow "
                "pour les données EXIF et fournissez ffprobe pour les vidéos.\n"
                "• L'onglet \"Nettoyer\" est verrouillé : aucun vrai tri n'a encore eu lieu "
                "dans cette cible. Triez d'abord — un essai à blanc ne suffit pas.\n"
                "• Les fichiers s'appellent _1, _2 : il y a eu un conflit de noms. Faites le "
                'nettoyage dans l\'onglet "Nettoyer".\n'
                "• Des fichiers manquent après le tri : ils existaient déjà avec le même "
                "contenu et ont été ignorés comme doublons — le journal les indique comme "
                "DUP.\n"
                '• Le passage s\'arrête avec "Espace disque insuffisant" : libérez de la place '
                "dans la cible ou choisissez un autre disque cible."
            ),
        },
    ],
}
