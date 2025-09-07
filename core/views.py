from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'core/index.html')
# Se define el index para que sea la página principal, este será nuestra página de inicio de la pagina web aquí, en views.py
#El segundo paso será crear la url en url.py tanto de core como de Eltotem, y se crean las rutas
#Tercer paso es agregar 'core' en settings.py de Eltotem en la parte de INSTALLED_APPS

# Ahora procedemos a hacer la view de registro:
def registrarse_view(request):
    return render(request, 'core/registrarse.html')
#Luego, procedemos a agregarlo al pattern en urls.py de la aplicación, en este caso, core