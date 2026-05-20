from flask import render_template, request, redirect, url_for
from app import app, db, cache
from app.models import Postagem
from app.utils import validar_postagem
from app.jobs import background_process_post

@app.route("/")
def index():
    postagens = Postagem.query.order_by(Postagem.id.desc()).all()
    return render_template("index.html", postagens=postagens)

@app.route("/postagens/nova", methods=["GET", "POST"])
def nova_postagem():
    if request.method == "POST":
        titulo, descricao, erro = validar_postagem(
            request.form.get("titulo"), 
            request.form.get("descricao")
        )
        
        if erro:
            return erro, 400
            
        nova_postagem = Postagem(titulo=titulo, descricao=descricao)
        db.session.add(nova_postagem)
        db.session.commit()
        
        # Inicia processamento em segundo plano
        background_process_post(nova_postagem.id, nova_postagem.titulo)
        
        cache.delete_memoized(relatorios)
        return redirect(url_for("index"))
    return render_template("form.html", acao="Nova Postagem")

@app.route("/postagens/editar/<int:id>", methods=["GET", "POST"])
def editar_postagem(id):
    postagem = Postagem.query.get_or_404(id)
    if request.method == "POST":
        titulo, descricao, erro = validar_postagem(
            request.form.get("titulo"), 
            request.form.get("descricao")
        )
        
        if erro:
            return erro, 400
            
        postagem.titulo = titulo
        postagem.descricao = descricao
        db.session.commit()
        cache.delete_memoized(relatorios)
        return redirect(url_for("index"))
    return render_template("form.html", acao="Editar Postagem", postagem=postagem)

@app.route("/postagens/deletar/<int:id>", methods=["POST"])
def deletar_postagem(id):
    postagem = Postagem.query.get_or_404(id)
    db.session.delete(postagem)
    db.session.commit()
    cache.delete_memoized(relatorios)
    return redirect(url_for("index"))

@app.route("/relatorios")
@cache.memoize(timeout=60)
def relatorios():
    total_postagens = Postagem.query.count()
    return render_template("relatorios.html", total_postagens=total_postagens)
