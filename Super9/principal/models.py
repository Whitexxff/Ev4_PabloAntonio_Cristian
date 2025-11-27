from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('cajero', 'Cajero'),
        ('empleado', 'Empleado'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado', verbose_name='Rol')

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre Producto')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoría', related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name='Imagen')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"