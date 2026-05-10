from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Fournisseur, Uniforme

# ==========================================
# CONFIGURATION ADMIN : Categorie
# ==========================================
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des catégories
    list_display = ('libelle', 'niveau_scolaire', 'nombre_uniformes')
    # Ajoute un panneau de filtre par niveau scolaire sur le côté droit
    list_filter = ('niveau_scolaire',)
    # Permet de rechercher par le nom de la catégorie
    search_fields = ('libelle',)

    # Colonne personnalisée : nombre d'uniformes dans cette catégorie
    @admin.display(description="Nb. Uniformes")
    def nombre_uniformes(self, obj):
        return obj.uniformes.count()

# ==========================================
# CONFIGURATION ADMIN : Fournisseur
# ==========================================
@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    # Colonnes affichées pour les fournisseurs
    list_display = ('nom_societe', 'contact', 'delai_livraison', 'nombre_produits')
    # Recherche par nom de société
    search_fields = ('nom_societe',)

    # Colonne personnalisée : nombre de produits fournis
    @admin.display(description="Nb. Produits")
    def nombre_produits(self, obj):
        return obj.uniformes.count()

# ==========================================
# CONFIGURATION ADMIN : Uniforme
# ==========================================
@admin.register(Uniforme)
class UniformeAdmin(admin.ModelAdmin):
    # Affiche ces champs dans la liste principale des uniformes
    list_display = ('nom', 'type_tenue', 'categorie', 'taille', 'couleur', 'quantite', 'prix', 'fournisseur', 'apercu_image', 'statut_stock')
    # Filtres latéraux très utiles pour la gestion
    list_filter = ('categorie', 'type_tenue', 'taille', 'couleur')
    # Barre de recherche pour trouver rapidement un vêtement
    search_fields = ('nom', 'type_tenue', 'couleur', 'taille', 'categorie__libelle')
    # Permet de modifier directement la quantité et le prix depuis la vue liste
    list_editable = ('quantite', 'prix')

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

    # Affiche une miniature de l'image dans la liste admin
    @admin.display(description='Image')
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:cover; border-radius:6px;" />', obj.image.url)
        return "—"
