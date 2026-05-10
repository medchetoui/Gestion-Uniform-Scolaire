from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Uniforme, Categorie, Fournisseur

# ==========================================
# FORMULAIRE : UniformeForm
# ==========================================
# Ce formulaire est utilisé pour ajouter ou modifier un uniforme.
# On utilise ModelForm pour lier directement le formulaire au modèle Uniforme.
class UniformeForm(forms.ModelForm):
    class Meta:
        model = Uniforme
        # On définit les champs qui seront modifiables par l'utilisateur
        fields = ['nom', 'type_tenue', 'taille', 'couleur', 'quantite', 'prix', 'image', 'categorie', 'fournisseur']
        
        # Widgets pour personnaliser l'apparence des champs du formulaire
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Ex: Chemise blanche cérémonie'}),
            'type_tenue': forms.Select(attrs={'class': 'form-select'}),
            'taille': forms.TextInput(attrs={'placeholder': 'Ex: M, L ou 10 ans'}),
            'couleur': forms.TextInput(attrs={'placeholder': 'Ex: Bleu Marine'}),
            'quantite': forms.NumberInput(attrs={'min': 0}),
            'prix': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'placeholder': 'Ex: 150.00'}),
        }

# ==========================================
# FORMULAIRE : CategorieForm
# ==========================================
# Formulaire pour créer ou modifier une catégorie d'uniformes.
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['libelle', 'niveau_scolaire']
        widgets = {
            'libelle': forms.TextInput(attrs={'placeholder': 'Ex: Tenue de sport'}),
            'niveau_scolaire': forms.Select(attrs={'class': 'form-select'}),
        }

# ==========================================
# FORMULAIRE : FournisseurForm
# ==========================================
# Formulaire pour créer ou modifier un fournisseur.
class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom_societe', 'contact', 'delai_livraison']
        widgets = {
            'nom_societe': forms.TextInput(attrs={'placeholder': 'Ex: TextilePro SARL'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Ex: contact@textilepro.ma'}),
            'delai_livraison': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Ex: 15'}),
        }

# ==========================================
# FORMULAIRE : SimpleSignUpForm
# ==========================================
# Un formulaire d'inscription épuré pour éviter les longs textes 
# d'aide générés par défaut par Django.
class SimpleSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On supprime les textes d'aide par défaut pour rendre l'interface plus propre
        if 'username' in self.fields:
            self.fields['username'].help_text = None
