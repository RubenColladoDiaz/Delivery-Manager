from django.db import models
from django.db.models import ForeignKey


# Create your models here.
class Client(models.Model):
    codi_client = models.CharField(max_length=200, unique=True) # SIEMPRE DECLARAR MAX LENGTH EN CHAR
    nom_comercial = models.CharField(max_length=200)
    cif = models.CharField(max_length=200)
    persona_contacte = models.CharField(max_length=200)
    telefon = models.IntegerField()
    email = models.EmailField()
    adreca_entrega = models.CharField(max_length=200)
    poblacio = models.CharField(max_length=200)
    codi_postal = models.IntegerField()
    actiu = models.BooleanField(default=True)
    def __str__(self):
        return self.nom_comercial

class Albara(models.Model):
    ESTAT = [
        ('PENDENT', 'PENDENT'),
        ('EN_PREPARACIO', 'EN_PREPARACIO'),
        ('ENVIAT', 'ENVIAT'),
        ('ENTREGAT', 'ENTREGAT'),
        ('CANCELAT', 'CANCELAT')
    ]

    numero_albara = models.CharField(max_length=200, unique=True)
    client = ForeignKey('Client', on_delete=models.CASCADE, related_name='albarans') # FK SIEMPRE VA EN LA N EN 1..N
    data_creacio = models.DateTimeField(auto_now_add=True)
    data_entrega_prevista = models.DateTimeField()
    estat = models.CharField(max_length=200, choices=ESTAT)
    total = models.DecimalField(max_digits=5, decimal_places=2) # OJO DECIMALES SIEMPRE PIDE ESTOS ATRIBUTOS
    observacions = models.TextField(blank=True, null=False) # Se guarda como ''. Si ambos fueran True se guardaria como NULL

class LineaAlbara(models.Model):
    albara = ForeignKey('Albara', on_delete=models.CASCADE, related_name='linies_albara')
    nom_producte = models.CharField(max_length=200)
    quantitat = models.IntegerField()
    preu_unitari = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.CharField(blank=True, null=False)