from django.db import models

# Create your models here.

# Modelo de sección NOTICIAS
class NoticiaTCG(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    fecha = models.DateField()
    juego = models.CharField(max_length=50, choices=[
        ('pokemon', 'Pokémon TCG'),
        ('yugioh', 'Yu-Gi-Oh!'),
        ('mitos', 'Mitos y Leyendas'),
        ('otros', 'Otros')
    ])
    tipo_evento = models.CharField(max_length=50, choices=[
        ('torneo', 'Torneo'),
        ('lanzamiento', 'Lanzamiento'),
        ('actualizacion', 'Actualización'),
        ('comunidad', 'Comunidad')
    ])
    fuente = models.URLField()
    imagen = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.juego})"

