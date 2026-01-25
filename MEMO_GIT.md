# 📝 MÉMENTO GIT - ROUTINE QUOTIDIENNE

Ce fichier sert de rappel pour les commandes à utiliser dans le terminal de VS Code.

# 1. ☀️ LE MATIN (Avant de commencer)
Toujours s'assurer d'avoir la dernière version (surtout si tu changes d'ordi).
-> git pull
-> source .venv/bin/activate

# 2. 🌙 LA ROUTINE DE SAUVEGARDE (Le "Carton")
À faire à chaque fois que tu finis une fonctionnalité ou avant d'arrêter de travailler.

# Étape A : Vérifier l'état (Quels fichiers ont changé ?)
-> git status (Les fichiers en ROUGE sont modifiés mais pas encore prêts à être sauvegardés)

# Étape B : Remplir le carton (Tout préparer)
-> git add . (Le point . signifie "Ajoute TOUS les fichiers modifiés dans le carton")

# Étape C : Fermer le carton et étiqueter (La "Photo")
-> git commit -m "Description de ce que j'ai fait"

    Exemple : git commit -m "Ajout du graphique RSI et nettoyage du code" 
    Les fichiers sont maintenant sauvegardés sur ton PC (localement)

# Étape D : Envoyer le camion (Synchroniser avec le Cloud)
-> git push (Tes modifications sont maintenant sécurisées sur GitHub)

# 3. 🌳 LES BRANCHES (Pour tester sans risque)
Utile si tu veux tester une idée complexe (ex: "Ajout Crypto") sans casser ton site principal qui marche.
    Créer une nouvelle branche et aller dessus (Créer un univers parallèle) :
        -> git checkout -b nom-de-ma-branche
    
    Revenir sur la branche principale (Retour à la normale) :
        -> git checkout main

    Fusionner ta branche dans le projet principal (Si le test est réussi) :
        1. Revenir sur main : git checkout main
        2. Fusionner : git merge nom-de-ma-branche
        3. Supprimer la branche de test (optionnel) : git branch -d nom-de-ma-branche

# 4. 🆘 BOUTON PANIQUE
J'ai tout cassé et je veux revenir à ma dernière sauvegarde propre : 
⚠️ Attention : Cela efface tout le travail non sauvegardé depuis le dernier commit.
-> git restore .

    Voir l'historique de ce qui a été fait :
    -> git log (Appuie sur q pour quitter l'affichage du log)


