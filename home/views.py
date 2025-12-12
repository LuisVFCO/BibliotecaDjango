from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conta, Livro, Estoque

def home(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Instanciando e salvando
        user = Conta(email=email, senha=senha)
        user.save()

        return redirect('login')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = Conta.objects.filter(email=email, senha=senha).first()

        if user:
            return redirect('estoque_home')
        else:
            return HttpResponse('Usuário ou senha incorretas!!! Volte e tente novamente')

def redirecionar_para_cadastro(request):
    return redirect('cadastro')


def estoque_home(request):
    livros = Livro.objects.all().order_by('id_livro')
    alertas = Estoque.objects.filter(quantidade__lt=5).select_related('livro')
    context = {
        'livros': livros,
        'alertas': alertas,
    }
    return render(request, 'estoque_home.html', context)

def cadastrar_livro(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_livro.html')

    id_livro = request.POST.get('id_livro')
    titulo = request.POST.get('titulo')
    autor = request.POST.get('autor')
    data_lanc = request.POST.get('data_lanc')
    qtd_ini = int(request.POST.get('qtd_ini') or 0)

    if Livro.objects.filter(id_livro=id_livro).exists():
        return HttpResponse("Já existe um livro com esse id_livro. Use outro ID.")

    livro = Livro.objects.create(id_livro=id_livro, titulo=titulo, autor=autor, data_lanc=data_lanc)
    Estoque.objects.create(livro=livro, quantidade=qtd_ini)
    return redirect('estoque_home')

def movimentar_estoque(request):
    if request.method == 'GET':
        livros = Livro.objects.all().order_by('id_livro')
        return render(request, 'movimentar_estoque.html', {'livros': livros})

    id_livro = request.POST.get('id_livro')
    tipo = request.POST.get('tipo')
    qtd = int(request.POST.get('qtd') or 0)

    livro = Livro.objects.filter(id_livro=id_livro).first()
    if not livro:
        return HttpResponse("Livro não encontrado.")

    estoque = getattr(livro, 'estoque', None)
    if not estoque:
        estoque = Estoque.objects.create(livro=livro, quantidade=0)

    if tipo == 'entrada':
        estoque.adicionar(qtd)
        return redirect('estoque_home')

    elif tipo == 'saida':
        sucesso = estoque.remover(qtd)
        if not sucesso:
            return HttpResponse("Operação inválida: quantidade insuficiente.")
        return redirect('estoque_home')

    else:
        return HttpResponse("Operação inválida.")