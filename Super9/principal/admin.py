from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Producto, Categoria

# Registrar el modelo de Usuario personalizado
admin.site.register(Usuario, UserAdmin)

# Registrar el modelo de Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Registrar el modelo de Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria',) # Permite filtrar por la nueva tabla Categoría
    search_fields = ('nombre',)