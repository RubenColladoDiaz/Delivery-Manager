from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User


# Create your models here.
class Categoria(models.Model):
    nom = models.CharField(max_length=200)
    descripcio = models.TextField(blank=True, null=False)
    requereix_refrigeracio = models.BooleanField(default=False)
    temperatura_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.nom

class Producte(models.Model):
    UNITAT_MESURA = [
        ('UNITAT', 'UNITAT'),
        ('CAIXA', 'CAIXA'),
        ('PALET', 'PALET'),
        ('KG', 'KG'),
        ('LITRE', 'LITRE')
    ]
    codi = models.CharField(max_length=200, unique=True)
    nom = models.CharField(max_length=200)
    descripcio = models.TextField(blank=True, null=False)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productes')
    preu_unitari = models.DecimalField(max_digits=5, decimal_places=2)
    unitat_mesura = models.CharField(max_length=200, choices=UNITAT_MESURA)
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    es_periple = models.BooleanField(default=False)
    imatge_url = models.URLField(max_length=200)
    actiu = models.BooleanField(default=True)
    def __str__(self):
        return self.nom

class Magatzem(models.Model):
    nom = models.CharField(max_length=200)
    adreca = models.CharField(max_length=200)
    capacitat_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    te_cambra_frio = models.BooleanField(default=False)
    responsable = models.CharField(max_length=200)
    def __str__(self):
        return self.nom
    
class StockMagatzem(models.Model):
    producte = ForeignKey('Producte', on_delete=models.CASCADE, related_name='stocks_magatzem')
    magatzem = ForeignKey('Magatzem', on_delete=models.CASCADE, related_name='stocks_magatzem')
    quantitat = models.IntegerField()
    data_ultima_entrada = models.DateTimeField()
    ubicacio = models.CharField(max_length=200)
    def __str__(self):
        return self.ubicacio

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

class Empleat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleat')
    codi_empleat = models.CharField(unique=True)
    telefon = models.IntegerField()
    data_alta = models.DateTimeField()
    magatzem_assignat = ForeignKey('Magatzem', on_delete=models.CASCADE, related_name='empleats', null=True)
    carrec = models.CharField(max_length=200)
    def __str__(self):
        return self.codi_empleat

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
    empleat = ForeignKey('Empleat', on_delete=models.CASCADE, related_name='albarans')
    magatzem = ForeignKey('Magatzem', on_delete=models.CASCADE, related_name='albarans')
    data_creacio = models.DateTimeField(auto_now_add=True)
    data_entrega_prevista = models.DateTimeField()
    estat = models.CharField(max_length=200, choices=ESTAT)
    base_imposable = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2) # OJO DECIMALES SIEMPRE PIDE ESTOS ATRIBUTOS
    observacions = models.TextField(blank=True, null=False) # Se guarda como ''. Si ambos fueran True se guardaria como NULL
    signatura_client = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.numero_albara

class LineaAlbara(models.Model):
    albara = ForeignKey('Albara', on_delete=models.CASCADE, related_name='linies_albara')
    producte = ForeignKey('Producte', on_delete=models.CASCADE, related_name='linies_albara')
    nom_producte = models.CharField(max_length=200)
    quantitat = models.IntegerField()
    preu_unitari = models.DecimalField(max_digits=5, decimal_places=2)
    descompte_percentatge = models.IntegerField()
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.CharField(blank=True, null=False)
    def __str__(self):
        return self.nom_producte