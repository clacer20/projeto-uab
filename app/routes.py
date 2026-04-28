from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Postagem

@app.route("/")
def index():
    postagens = Postagem.query.order_by(Postagem.id.desc()).all()
    return render_template("index.html", postagens=postagens)

@app.route("/postagens/nova", methods=["GET", "POST"])
def nova_postagem():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        nova_postagem = Postagem(titulo=titulo, descricao=descricao)
        db.session.add(nova_postagem)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("form.html", acao="Nova Postagem")

@app.route("/postagens/editar/<int:id>", methods=["GET", "POST"])
def editar_postagem(id):
    postagem = Postagem.query.get_or_404(id)
    if request.method == "POST":
        postagem.titulo = request.form.get("titulo")
        postagem.descricao = request.form.get("descricao")
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("form.html", acao="Editar Postagem", postagem=postagem)

@app.route("/postagens/deletar/<int:id>", methods=["POST"])
def deletar_postagem(id):
    postagem = Postagem.query.get_or_404(id)
    db.session.delete(postagem)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/relatorios")
def relatorios():
    total_postagens = Postagem.query.count()
    return render_template("relatorios.html", total_postagens=total_postagens)
