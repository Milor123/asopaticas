from __future__ import unicode_literals
#!/usr/bin/python 2.7
# -*- encoding: utf-8 -*-
from django.contrib import admin
from animalitos.models import Animal, Adoptante, Adoptar
from django.db import models#test
from django.utils.safestring import mark_safe
from datetime import datetime, date, time, timedelta



#@admin.register(Animal)
#class Animal(admin.ModelAdmin):
#    pass

#StackedInline ?? TabularInline
class AdoptarInLine(admin.StackedInline):

    model = Adoptar
    #fields=('fecha',)
    #readonly_fields = ('fecha',)
    #raw_id_fields = ("Animal_idAnimal","Adoptante_idAdoptante")
    extra = 0
    #ordering = ('-fecha',)
    fk_name = ('Animal_idAnimal')


    #fix bug auto add extra
    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra

#@admin.register(Adoptar)
#class Adoptar(admin.ModelAdmin):
    #pass
    #list_display = ('fecha','voluntario')




@admin.register(Animal)
class AnimalInline(admin.ModelAdmin):

    list_display = ('nombre','tipo_de_animal','estado_de_salud', 'numero_telefono','sexo','edad', 'color','adoptantes','fecha_de_adopcion', 'esterilizado','edad_desde_adopcion')
    search_fields = ('nombre', 'adoptar__Adoptante_idAdoptante__idAdoptante','adoptar__Adoptante_idAdoptante__telefono')
    readonly_fields = ('image_tag',)
    inlines = [AdoptarInLine,]


    def adoptantes(self,Animal):
        adoptante = Adoptar.objects.filter(Animal_idAnimal = Animal.idAnimal).order_by('-fecha').first()
        try:
            return mark_safe("<a href='/animalitos/adoptante/%s'>%s</a> " %(adoptante.Adoptante_idAdoptante.idAdoptante,adoptante.Adoptante_idAdoptante))
        except:
            return 0

    def numero_telefono(self,Animal):
        adoptante = Adoptar.objects.filter(Animal_idAnimal = Animal.idAnimal).order_by('-fecha').first()
        try:
            return  adoptante.Adoptante_idAdoptante.telefono
        except:
            return 0

    def esterilizado(self, Animal):
        if Animal.es_esterilizado=='Si':
            return mark_safe( "<font color='green'><b>%s</b></font>" %Animal.es_esterilizado)
        elif Animal.es_esterilizado=='No':
            return mark_safe( "<font color='red'><b>%s</b></font>" %Animal.es_esterilizado)

    def estado_de_salud(self, Animal):
        if Animal.salud == 'Excelente':
            return mark_safe( "<font color='green'><b>%s</b></font>" %Animal.salud)
        elif Animal.salud == 'Bueno':
            return mark_safe( "<font color='blue'><b>%s</b></font>" %Animal.salud)
        elif Animal.salud == 'Regular':
            return mark_safe( "<font color=#F29C2A><b>%s</b></font>" %Animal.salud)
        elif Animal.salud == 'Pesimo':
            return mark_safe( "<font color='red'><b>%s</b></font>" %Animal.salud)
        else:
            return ''

    def edad_desde_adopcion(self,Animal):
        try:
            adoptante = Adoptar.objects.filter(Animal_idAnimal = Animal.idAnimal).order_by('-fecha').first()
            tiempo = date.today() - adoptante.fecha
            days=int(tiempo.days)
            mes=0
            while days>30:
                days-=30
                mes+=1
            if (days < int(0) or mes < int(0) ):
                return mark_safe('<font color="red"><b>Meses=%s Dias=%s</b></font>' %(mes,days))
            else:
                return ('Meses=%s Dias=%s'%(mes,days))
        except:
            return 0

    def fecha_de_adopcion(self,Animal):
        #import pdb
        #pdb.set_trace() # dir(string)
        try:
            adoptante = Adoptar.objects.filter(Animal_idAnimal = Animal.idAnimal).order_by('-fecha').first()
            return adoptante.fecha
        except:
            return 0
    esterilizado.admin_order_field='es_esterilizado'
    estado_de_salud.admin_order_field='salud'
    fecha_de_adopcion.admin_order_field='adoptar__fecha'
    adoptantes.admin_order_field = 'adoptar__Adoptante_idAdoptante'
    numero_telefono.admin_order_field= 'adoptar__Adoptante_idAdoptante__telefono'
    edad_desde_adopcion.admin_order_field='adoptar__fecha'

@admin.register(Adoptante)
class Adoptante(admin.ModelAdmin):
    list_display = ('nombre','apellido','telefono','direccion','cedula','departamento','cuidad','email','informacion','foto')
    search_fields = ('nombre','apellido','informacion','direccion','email')

    def foto(self,Adoptante):
        #import pdb
        #pdb.set_trace() # dir(string)
        try:
            adoptante = Adoptar.objects.filter(Adoptante_idAdoptante = Adoptante.idAdoptante).order_by('-fecha').first()
            if not bool(adoptante.Animal_idAnimal.foto):
                return mark_safe('<img src="/images/pic_folder/404animal.jpg" height="50" width="50">')
            else:
                return mark_safe('<a href="/images/%s"><img src="/images/%s" height="50" width="50"> ' %(adoptante.Animal_idAnimal.foto,adoptante.Animal_idAnimal.foto))
        except:
            return 0
    foto.admin_order_field='animal__foto'