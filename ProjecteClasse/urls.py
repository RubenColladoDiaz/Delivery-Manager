from django.contrib import admin
from django.urls import path

from Projecte import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LlistatClients.as_view(), name='home'),
    path('clients/', views.LlistatClients.as_view(), name='llistatClients'),
    path('clients/<int:id>/', views.DetallsClient.as_view(), name='detallsClient'),
    path('clients/<int:id>/editar/', views.EditarClient.as_view(), name='editarClient'),
    path('albarans/', views.LlistatAlbarans.as_view(), name='llistatAlbarans'),
    path('albarans/<int:id>/', views.DetallsAlbara.as_view(), name='detallsAlbara'),
    path('albarans/nova/', views.CrearAlbara.as_view(), name='crearAlbara'),
    path('albarans/<int:id>/afegir-linia/', views.AfegirLinia.as_view(), name='afegirLinia'),
    path('albarans/<int:id>/estat/<str:nouEstat>/', views.CanviarEstat.as_view(),name='canviarEstat'),
    path('albara/<int:id>/estat/', views.CanviarEstatFormulari.as_view(), name='canviarEstatFormulari'),
    path('consulta/', views.Consulta.as_view(), name='consulta'),
    path('consulta/<int:numero_albara>', views.ResultatConsulta.as_view(), name='resultatConsulta'),
    path('estadistiques/', views.Estadistiques.as_view(), name='estadistiques'),
    path('cataleg/', views.Cataleg.as_view(), name='cataleg'),
    path('cataleg/<str:categoria>/', views.CatalegFiltrat.as_view(), name='cataleg_filtrat'),
    path('preparacio/', views.Preparacio.as_view(), name='preparacio'),
    path('preparacio/<int:id>/', views.Preparacio.as_view(), name='preparacioPOST'),
    path('stock/', views.Stock.as_view(), name='stock'),
    path('stock/reposicio/', views.StockReposicio.as_view(), name='stockReposicio'),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.Register.as_view(), name="register"),
]