# SchoolUniforms - Gestion des Uniformes Scolaires

Application full-stack développée avec Django et Bootstrap 5 pour la gestion simplifiée des stocks d'uniformes.

## Fonctionnalités
- **Tableau de bord** : Statistiques en temps réel et alertes de stock (faible/rupture).
- **Gestion des stocks** : CRUD complet pour les uniformes.
- **Recherche & Filtres** : Filtrage par catégorie, taille et recherche textuelle.
- **Administration** : Interface Django Admin optimisée pour gérer les catégories et fournisseurs.
- **Sécurité** : Système d'authentification complet.
- **Bonus** : Export des données en format CSV.

## Installation et Exécution

1. **Activer l'environnement virtuel** :
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Appliquer les migrations** (déjà fait lors de la création, mais utile si vous changez de machine) :
   ```bash
   python manage.py migrate
   ```

3. **Créer un super-utilisateur (Admin)** :
   ```bash
   python manage.py createsuperuser
   ```
   *Suivez les instructions pour créer votre compte administrateur.*

4. **Lancer le serveur** :
   ```bash
   python manage.py runserver
   ```

5. **Accéder à l'application** :
   - Interface utilisateur : `http://127.0.0.1:8000/`
   - Interface Admin : `http://127.0.0.1:8000/admin/`

## Structure du projet
- `inventory/` : Application principale contenant les modèles, vues et formulaires.
- `school_uniforms/` : Configuration du projet (settings, urls).
- `templates/` : Fichiers HTML utilisant le moteur de template Django.
- `static/` : Fichiers CSS personnalisés (si ajoutés).
