from django.contrib import admin
from .models import NoticiaTCG

@admin.register(NoticiaTCG)
class NoticiaTCGAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'juego', 'tipo_evento', 'fecha')
    search_fields = ('titulo', 'resumen')
    list_filter = ('juego', 'tipo_evento', 'fecha')
