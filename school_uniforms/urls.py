from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
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
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Inscription
    path('signup/', views.SignUpView.as_view(), name='signup'),
]

# En mode développement, Django sert aussi les fichiers média (images uploadées)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Page 404 personnalisée (active uniquement quand DEBUG=False)
handler404 = 'inventory.views.handler404_view'
