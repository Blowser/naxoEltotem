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

#IMPORTES PARA SCRAPPING:
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from core.models import NoticiaTCG
from django.http import HttpResponse




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
# VISTAS PARA SCRAPPING:

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from .models import NoticiaTCG

def parse_fecha(texto):
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    partes = texto.split()
    dia = int(partes[0])
    mes = meses[partes[1].lower()]
    año = int(partes[2])
    return datetime(año, mes, dia).date()

def extraer_url_de_style(style):
    inicio = style.find("url(") + 4
    fin = style.find(")", inicio)
    url_relativa = style[inicio:fin].strip("'\"")
    return "https://www.yugioh-card.com" + url_relativa

def obtener_fecha_desde_articulo(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        fecha_tag = soup.find('p', class_='date')  # Ajustar si cambia
        if fecha_tag:
            return datetime.strptime(fecha_tag.text.strip(), "%B %d, %Y").date()
    except Exception as e:
        print("Error al obtener fecha:", e)
    return datetime.today().date()

def scrap_tcg(request):
    # 🔹 Yu-Gi-Oh!
    url_yugi = "https://www.yugioh-card.com/eu/es/noticias/"
    response_yugi = requests.get(url_yugi)
    soup_yugi = BeautifulSoup(response_yugi.text, 'html.parser')
    noticias_yugi = soup_yugi.find_all('article', class_='news-tile')
    print("Noticias Yu-Gi-Oh encontradas:", len(noticias_yugi))

    for item in noticias_yugi:
        titulo_tag = item.find('h2', class_='news-tile__heading')
        resumen_tag = item.find('p', class_='news-tile__excerpt')
        fecha_tag = item.find('p', class_='news-tile__date')
        imagen_style = item.find('div', class_='news-tile__image')['style']
        enlace_tag = item.find('a', class_='news-tile__link')

        titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
        resumen = resumen_tag.text.strip() if resumen_tag else "Sin resumen"
        fecha = parse_fecha(fecha_tag.text.strip()) if fecha_tag else datetime.today().date()
        fuente = "https://www.yugioh-card.com" + enlace_tag['href'] if enlace_tag else url_yugi
        imagen = extraer_url_de_style(imagen_style) if imagen_style else None

        obj, creado = NoticiaTCG.objects.get_or_create(
            fuente=fuente,
            defaults={
                'titulo': titulo,
                'resumen': resumen,
                'fecha': fecha,
                'juego': 'yugioh',
                'tipo_evento': "actualizacion",
                'imagen': imagen
            }
        )
        print("Yu-Gi-Oh:", "Guardada" if creado else "Ya existía", titulo)

    # 🔹 Pokeguardian (fuente alternativa Pokémon TCG)
    url_pg = "https://www.pokeguardian.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response_pg = requests.get(url_pg, headers=headers)
    soup_pg = BeautifulSoup(response_pg.text, 'html.parser')
    noticias_pg = soup_pg.find_all('article', class_='jw-news-post')
    print("Noticias Pokeguardian encontradas:", len(noticias_pg))

    for item in noticias_pg:
        titulo_tag = item.find('h2', class_='jw-news-post__title')
        resumen_tag = item.find('div', class_='jw-news-post__lead')
        fecha_tag = item.find('span', class_='jw-news-date')
        enlace_tag = item.find('a', class_='jw-news-color-heading')
        imagen_style = item.find('div', style=lambda s: s and 'background-image' in s)

        titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
        resumen = resumen_tag.text.strip() if resumen_tag else "Sin resumen"
        try:
            fecha = datetime.strptime(fecha_tag.text.strip(), "%d %b %Y").date() if fecha_tag else datetime.today().date()
        except:
            fecha = datetime.today().date()
        fuente = "https://www.pokeguardian.com" + enlace_tag['href'] if enlace_tag else url_pg
        imagen = None
        if imagen_style:
            style = imagen_style['style']
            inicio = style.find("url(") + 4
            fin = style.find(")", inicio)
            imagen = style[inicio:fin].strip("'\"")

        obj, creado = NoticiaTCG.objects.get_or_create(
            fuente=fuente,
            defaults={
                'titulo': titulo,
                'resumen': resumen,
                'fecha': fecha,
                'juego': 'pokemon',
                'tipo_evento': "actualizacion",
                'imagen': imagen
            }
        )
        print("Pokeguardian:", "Guardada" if creado else "Ya existía", titulo)
    # 🔹 Mitos y Leyendas
    url_myl = "https://casamyl.cl/blogs/myl"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response_myl = requests.get(url_myl, headers=headers)
    soup_myl = BeautifulSoup(response_myl.text, 'html.parser')
    noticias_myl = soup_myl.find_all('li', class_='grid__item')
    print("Noticias Mitos y Leyendas encontradas:", len(noticias_myl))

    for item in noticias_myl:
        enlace_tag = item.find('a', class_='article__link')
        titulo_tag = item.find('h2', class_='article__title')
        resumen_tag = item.find('div', class_='rte article__grid-excerpt')
        fecha_tag = item.find('time')
        imagen_tag = item.find('img')

        titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
        resumen = resumen_tag.text.strip() if resumen_tag else "Sin resumen"
        fecha = datetime.strptime(fecha_tag['datetime'][:10], "%Y-%m-%d").date() if fecha_tag else datetime.today().date()
        fuente = "https://casamyl.cl" + enlace_tag['href'] if enlace_tag else url_myl
        imagen = "https:" + imagen_tag['src'] if imagen_tag and 'src' in imagen_tag.attrs else None

        obj, creado = NoticiaTCG.objects.get_or_create(
            fuente=fuente,
            defaults={
                'titulo': titulo,
                'resumen': resumen,
                'fecha': fecha,
                'juego': 'Mitos y leyendas',
                'tipo_evento': "actualizacion",
                'imagen': imagen
            }
        )
        print("Mitos y Leyendas:", "Guardada" if creado else "Ya existía", titulo)

    return HttpResponse("Scraping combinado de TCG completado.")


    
