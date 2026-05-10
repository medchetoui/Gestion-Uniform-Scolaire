from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory import views

# ==========================================
# CONFIGURATION GENERALE DES URLS
# ==========================================
urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Inclusion des URLs de notre application d'inventaire
    path('', include('inventory.urls')),
    
    # Authentification (Login / Logout)
    # Django fournit des vues prêtes à l'emploi. 
    # Nous devons juste créer les templates correspondants.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Inscription
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
