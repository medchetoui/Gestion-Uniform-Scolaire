from django.urls import path
from . import views

# ==========================================
# ROUTES DE L'APPLICATION INVENTORY
# ==========================================
urlpatterns = [
    # Page d'accueil publique (Landing Page)
    path('', views.home, name='home'),

    # Tableau de bord (Dashboard SaaS)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ---- Gestion des Uniformes ----
    path('uniformes/', views.UniformeListView.as_view(), name='uniform_list'),
    path('uniformes/ajouter/', views.UniformeCreateView.as_view(), name='uniform_create'),
    path('uniformes/<int:pk>/', views.UniformeDetailView.as_view(), name='uniform_detail'),
    path('uniformes/<int:pk>/modifier/', views.UniformeUpdateView.as_view(), name='uniform_update'),
    path('uniformes/<int:pk>/supprimer/', views.UniformeDeleteView.as_view(), name='uniform_delete'),
    
    # ---- Gestion des Catégories ----
    path('categories/', views.CategorieListView.as_view(), name='categorie_list'),
    path('categories/ajouter/', views.CategorieCreateView.as_view(), name='categorie_create'),
    path('categories/<int:pk>/modifier/', views.CategorieUpdateView.as_view(), name='categorie_update'),
    path('categories/<int:pk>/supprimer/', views.CategorieDeleteView.as_view(), name='categorie_delete'),

    # ---- Gestion des Fournisseurs ----
    path('fournisseurs/', views.FournisseurListView.as_view(), name='fournisseur_list'),
    path('fournisseurs/ajouter/', views.FournisseurCreateView.as_view(), name='fournisseur_create'),
    path('fournisseurs/<int:pk>/modifier/', views.FournisseurUpdateView.as_view(), name='fournisseur_update'),
    path('fournisseurs/<int:pk>/supprimer/', views.FournisseurDeleteView.as_view(), name='fournisseur_delete'),

    # Export CSV (Bonus)
    path('uniformes/export-csv/', views.export_uniforms_csv, name='uniform_export_csv'),
]
