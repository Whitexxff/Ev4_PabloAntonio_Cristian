from django.contrib import admin
from django.urls import path, include
# Importamos todas las vistas de la app 'principal'
from principal import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='user_login'), 
    path('base/', views.base, name='base'),
    path('logout/', views.user_logout, name='user_logout'),
    path('registro/', views.registro, name='registro'),
    path('contacto/', views.contacto, name='contacto'),
    path('trabajanosotros/', views.trabajanosotros, name='trabajanosotros'),
    path('quienessomos/', views.quienessomos, name='quienessomos'),
    path('nuestroslocales/', views.nuestroslocales, name='nuestroslocales'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/categoria/<int:categoria_id>/', views.lista_productos, name='lista_productos_por_categoria'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('productos/exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
]