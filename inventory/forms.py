from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Uniforme

# ==========================================
# FORMULAIRE : UniformeForm
# ==========================================
# Ce formulaire est utilisé pour ajouter ou modifier un uniforme.
# On utilise ModelForm pour lier directement le formulaire au modèle Uniforme.
class UniformeForm(forms.ModelForm):
    class Meta:
        model = Uniforme
        # On définit les champs qui seront modifiables par l'utilisateur
        fields = ['type_tenue', 'taille', 'couleur', 'quantite', 'categorie', 'fournisseur']
        
        # On peut ajouter des widgets pour personnaliser l'apparence si besoin,
        # mais Crispy Forms s'occupera du gros du travail de design.
        widgets = {
            'type_tenue': forms.Select(attrs={'class': 'form-select'}),
            'taille': forms.TextInput(attrs={'placeholder': 'Ex: M, L ou 10 ans'}),
            'couleur': forms.TextInput(attrs={'placeholder': 'Ex: Bleu Marine'}),
            'quantite': forms.NumberInput(attrs={'min': 0}),
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

