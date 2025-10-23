from django.db import models

# ATRIBUTOS DEL MODELO

class cliente(models.Model):
  nombre=models.CharField(max_length=20)
  apellido=models.CharField(max_length=20)
  num_documento=models.IntegerField()
  telefono=models.IntegerField(max_length=10)
  correo=models.CharField(max_length=30)
  
  
# Representación del objeto
  def __str__(self):
        return f"{self.nombre} {self.apellido}"

    # ---- MÉTODOS GET ----
  def get_nombre(self):
        return self.nombre

  def get_apellido(self):
        return self.apellido

  def get_num_documento(self):
        return self.num_documento

  def get_telefono(self):
        return self.telefono

  def get_correo(self):
        return self.correo

    # ---- MÉTODOS SET ----
  def set_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre
        self.save()

  def set_apellido(self, nuevo_apellido):
        self.apellido = nuevo_apellido
        self.save()

  def set_num_documento(self, nuevo_num_documento):
        self.num_documento = nuevo_num_documento
        self.save()

  def set_telefono(self, nuevo_telefono):
        self.telefono = nuevo_telefono
        self.save()

  def set_correo(self, nuevo_correo):
        self.correo = nuevo_correo
        self.save()






