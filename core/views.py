#IMPORTACIONE CON COMENTARIOS
from django.shortcuts import render, redirect
#render:Renderiza un template HTML y lo devuelve como respuesta al navegador.
#Se usa para mostrar una página, como login.html, perfil.html, registrarse.html, etc.
#redirect: Redirige al usuario a otra URL o vista, sin mostrar un template.
#Se usa Después de un login exitoso, un registro, un logout, o cualquier acción que no necesita mostrar una página intermedia.

from django.contrib.auth import authenticate, login # para manejar el inicio de sesión
#authenticate(request, username, password):Verifica si el usuario existe y si la contraseña es correcta.
#login(request, user): Si el usuario fue autenticado, lo registra en la sesión activa.

from django.contrib.auth.forms import UserCreationForm
#clase de formulario que Django da lista para usar en el registro de usuarios. 
# Ya incluye validación de contraseñas, verificación de campos, etc.

from django.contrib.auth.decorators import user_passes_test, login_required
#decoradores que se usan para proteger vistas:
#@login_required: Solo permite acceder a la vista si el usuario está logueado.
#@user_passes_test(lambda u: u.is_superuser):Solo permite acceso si el usuario cumple una condición (como ser admin).


# CREACIÓN DE VISTAS
def index(request):
    return render(request, 'core/index.html')
# Se define el index para que sea la página principal, este será nuestra página de inicio de la pagina web aquí, en views.py
#El segundo paso será crear la url en url.py tanto de core como de Eltotem, y se crean las rutas
#Tercer paso es agregar 'core' en settings.py de Eltotem en la parte de INSTALLED_APPS

# Ahora procedemos a hacer la view de registro:
def registrarse_view(request):
    return render(request, 'core/registrarse.html')
#Luego, procedemos a agregarlo al pattern en urls.py de la aplicación, en este caso, core

#REPETIR para todas las templates, por ejemplo, login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # o donde quieras redirigir
        else:
            return render(request, 'core/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'core/login.html')
