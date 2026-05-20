def validar_postagem(titulo, descricao):
    """
    Sanitiza e valida os campos de uma postagem.
    Retorna (titulo, descricao, erro)
    """
    t = titulo.strip() if titulo else ""
    d = descricao.strip() if descricao else ""
    
    if not t or not d:
        return None, None, "Título e descrição são obrigatórios"
    
    return t, d, None
