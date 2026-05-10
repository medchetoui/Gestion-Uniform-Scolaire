from django.db import models

# ==========================================
# MODEL: Categorie
# ==========================================
# Ce modèle représente les différentes catégories d'uniformes.
# Par exemple : Tenue de sport, Cérémonie, Quotidienne.
class Categorie(models.Model):
    # Les choix pour le niveau scolaire (Primaire, Collège, Lycée)
    NIVEAU_CHOICES = [
        ('Primaire', 'Primaire'),
        ('Collège', 'Collège'),
        ('Lycée', 'Lycée'),
    ]

    # Le nom de la catégorie (ex: Tenue de sport)
    libelle = models.CharField(max_length=100, verbose_name="Libellé de la catégorie")
    
    # Le niveau scolaire associé, choisi depuis la liste NIVEAU_CHOICES
    niveau_scolaire = models.CharField(max_length=50, choices=NIVEAU_CHOICES, verbose_name="Niveau Scolaire")

    def __str__(self):
        # Cette méthode définit comment l'objet s'affiche dans l'administration Django ou les listes.
        return f"{self.libelle} ({self.niveau_scolaire})"

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

# ==========================================
# MODEL: Fournisseur
# ==========================================
# Ce modèle sert à enregistrer les informations des fournisseurs.
class Fournisseur(models.Model):
    # Le nom de l'entreprise fournissant les uniformes
    nom_societe = models.CharField(max_length=150, verbose_name="Nom de la société")
    
    # Les coordonnées du fournisseur (numéro, email, etc.)
    contact = models.CharField(max_length=150, verbose_name="Contact (Email/Tél)")
    
    # Le délai moyen de livraison en jours
    delai_livraison = models.IntegerField(verbose_name="Délai de livraison (en jours)", help_text="Ex: 15 pour 15 jours")

    def __str__(self):
        return self.nom_societe

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

# ==========================================
# MODEL: Uniforme
# ==========================================
# Ce modèle est le cœur de l'application, il gère le stock de chaque uniforme.
class Uniforme(models.Model):
    # Différents types de vêtements possibles
    TYPE_CHOICES = [
        ('Chemise', 'Chemise'),
        ('Pantalon', 'Pantalon'),
        ('Jupe', 'Jupe'),
        ('Pull', 'Pull'),
        ('T-shirt', 'T-shirt'),
        ('Survêtement', 'Survêtement'),
    ]

    # Nom descriptif de l'uniforme (ex: "Chemise blanche cérémonie")
    nom = models.CharField(max_length=200, verbose_name="Nom de l'uniforme", default="Uniforme")

    # Le type du vêtement
    type_tenue = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Type de tenue")
    
    # La taille (S, M, L, XL ou l'âge ex: '10 ans')
    taille = models.CharField(max_length=20, verbose_name="Taille")
    
    # La couleur de l'uniforme
    couleur = models.CharField(max_length=50, verbose_name="Couleur")
    
    # La quantité actuellement en stock. 
    # Un entier positif ou nul (pas de stock négatif).
    quantite = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")

    # Le prix unitaire de l'uniforme en dirhams (MAD)
    prix = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Prix unitaire (MAD)")

    # Image du produit (optionnelle). Les images seront stockées dans le dossier media/uniformes/
    image = models.ImageField(upload_to='uniformes/', blank=True, null=True, verbose_name="Photo du produit")

    # Date de création automatique pour trier par "derniers ajoutés"
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    
    # Clé étrangère vers le modèle Categorie : un uniforme appartient à une seule catégorie, 
    # mais une catégorie peut avoir plusieurs uniformes.
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="uniformes", verbose_name="Catégorie")
    
    # Clé étrangère optionnelle vers Fournisseur : On peut enregistrer un uniforme 
    # sans fournisseur immédiatement (null=True, blank=True).
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True, related_name="uniformes", verbose_name="Fournisseur")

    def __str__(self):
        return f"{self.nom} - {self.type_tenue} ({self.taille})"

    # Propriété calculée pour savoir si le stock est faible (ex: moins de 10)
    @property
    def est_stock_faible(self):
        return self.quantite > 0 and self.quantite < 10

    # Propriété calculée pour savoir si l'article est en rupture
    @property
    def est_rupture(self):
        return self.quantite == 0

    class Meta:
        ordering = ['-date_ajout']  # Les plus récents en premier
        verbose_name = "Uniforme"
        verbose_name_plural = "Uniformes"
