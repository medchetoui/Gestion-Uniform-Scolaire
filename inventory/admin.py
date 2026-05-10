from django.contrib import admin
from .models import Categorie, Fournisseur, Uniforme

# ==========================================
# CONFIGURATION ADMIN : Categorie
# ==========================================
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des catégories
    list_display = ('libelle', 'niveau_scolaire')
    # Ajoute un panneau de filtre par niveau scolaire sur le côté droit
    list_filter = ('niveau_scolaire',)
    # Permet de rechercher par le nom de la catégorie
    search_fields = ('libelle',)

# ==========================================
# CONFIGURATION ADMIN : Fournisseur
# ==========================================
@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    # Colonnes affichées pour les fournisseurs
    list_display = ('nom_societe', 'contact', 'delai_livraison')
    # Recherche par nom de société
    search_fields = ('nom_societe',)

# ==========================================
# CONFIGURATION ADMIN : Uniforme
# ==========================================
@admin.register(Uniforme)
class UniformeAdmin(admin.ModelAdmin):
    # Affiche ces champs dans la liste principale des uniformes
    list_display = ('type_tenue', 'categorie', 'taille', 'couleur', 'quantite', 'fournisseur', 'statut_stock')
    # Filtres latéraux très utiles pour la gestion
    list_filter = ('categorie', 'type_tenue', 'taille', 'couleur')
    # Barre de recherche pour trouver rapidement un vêtement
    search_fields = ('type_tenue', 'couleur', 'taille', 'categorie__libelle')
    # Permet de modifier directement la quantité depuis la vue liste sans entrer dans les détails
    list_editable = ('quantite',)

    # Méthode personnalisée pour afficher le statut du stock avec un code couleur
    @admin.display(description='Statut Stock')
    def statut_stock(self, obj):
        if obj.est_rupture:
            # En rupture de stock = Rouge
            return "🔴 Rupture"
        elif obj.est_stock_faible:
            # Stock faible (<10) = Orange
            return "🟠 Faible"
        else:
            # Stock normal = Vert
            return "🟢 Normal"
