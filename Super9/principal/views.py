from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Producto, Categoria
from .forms import ProductoForm, RegistroUsuarioForm, CategoriaForm

# Obtener el modelo de usuario personalizado
Usuario = get_user_model()


# --- Vistas de Autenticación y Principales ---

def user_login(request):
    # Si el usuario ya está autenticado, redirigirlo para que no vea la página de login
    if request.user.is_authenticated:
        return redirect('base') 

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('contrasena_usuario', '').strip() 

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido, {username}!")
            
            # Redireccionar a la página 'next' si existe, si no, a 'base'
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('base') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('user_login')

# Vista de Registro (Ajustada para usar el formulario)
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: Loguear al usuario automáticamente después del registro
            auth_login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('base')
        else:
            # Si el formulario no es válido, se mostrará con los errores
            messages.error(request, 'Error en el formulario de registro. Revise los datos.')
    else:
        # Método GET: Mostrar formulario vacío
        form = RegistroUsuarioForm()
        
    return render(request, 'registro.html', {'form': form})

@login_required
def base(request):
    return render(request, 'base.html')

@login_required
def contacto(request):
    return render(request, 'contacto.html')

@login_required
def trabajanosotros(request):
    return render(request, 'trabajanosotros.html')

@login_required
def quienessomos(request):
    # Tu plantilla se llama 'nosotros.html'
    return render(request, 'nosotros.html')

@login_required
def nuestroslocales(request):
    return render(request, 'sucursales.html')


# --- Vistas de Productos (Flujo Clásico) ---

def lista_productos(request, categoria_id=None):
    """
    Lista productos, permitiendo filtrar por categoría.
    """
    # 1. Obtener todas las categorías para mostrar en el sidebar
    categorias = Categoria.objects.all()
    
    # 2. Lógica de filtrado
    if categoria_id:
        # Si hay un ID en la URL, buscamos la categoría y filtramos
        categoria_seleccionada = get_object_or_404(Categoria, id=categoria_id)
        productos = Producto.objects.filter(categoria=categoria_seleccionada)
    else:
        # Si no hay ID, mostramos todo
        categoria_seleccionada = None
        productos = Producto.objects.all()

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada, # Para resaltar la opción activa en el HTML
        'is_admin': hasattr(request.user, 'rol') and request.user.rol == 'admin',
    }
    return render(request, 'lista_productos.html', context)

@login_required
def crear_producto(request):
    """
    Maneja la creación de un producto usando una plantilla dedicada. (CREATE)
    """
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para crear productos.')
        return redirect('lista_productos')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error de validación. Revise los datos en el formulario.')
    else:
        form = ProductoForm()
            
    # Renderiza la plantilla de formulario dedicada
    return render(request, 'producto_form.html', {'form': form, 'titulo': 'Crear Producto'})


@login_required
def editar_producto(request, id):
    """
    Maneja la edición de un producto usando una plantilla dedicada. (UPDATE)
    """
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para editar productos.')
        return redirect('lista_productos')

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error de validación. Revise los datos en el formulario.')
    else:
        form = ProductoForm(instance=producto)
            
    # Renderiza la plantilla de formulario dedicada
    return render(request, 'producto_form.html', {'form': form, 'titulo': f'Editar Producto: {producto.nombre}'})


@login_required
def eliminar_producto(request, id):
    """
    Procesa la eliminación de un producto (POST). (DELETE)
    """
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para eliminar productos.')
        return redirect('lista_productos')

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
    else:
        messages.error(request, 'Acceso no permitido para la eliminación.')
        
    return redirect('lista_productos')

@login_required
def lista_categorias(request):
    """READ: Lista todas las categorías."""
    # Validación de rol (Solo Admin)
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        messages.error(request, 'Acceso denegado a gestión de categorías.')
        return redirect('lista_productos')

    categorias = Categoria.objects.all()
    # Usa el template lista_categorias.html que creamos antes
    return render(request, 'lista_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    """CREATE: Crea una nueva categoría."""
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        return redirect('lista_productos')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Error al crear la categoría.')
    else:
        form = CategoriaForm()

    # Usa el template categoria_form.html que creamos antes
    return render(request, 'categoria_form.html', {'form': form, 'titulo': 'Crear Categoría'})

@login_required
def editar_categoria(request, id):
    """UPDATE: Edita una categoría existente."""
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        return redirect('lista_productos')

    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada.')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Error al actualizar.')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categoria_form.html', {'form': form, 'titulo': f'Editar: {categoria.nombre}'})

@login_required
def eliminar_categoria(request, id):
    """DELETE: Elimina una categoría (protegido si tiene productos)."""
    if not hasattr(request.user, 'rol') or request.user.rol != 'admin':
        return redirect('lista_productos')

    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoría eliminada.')
        except Exception:
            # Captura el error de integridad si hay productos vinculados
            messages.error(request, 'No se puede eliminar: tiene productos asociados.')

    return redirect('lista_categorias')




@login_required
def exportar_pdf(request):
    """Genera un reporte PDF simple de los productos (Valor Agregado)"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="catalogo_productos.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Catálogo de Productos - Super9")
    
    p.setFont("Helvetica", 12)
    y = 720
    
    productos = Producto.objects.all()
    
    for producto in productos:
        p.drawString(100, y, f"- {producto.nombre} | Stock: {producto.stock} | Precio: ${producto.precio}")
        y -= 20
        if y < 50: # Nueva página si se acaba el espacio
            p.showPage()
            y = 750
            
    p.save()
    return response