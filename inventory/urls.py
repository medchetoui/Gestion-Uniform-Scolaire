from django.urls import path
from . import views

# ==========================================
# ROUTES DE L'APPLICATION INVENTORY
# ==========================================
urlpatterns = [
    # Page d'accueil / Tableau de bord
    path('', views.dashboard, name='dashboard'),
    
    # Gestion des uniformes (Liste et Recherche)
    path('uniformes/', views.UniformeListView.as_view(), name='uniform_list'),
    
    # Actions CRUD sur les uniformes
    path('uniformes/ajouter/', views.UniformeCreateView.as_view(), name='uniform_create'),
    path('uniformes/<int:pk>/modifier/', views.UniformeUpdateView.as_view(), name='uniform_update'),
    path('uniformes/<int:pk>/supprimer/', views.UniformeDeleteView.as_view(), name='uniform_delete'),
    
    # Export CSV (Bonus)
    path('uniformes/export-csv/', views.export_uniforms_csv, name='uniform_export_csv'),
]
