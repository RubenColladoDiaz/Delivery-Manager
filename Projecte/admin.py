from django.contrib import admin

from Projecte.models import Client, Albara, LineaAlbara, Producte, Categoria, Empleat, Magatzem, StockMagatzem

# Register your models here.
admin.site.register(Client)
admin.site.register(Albara)
admin.site.register(LineaAlbara)
admin.site.register(Producte)
admin.site.register(Categoria)
admin.site.register(Empleat)
admin.site.register(Magatzem)
admin.site.register(StockMagatzem)