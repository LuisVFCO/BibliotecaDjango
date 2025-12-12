from django.db import models

class Conta(models.Model):
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    
class Livro(models.Model):
    id_livro = models.PositiveIntegerField(unique=True) 
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    data_lanc = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_livro} - {self.titulo}"

class Estoque(models.Model):
    livro = models.OneToOneField(Livro, on_delete=models.CASCADE, related_name='estoque')
    quantidade = models.IntegerField(default=0)

    def adicionar(self, qtd):
        self.quantidade += qtd
        self.save()

    def remover(self, qtd):
        if qtd <= self.quantidade:
            self.quantidade -= qtd
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.livro.titulo}: {self.quantidade}"

# Create your models here.
