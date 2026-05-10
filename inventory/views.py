from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q, Sum
import csv
from django.http import HttpResponse
from .models import Uniforme, Categorie, Fournisseur
from .forms import UniformeForm, CategorieForm, FournisseurForm, SimpleSignUpForm

# ==========================================
# VUE : Page d'accueil publique (Landing Page)
# ==========================================
def home(request):
    """
    Landing page moderne de type SaaS.
    Accessible sans authentification pour présenter l'application.
    Si l'utilisateur est déjà connecté, il est redirigé vers le dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

# ==========================================
# VUE : Tableau de bord (Dashboard)
# ==========================================
@login_required
def dashboard(request):
    """
    Cette vue calcule les statistiques globales pour les afficher
    sur le tableau de bord principal de type SaaS.
    """
    total_uniformes = Uniforme.objects.count()
    quantite_totale = Uniforme.objects.aggregate(total=Sum('quantite'))['total'] or 0
    
    # Stock faible : quantité < 10 mais > 0
    stock_faible = Uniforme.objects.filter(quantite__gt=0, quantite__lt=10)
    
    # Rupture de stock : quantité == 0
    rupture_stock = Uniforme.objects.filter(quantite=0)
    
    # Les 5 derniers uniformes ajoutés (pour la section "Récemment ajoutés")
    derniers_uniformes = Uniforme.objects.order_by('-date_ajout')[:5]
    
    context = {
        'total_uniformes': total_uniformes,
        'quantite_totale': quantite_totale,
        'stock_faible': stock_faible,
        'rupture_stock': rupture_stock,
        'total_categories': Categorie.objects.count(),
        'total_fournisseurs': Fournisseur.objects.count(),
        'total_ruptures': rupture_stock.count(),
        'derniers_uniformes': derniers_uniformes,
    }
    return render(request, 'inventory/dashboard.html', context)

# ==========================================
# VUE : Liste des Uniformes (avec Recherche/Filtre)
# ==========================================
class UniformeListView(LoginRequiredMixin, ListView):
    model = Uniforme
    template_name = 'inventory/uniform_list.html'
    context_object_name = 'uniformes'
    paginate_by = 12  # 12 éléments par page (grille de 3x4 cards)

    def get_queryset(self):
        """
        Cette méthode permet de filtrer les résultats en fonction de la recherche.
        Utilise les objets Q de Django pour combiner les critères de recherche.
        """
        queryset = super().get_queryset()
        
        # Récupération des paramètres de recherche/filtre depuis l'URL
        query = self.request.GET.get('q')
        categorie_id = self.request.GET.get('categorie')
        taille = self.request.GET.get('taille')
        couleur = self.request.GET.get('couleur')
        
        if query:
            # Recherche par nom, type de tenue ou couleur
            queryset = queryset.filter(
                Q(nom__icontains=query) | Q(type_tenue__icontains=query) | Q(couleur__icontains=query)
            )
        
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
            
        if taille:
            queryset = queryset.filter(taille__icontains=taille)

        if couleur:
            queryset = queryset.filter(couleur__icontains=couleur)
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute les catégories au contexte pour alimenter les filtres dans le template.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context

# ==========================================
# VUE : Détail d'un Uniforme
# ==========================================
class UniformeDetailView(LoginRequiredMixin, DetailView):
    model = Uniforme
    template_name = 'inventory/uniform_detail.html'
    context_object_name = 'uniforme'

# ==========================================
# VUES CRUD : Uniformes — Création, Modification, Suppression
# ==========================================

class UniformeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Uniforme
    form_class = UniformeForm
    template_name = 'inventory/uniform_form.html'
    success_url = reverse_lazy('uniform_list')
    success_message = "✅ L'uniforme « %(nom)s » a été ajouté avec succès !"

class UniformeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Uniforme
    form_class = UniformeForm
    template_name = 'inventory/uniform_form.html'
    success_url = reverse_lazy('uniform_list')
    success_message = "✅ L'uniforme « %(nom)s » a été modifié avec succès !"

class UniformeDeleteView(LoginRequiredMixin, DeleteView):
    model = Uniforme
    template_name = 'inventory/uniform_confirm_delete.html'
    success_url = reverse_lazy('uniform_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "🗑️ L'uniforme a été supprimé avec succès.")
        return super().post(request, *args, **kwargs)

# ==========================================
# VUES CRUD : Catégories
# ==========================================

class CategorieListView(LoginRequiredMixin, ListView):
    model = Categorie
    template_name = 'inventory/categorie_list.html'
    context_object_name = 'categories'

class CategorieCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'inventory/categorie_form.html'
    success_url = reverse_lazy('categorie_list')
    success_message = "✅ La catégorie « %(libelle)s » a été créée avec succès !"

class CategorieUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'inventory/categorie_form.html'
    success_url = reverse_lazy('categorie_list')
    success_message = "✅ La catégorie « %(libelle)s » a été modifiée avec succès !"

class CategorieDeleteView(LoginRequiredMixin, DeleteView):
    model = Categorie
    template_name = 'inventory/categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "🗑️ La catégorie a été supprimée avec succès.")
        return super().post(request, *args, **kwargs)

# ==========================================
# VUES CRUD : Fournisseurs
# ==========================================

class FournisseurListView(LoginRequiredMixin, ListView):
    model = Fournisseur
    template_name = 'inventory/fournisseur_list.html'
    context_object_name = 'fournisseurs'

class FournisseurCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'inventory/fournisseur_form.html'
    success_url = reverse_lazy('fournisseur_list')
    success_message = "✅ Le fournisseur « %(nom_societe)s » a été ajouté avec succès !"

class FournisseurUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'inventory/fournisseur_form.html'
    success_url = reverse_lazy('fournisseur_list')
    success_message = "✅ Le fournisseur « %(nom_societe)s » a été modifié avec succès !"

class FournisseurDeleteView(LoginRequiredMixin, DeleteView):
    model = Fournisseur
    template_name = 'inventory/fournisseur_confirm_delete.html'
    success_url = reverse_lazy('fournisseur_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "🗑️ Le fournisseur a été supprimé avec succès.")
        return super().post(request, *args, **kwargs)

# ==========================================
# VUE : Inscription (Sign Up)
# ==========================================
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SimpleSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    success_message = "✅ Compte créé avec succès ! Connectez-vous maintenant."

# ==========================================
# BONUS : Export CSV des données
# ==========================================
@login_required
def export_uniforms_csv(request):
    """
    Exporte la liste complète des uniformes au format CSV pour Excel/LibreOffice.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventaire_uniformes.csv"'

    writer = csv.writer(response)
    # En-têtes des colonnes
    writer.writerow(['Nom', 'Type', 'Taille', 'Couleur', 'Quantité', 'Prix', 'Catégorie', 'Fournisseur'])

    uniformes = Uniforme.objects.all()
    for item in uniformes:
        writer.writerow([
            item.nom,
            item.type_tenue,
            item.taille,
            item.couleur,
            item.quantite,
            item.prix,
            item.categorie.libelle if item.categorie else "",
            item.fournisseur.nom_societe if item.fournisseur else ""
        ])

    return response

# ==========================================
# VUE : Page 404 personnalisée
# ==========================================
def handler404_view(request, exception):
    """Vue personnalisée pour les erreurs 404 (Page non trouvée)."""
    return render(request, '404.html', status=404)
