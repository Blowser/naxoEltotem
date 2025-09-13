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

from django.views.generic import ListView
#Una de las tantas vistas preconstruidas de django, está basada en clase y sirve para mostrar lista de objetos de un modelo
#Seleccionamos cual modelo mostrar, qué plantilla usar, y cómo filtrar los datos.
from .models import NoticiaTCG
#importamos nuestro modelo personalizado para las noticias, así podemos consultar, fitlrar y mostrar
#“Traéme las runas que definimos para las noticias, que vamos a mostrarlas al clan”.


# CREACIÓN DE VISTAS
def index(request):
    return render(request, 'core/index.html')
# Se define el index para que sea la página principal, este será nuestra página de inicio de la pagina web aquí, en views.py
#El segundo paso será crear la url en url.py tanto de core como de Eltotem, y se crean las rutas
#Tercer paso es agregar 'core' en settings.py de Eltotem en la parte de INSTALLED_APPS

# Ahora procedemos a hacer la view de registro:
def registrarse_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST['username']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        direccion = request.POST['direccion']
        
        # Validar que las contraseñas coincidan
        if password1 != password2:
            return render(request, 'core/registrarse.html', {
                'error': 'Las contraseñas no coinciden'
            })
        
        # Crear el usuario usando UserCreationForm
        form = UserCreationForm({
            'username': username,
            'password1': password1,
            'password2': password2,
        })
        
        if form.is_valid():
            user = form.save()
            # Autenticar y hacer login automáticamente después del registro
            login(request, user)
            return redirect('index')  # Redirigir al index después del registro exitoso
        else:
            # Si hay errores en el formulario, mostrarlos
            return render(request, 'core/registrarse.html', {
                'error': 'Error en el formulario: ' + str(form.errors)
            })
    
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


#AHORA SE IMPORTA EL VIEWLIST DE LAS NOTICIAS, LUEGO SE CREA LA CLASE PARA FILTRAR
class NoticiasFiltradasView(ListView):
    model = NoticiaTCG
    template_name = 'core/noticias.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        qs = super().get_queryset()
        juego = self.request.GET.get('juego')
        tipo = self.request.GET.get('tipo_evento')
        fecha = self.request.GET.get('fecha')

        if juego:
            qs = qs.filter(juego=juego)
        if tipo:
            qs = qs.filter(tipo_evento=tipo)
        if fecha:
            qs = qs.filter(fecha__gte=fecha)

        return qs.order_by('-fecha')
