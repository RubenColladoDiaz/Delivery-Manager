from django.shortcuts import render, redirect
from django.views import View

from Projecte.models import Client, Albara


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

class LlistatAlbarans(View):
    def get(self, request, *args, **kwargs):
        albarans = Albara.objects.all()
        return render(request, 'albarans/mostrarAlbarans.html', {'albarans': albarans})