from decimal import Decimal

from django.utils import timezone
from django.db.models import Sum

from django.shortcuts import render, redirect
from django.views import View
import plotly.graph_objects as go

from Projecte.models import Client, Albara, LineaAlbara, Producte, Categoria, StockMagatzem, Empleat, Magatzem

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class LlistatClients(View):
    def get(self, request, *args, **kwargs):
        clientsActius = Client.objects.filter(actiu=True)
        return render(request, 'clients/mostrarClients.html', {'clientsActius': clientsActius})

class DetallsClient(View):
    def get(self, request, *args, **kwargs):
        idURL = self.kwargs['id'] # PILLAMOS EL ID DE LA URL
        client = Client.objects.get(pk=idURL)
        # client = get_object_or_404(Client, pk=idURL) OTRA MANERA QUE LE GUSTA AL MARC
        return render(request, 'clients/detallsClient.html', {'client': client})

class EditarClient(View):
    def get(self, request, *args, **kwargs):
        idURL = self.kwargs['id']
        client = Client.objects.get(pk=idURL)
        return render(request, 'clients/editarClient.html', {'client': client})

    def post(self, request, *args, **kwargs):
        idURL = self.kwargs['id']
        client = Client.objects.get(pk=idURL)

        client.codi_client = request.POST['codi_client']
        client.nom_comercial = request.POST['nom_comercial']
        client.cif = request.POST['cif']
        client.persona_contacte = request.POST['persona_contacte']
        client.telefon = request.POST['telefon']
        client.email = request.POST['email']
        client.adreca_entrega = request.POST['adreca_entrega']
        client.poblacio = request.POST['poblacio']
        client.codi_postal = request.POST['codi_postal']
        client.actiu = 'actiu' in request.POST  # checkbox

        client.save()
        return redirect('llistatClients')
    
class Cataleg(View):
    def get(self, request, *args, **kwargs):
        categories = Categoria.objects.all()
        return render(request, 'productes/cataleg.html', {'categories': categories})

class CatalegFiltrat(View):
    def get(self, request, *args, **kwargs):
        categoriaURL = self.kwargs['categoria']
        categoria = Categoria.objects.get(nom=categoriaURL)
        return render(request, 'productes/catalegFiltrat.html', {'categoria': categoria})

class LlistatAlbarans(View):
    def get(self, request, *args, **kwargs):
        albarans = Albara.objects.all()
        return render(request, 'albarans/mostrarAlbarans.html', {'albarans': albarans})

class DetallsAlbara(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            idURL = self.kwargs['id']
            albara = Albara.objects.get(pk=idURL)

            totalSubtotals = 0
            for liniaAlbara in albara.linies_albara.all():
                totalSubtotals += liniaAlbara.subtotal

            afegirLinea = albara.estat == 'PENDENT'
            return render(request, 'albarans/detallsAlbara.html', {'albara': albara, 'totalSubtotals': totalSubtotals, 'afegirLinea': afegirLinea})

class CrearAlbara(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            clients = Client.objects.all()
            return render(request, 'albarans/crearAlbara.html', {'clients': clients})

    def post(self, request, *args, **kwargs):
        numero_albara = request.POST['numero_albara']
        data_entrega_prevista = request.POST['data_entrega_prevista']
        observacions = request.POST['observacions']
        client_id = request.POST['client']
        total_iva = request.POST['total_iva']

        client = Client.objects.get(id=client_id)

        nouAlbara = Albara(
            numero_albara=numero_albara,
            client=client,
            data_creacio=timezone.now(),
            data_entrega_prevista=data_entrega_prevista,
            estat='PENDENT',
            total=0,
            total_iva=total_iva,
            observacions=observacions
        )
        nouAlbara.save()
        return redirect('detallsAlbara', id=nouAlbara.id)

class AfegirLinia(View):
    def get(self, request, *args, **kwargs):
        idURL = self.kwargs['id']
        albara = Albara.objects.get(id=idURL)
        productes = Producte.objects.all()
        return render(request, 'albarans/afegirLinia.html', {'albara': albara, 'productes': productes})

    def post(self, request, *args, **kwargs):
        idURL = self.kwargs['id']
        albara = Albara.objects.get(id=idURL)

        producte_id = request.POST['producteSeleccionat']
        producte = Producte.objects.get(id=producte_id)

        quantitat = int(request.POST['quantitat'])
        preu_unitari = Decimal(request.POST['preu_unitari'])
        descompte = int(request.POST['descompte'])
        notes = request.POST['notes']

        subtotal = quantitat * preu_unitari

        stock = StockMagatzem.objects.get(producte=producte, magatzem=albara.magatzem)

        if stock and stock.quantitat >= quantitat:
            novaLinia = LineaAlbara(
                albara=albara,
                producte=producte,
                quantitat=quantitat,
                preu_unitari=preu_unitari,
                descompte_percentatge = descompte,
                subtotal=subtotal,
                notes=notes
            )
            novaLinia.save()

            albara.total += subtotal
            albara.save()
        else:
            messages.error(request, 'No hi ha prou stock')

        return redirect('detallsAlbara', id=albara.id)

class Estadistiques(View):
    def get(self, request, *args, **kwargs):
        albarans = Albara.objects.filter(estat='ENTREGAT').order_by('-data_creacio')

        productes_mes_venuts = (
            LineaAlbara.objects
            .filter(albara__estat='ENTREGAT')
            .values('producte__nom')
            .annotate(quantitat_total=Sum('quantitat'))
            .order_by('-quantitat_total')
        )

        vendes_per_categoria = (
            LineaAlbara.objects
            .filter(albara__estat='ENTREGAT')
            .values('producte__categoria__nom')
            .annotate(total_vendes=Sum('subtotal'))
            .order_by('producte__categoria__nom')
        )

        categories_labels = [item['producte__categoria__nom'] for item in vendes_per_categoria]
        categories_totals = [float(item['total_vendes'] or 0) for item in vendes_per_categoria]

        colors = ['#00FFFF', '#248241', '#FF69B4', '#FFA500', '#4169E1']
        fig = go.Figure(data=[
            go.Bar(
                x=categories_labels,
                y=categories_totals,
                marker_color=[colors[i % len(colors)] for i in range(len(categories_labels))]
            )
        ])

        fig.update_layout(
            title='Vendes per categoria',
            xaxis_tickangle=-45,
            yaxis_tickangle=-45,
            font=dict(
                family='Courier New, monospace',
            ),
            height=600,
            width=800,
            autosize=True,
            xaxis_title_text='Categoria',
            yaxis_title_text='Vendes',
        )

        grafic_html = fig.to_html(div_id='vendesCategoriaChart', full_html=False)

        ranking_clients = (
            Albara.objects
            .filter(estat='ENTREGAT')
            .values('client__nom_comercial')
            .annotate(volum_compra=Sum('total'))
            .order_by('-volum_compra')
        )

        return render(
            request,
            'consulta/estadistiques.html',
            {
                'albarans': albarans,
                'productesMesVenuts': productes_mes_venuts,
                'grafic': grafic_html,
                'rankingClients': ranking_clients,
            }
        )

class CanviarEstat(View):
    def get(self, request, *args, **kwargs):
        idURL = self.kwargs['id']
        albara = Albara.objects.get(id=idURL)

        nouEstat = self.kwargs['nouEstat']
        albara.estat = nouEstat
        albara.save()
        return redirect('detallsAlbara', id=albara.id)
    
class CanviarEstatFormulari(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            idAlbara = self.kwargs['id']
            albara = Albara.objects.get(id=idAlbara)
            estats = Albara.ESTAT
            return render(request, 'albarans/canviarEstat.html', {'albara': albara, 'estats': estats})
        
    def post(self, request, *args, **kwargs):
        idAlbara = self.kwargs['id']
        albara = Albara.objects.get(id=idAlbara)

        nouEstat = request.POST['estatSeleccionat']
        if not (albara.estat == 'ENVIAT' and nouEstat == 'PENDENT'):
            albara.estat = nouEstat
            albara.save()
            return redirect('detallsAlbara', id=albara.id)
        else:
            return redirect('llistatAlbarans')

class Consulta(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'consulta/consulta.html')

    def post(self, request, *args, **kwargs):
        numero_albara = request.POST['numero_albara']
        return redirect('resultatConsulta', numero_albara=numero_albara)

class ResultatConsulta(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            numero_albaraURL = self.kwargs['numero_albara']

            albara = Albara.objects.filter(numero_albara=numero_albaraURL).first()
            if albara:
                noTrobat = ""
                liniesAlbara = albara.linies_albara.all()
            else:
                noTrobat = "Albarà no trobada"
                liniesAlbara = []
            return render(request, 'consulta/resultatConsulta.html', {'albara': albara, 'liniesAlbara': liniesAlbara, 'noTrobat': noTrobat})

class Preparacio(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.empleat is not None:
            empleat = request.user.empleat
            albarans = empleat.magatzem_assignat.albarans.all()
            albarans_filtrats = albarans.filter(estat__in=['PENDENT', 'EN_PREPARACIO'])
            return render(request, 'preparacio/preparacio.html', {'albarans': albarans_filtrats,'empleat': empleat})

    def post(self, request, *args, **kwargs):
        idAlbara = self.kwargs['id']
        albara = Albara.objects.get(id=idAlbara)
        empleat = request.user.empleat

        for linia_albara in albara.linies_albara.all():
            stock = albara.magatzem.stocks_magatzem.get(producte=linia_albara.producte)
            if not stock or stock.quantitat < linia_albara.quantitat:
                return redirect('preparacio')

        if albara.magatzem == empleat.magatzem_assignat:
            stock = StockMagatzem.objects.get(magatzem=empleat.magatzem_assignat)
            if stock.quantitat <= 0:
                messages.error(request, 'Stock insuficient')
                return redirect('albarans')
            stock.quantitat = stock.quantitat - 1
            albara.estat = 'ENVIAT'
            albara.save()

        return redirect('preparacio')

class Stock(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.empleat is not None:
            magatzems = Magatzem.objects.all()
            productes = Producte.objects.all()
            return render(request, 'stock/stock.html', {'magatzems': magatzems, 'productes': productes})

class StockReposicio(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.empleat is not None:
            productes = Producte.objects.all()
            magatzems = Magatzem.objects.all()
            return render(request, 'stock/reposicio.html', {'magatzems': magatzems, 'productes': productes})

    def post(self, request, *args, **kwargs):
        magatzem = request.POST['magatzemSeleccionat']
        quantitat = int(request.POST['quantitat'])
        # get UNO. filter MUCHOS aunque sea VACIO
        stock = StockMagatzem.objects.get(magatzem=magatzem)
        stock.quantitat += quantitat
        stock.save()
        return redirect('stock')


class Register(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente")
            return redirect("login")

        return render(request, "auth/register.html", {"form": form})