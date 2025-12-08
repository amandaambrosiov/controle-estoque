from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Movimentacao, Categoria, Fornecedor

# LISTAR PRODUTOS
def listar_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, "estoque/listar_produtos.html", {"produtos": produtos})


# ADICIONAR PRODUTO
def adicionar_produto(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")
        quantidade = request.POST.get("quantidade")
        categoria_id = request.POST.get("categoria")
        fornecedor_id = request.POST.get("fornecedor")

        categoria = Categoria.objects.get(id=categoria_id)
        fornecedor = Fornecedor.objects.get(id=fornecedor_id)

        Produto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade=quantidade,
            categoria=categoria,
            fornecedor=fornecedor
        )

        return redirect("listar_produtos")

    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()
    return render(request, "estoque/adicionar_produto.html", {
        "categorias": categorias,
        "fornecedores": fornecedores
    })

#EXCLUIR PRODUTO
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.ativo = False
    produto.save()
    return redirect("listar_produtos")


# EDITAR PRODUTO
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        produto.nome = request.POST.get("nome")
        produto.descricao = request.POST.get("descricao")
        produto.preco = request.POST.get("preco")
        produto.quantidade = request.POST.get("quantidade")
        produto.categoria_id = request.POST.get("categoria")
        produto.fornecedor_id = request.POST.get("fornecedor")
        produto.save()

        return redirect("listar_produtos")

    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()

    return render(request, "estoque/editar_produto.html", {
        "produto": produto,
        "categorias": categorias,
        "fornecedores": fornecedores
    })


# REGISTRAR MOVIMENTAÇÃO
def registrar_movimentacao(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        quantidade = int(request.POST.get("quantidade"))

        mov = Movimentacao.objects.create(
            produto=produto,
            tipo=tipo,
            quantidade=quantidade,
        )

        mov.aplicar_movimentacao()

        return redirect("listar_produtos")

    return render(request, "estoque/registrar_movimentacao.html", {"produto": produto})


# HISTÓRICO DE MOVIMENTAÇÕES
def historico_movimentacoes(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    movimentacoes = Movimentacao.objects.filter(produto=produto).order_by("-data")

    return render(request, "estoque/historico_movimentacoes.html", {
        "produto": produto,
        "movimentacoes": movimentacoes
    })

#CATEGORIA
def adicionar_categoria(request):
    if request.method == "POST":
        nome = request.POST.get("nome")

        Categoria.objects.create(nome=nome)
        return redirect("lista_categorias")

    return render(request, "estoque/categorias/categoria_form.html")

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "estoque/categorias/categoria_lista.html", {"categorias": categorias})

#EDITAR CATEGORIA 
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == "POST":
        categoria.nome = request.POST.get("nome")
        categoria.descricao = request.POST.get("descricao")
        categoria.save()
        return redirect("lista_categorias")

    return render(request, "estoque/categorias/categoria_form.html", {
        "categoria": categoria
    })

#EXCLUIR CATEGORIA
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Verificar se existe produto usando esta categoria
    produtos_relacionados = Produto.objects.filter(
    categoria=categoria,
    ativo=True
    ).exists()


    if produtos_relacionados:
        return render(request, "estoque/erro.html", {
            "mensagem": "Não é possível excluir esta categoria porque existem produtos cadastrados usando ela."
        })

    # Se NÃO existir produtos, pode excluir
    categoria.delete()
    return redirect("lista_categorias")



# ---------- FORNECEDOR ----------
def adicionar_fornecedor(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")

        Fornecedor.objects.create(nome=nome, telefone=telefone, email=email)
        return redirect("lista_fornecedores")

    return render(request, "estoque/fornecedores/fornecedor_form.html")

def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, "estoque/fornecedores/fornecedor_lista.html", {"fornecedores": fornecedores})

#EDITAR FORNECEDOR

def editar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)

    if request.method == "POST":
        fornecedor.nome = request.POST.get("nome")
        fornecedor.telefone = request.POST.get("telefone")
        fornecedor.email = request.POST.get("email")
        fornecedor.save()
        return redirect("lista_fornecedores")

    return render(request, "estoque/fornecedores/fornecedor_form.html", {
        "fornecedor": fornecedor
    })

#EXCLUIR FORNECEDOR

def excluir_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)

    if Produto.objects.filter(fornecedor=fornecedor).exists():
        return render(request, "estoque/erro.html", {
            "mensagem": "Não é possível excluir: existem produtos usando este fornecedor."
        })

    fornecedor.delete()
    return redirect("lista_fornecedores")

#HISTORICO
def historico_geral(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data')

    # Adiciona o valor total de cada movimentação
    for m in movimentacoes:
        m.valor_total = m.quantidade * m.produto.preco

    return render(request, "estoque/historico_geral.html", {
        "movimentacoes": movimentacoes
    })


