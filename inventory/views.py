from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Sum
import csv
from django.http import HttpResponse
from .models import Uniforme, Categorie, Fournisseur
from .forms import UniformeForm

# ==========================================
# VUE : Tableau de bord (Dashboard)
# ==========================================
@login_required
def dashboard(request):
    """
    Cette vue calcule les statistiques globales pour les afficher sur la page d'accueil.
    """
    total_uniformes = Uniforme.objects.count()
    quantite_totale = Uniforme.objects.aggregate(total=Sum('quantite'))['total'] or 0
    
    # Stock faible : quantité < 10 mais > 0
    stock_faible = Uniforme.objects.filter(quantite__gt=0, quantite__lt=10)
    
    # Rupture de stock : quantité == 0
    rupture_stock = Uniforme.objects.filter(quantite=0)
    
    context = {
        'total_uniformes': total_uniformes,
        'quantite_totale': quantite_totale,
        'stock_faible': stock_faible,
        'rupture_stock': rupture_stock,
        'total_categories': Categorie.objects.count(),
        'total_fournisseurs': Fournisseur.objects.count(),
    }
    return render(request, 'inventory/dashboard.html', context)

# ==========================================
# VUE : Liste des Uniformes (avec Recherche/Filtre)
# ==========================================
class UniformeListView(LoginRequiredMixin, ListView):
    model = Uniforme
    template_name = 'inventory/uniform_list.html'
    context_object_name = 'uniformes'
    paginate_by = 10 # Pagination : 10 éléments par page

    def get_queryset(self):
        """
        Cette méthode permet de filtrer les résultats en fonction de la recherche.
        """
        queryset = super().get_queryset()
        
        # Récupération des paramètres de recherche/filtre depuis l'URL
        query = self.request.GET.get('q')
        categorie_id = self.request.GET.get('categorie')
        taille = self.request.GET.get('taille')
        
        if query:
            # Recherche par type de tenue ou couleur
            queryset = queryset.filter(
                Q(type_tenue__icontains=query) | Q(couleur__icontains=query)
            )
        
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
            
        if taille:
            queryset = queryset.filter(taille__icontains=taille)
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute les catégories au contexte pour alimenter le filtre dans le template.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context

# ==========================================
# VUES CRUD : Création, Modification, Suppression
# ==========================================

class UniformeCreateView(LoginRequiredMixin, CreateView):
    model = Uniforme
    form_class = UniformeForm
    template_name = 'inventory/uniform_form.html'
    success_url = reverse_lazy('uniform_list') # Redirection après succès

class UniformeUpdateView(LoginRequiredMixin, UpdateView):
    model = Uniforme
    form_class = UniformeForm
    template_name = 'inventory/uniform_form.html'
    success_url = reverse_lazy('uniform_list')

class UniformeDeleteView(LoginRequiredMixin, DeleteView):
    model = Uniforme
    template_name = 'inventory/uniform_confirm_delete.html'
    success_url = reverse_lazy('uniform_list')

# ==========================================
# VUE : Inscription (Sign Up)
# ==========================================
class SignUpView(CreateView):
    from .forms import SimpleSignUpForm
    form_class = SimpleSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login') # Redirige vers la connexion après inscription

# ==========================================
# BONUS : Export CSV des données
# ==========================================
@login_required
def export_uniforms_csv(request):
    """
    Exporte la liste des uniformes au format CSV pour Excel/LibreOffice.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventaire_uniformes.csv"'

    writer = csv.writer(response)
    # En-têtes des colonnes
    writer.writerow(['Type', 'Taille', 'Couleur', 'Quantité', 'Catégorie', 'Fournisseur'])

    uniformes = Uniforme.objects.all()
    for item in uniformes:
        writer.writerow([
            item.type_tenue,
            item.taille,
            item.couleur,
            item.quantite,
            item.categorie.libelle if item.categorie else "",
            item.fournisseur.nom_societe if item.fournisseur else ""
        ])

    return response

