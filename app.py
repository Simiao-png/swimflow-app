# ============================================================
# IMPORTAÇÕES
# ============================================================

from flask import Flask, render_template, request, redirect, session, url_for, Response
from functools import wraps
import calendar
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from modelos.usuarios import cadastrar_usuario, buscar_usuario_por_email, buscar_usuario_por_id, atualizar_perfil
from database.connection import conectar
from xml.sax.saxutils import escape

from modelos.treinos import (
    cadastrar_treino,
    listar_treinos,
    buscar_treino_por_id,
    atualizar_treino,
    excluir_treino_por_id,
    buscar_resumo,
    cadastrar_treino_modelo,
    listar_treinos_modelo,
    buscar_treino_modelo_por_id,
    mover_treino_programado,
    concluir_treino_por_id,
    marcar_treino_realizado
)


# ============================================================
# CONFIGURAÇÃO DO APP
# ============================================================

app = Flask(__name__)
app.secret_key = "natacao_app_secret"

UPLOAD_FOLDER = "static/img/usuarios"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def calcular_pace(duracao_minutos, distancia_metros):
    if distancia_metros == 0:
        return "0:00"

    pace_decimal = duracao_minutos / (distancia_metros / 100)
    pace_minutos = int(pace_decimal)
    pace_segundos = int((pace_decimal - pace_minutos) * 60)

    return f"{pace_minutos}:{pace_segundos:02d}"


def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar_login(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("tela_login"))

        return funcao(*args, **kwargs)

    return verificar_login


# ============================================================
# ROTAS PRINCIPAIS
# ============================================================

@app.route("/")
@login_obrigatorio
def home():
    usuario_id = session["usuario_id"]

    usuario = buscar_usuario_por_id(usuario_id)

    treinos = listar_treinos(usuario_id)
    treinos_modelo = listar_treinos_modelo(usuario_id)
    resumo = buscar_resumo(usuario_id)

    return render_template(
        "index.html",
        treinos=treinos,
        treinos_modelo=treinos_modelo,
        resumo=resumo,
        usuario=usuario,
        usuario_nome=usuario["nome_exibicao"] or usuario["nome"]
    )


# ============================================================
# ROTAS DO CALENDÁRIO
# ============================================================

@app.route("/calendario")
@login_obrigatorio
def calendario_view():
    hoje = date.today()

    ano = int(request.args.get("ano", hoje.year))
    mes = int(request.args.get("mes", hoje.month))

    mes_anterior = mes - 1
    ano_anterior = ano

    if mes_anterior == 0:
        mes_anterior = 12
        ano_anterior -= 1

    proximo_mes = mes + 1
    proximo_ano = ano

    if proximo_mes == 13:
        proximo_mes = 1
        proximo_ano += 1

    nomes_meses = [
        "",
        "JANEIRO",
        "FEVEREIRO",
        "MARÇO",
        "ABRIL",
        "MAIO",
        "JUNHO",
        "JULHO",
        "AGOSTO",
        "SETEMBRO",
        "OUTUBRO",
        "NOVEMBRO",
        "DEZEMBRO"
    ]

    nome_mes = nomes_meses[mes]

    usuario_id = session["usuario_id"]

    treinos = listar_treinos(usuario_id)
    treinos_por_dia = {}

    for treino in treinos:
        data_treino = treino["data_treino"]

        if isinstance(data_treino, str):
            data_treino = datetime.strptime(data_treino, "%Y-%m-%d").date()

        if data_treino.year == ano and data_treino.month == mes:
            dia = data_treino.day

            if dia not in treinos_por_dia:
                treinos_por_dia[dia] = []

            treinos_por_dia[dia].append(treino)

    calendario_mes = calendar.monthcalendar(ano, mes)
    treinos_modelo = listar_treinos_modelo(usuario_id)

    return render_template(
        "calendario.html",
        calendario_mes=calendario_mes,
        treinos_por_dia=treinos_por_dia,
        treinos_modelo=treinos_modelo,
        nome_mes=nome_mes,
        ano=ano,
        mes=mes,
        mes_anterior=mes_anterior,
        ano_anterior=ano_anterior,
        proximo_mes=proximo_mes,
        proximo_ano=proximo_ano
    )


@app.route("/agendar-treino", methods=["POST"])
@login_obrigatorio
def agendar_treino():
    modelo_id = int(request.form["modelo_id"])
    data_treino = request.form["data_treino"]

    usuario_id = session["usuario_id"]

    treino_modelo = buscar_treino_modelo_por_id(modelo_id, usuario_id)

    if treino_modelo is None:
        return redirect(url_for("calendario_view"))

    cadastrar_treino(
        usuario_id,
        data_treino,
        treino_modelo["titulo"],
        treino_modelo["estilo"],
        treino_modelo["tamanho_piscina"],
        treino_modelo["voltas"],
        treino_modelo["distancia_metros"],
        treino_modelo["duracao_minutos"],
        treino_modelo["pace"],
        treino_modelo["observacoes"],
        treino_modelo["equipamentos"],
        status="programado"
    )

    return redirect(url_for("calendario_view"))


@app.route("/mover-treino", methods=["POST"])
@login_obrigatorio
def mover_treino():
    treino_id = int(request.form["treino_id"])
    nova_data = request.form["nova_data"]

    mover_treino_programado(treino_id, nova_data)

    return redirect(url_for("calendario_view"))


# ============================================================
# ROTAS DE TREINOS
# ============================================================

@app.route("/treino/<int:id>")
@login_obrigatorio
def detalhe_treino(id):
    treino = buscar_treino_por_id(id)

    return render_template(
        "detalhe_treino.html",
        treino=treino
    )


@app.route("/salvar", methods=["POST"])
@login_obrigatorio
def salvar():
    usuario_id = session["usuario_id"]
    data_treino = request.form["data_treino"]
    titulo = request.form["titulo"]
    estilo = request.form["estilo"]

    tamanho_piscina = float(request.form["tamanho_piscina"])
    voltas = int(request.form["voltas"])
    duracao_minutos = int(request.form["duracao_minutos"])

    observacoes = request.form.get("observacoes", "")

    equipamentos = request.form.getlist("equipamentos")
    equipamentos = ", ".join(equipamentos)

    distancia_metros = tamanho_piscina * voltas

    pace = calcular_pace(
        duracao_minutos,
        distancia_metros
    )

    cadastrar_treino(
        usuario_id,
        data_treino,
        titulo,
        estilo,
        tamanho_piscina,
        voltas,
        distancia_metros,
        duracao_minutos,
        pace,
        observacoes,
        equipamentos
    )

    return redirect(url_for("home"))


@app.route("/treino/<int:id>/editar")
@login_obrigatorio
def editar_treino(id):
    treino = buscar_treino_por_id(id)

    return render_template(
        "editar_treino.html",
        treino=treino
    )


@app.route("/treino/<int:id>/atualizar", methods=["POST"])
@login_obrigatorio
def atualizar(id):
    data_treino = request.form["data_treino"]
    titulo = request.form["titulo"]
    estilo = request.form["estilo"]

    tamanho_piscina = float(request.form["tamanho_piscina"])
    voltas = int(request.form["voltas"])
    duracao_minutos = int(request.form["duracao_minutos"])

    observacoes = request.form.get("observacoes", "")

    equipamentos = request.form.getlist("equipamentos")
    equipamentos = ", ".join(equipamentos)

    distancia_metros = tamanho_piscina * voltas

    pace = calcular_pace(
        duracao_minutos,
        distancia_metros
    )

    atualizar_treino(
        id,
        data_treino,
        titulo,
        estilo,
        tamanho_piscina,
        voltas,
        distancia_metros,
        duracao_minutos,
        pace,
        observacoes,
        equipamentos
    )

    return redirect(url_for("detalhe_treino", id=id))


@app.route("/treino/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_treino(id):
    excluir_treino_por_id(id)

    return redirect(url_for("home"))


@app.route("/concluir-treino/<int:id>", methods=["POST"])
@login_obrigatorio
def concluir_treino(id):
    concluir_treino_por_id(id)

    return redirect(url_for("home"))


@app.route("/treino/<int:id>/realizar", methods=["POST"])
@login_obrigatorio
def realizar_treino(id):
    marcar_treino_realizado(id)

    return redirect(url_for("home"))


@app.route("/treino/<int:id>/exportar-tcx")
@login_obrigatorio
def exportar_tcx(id):
    treino = buscar_treino_por_id(id)

    if treino is None:
        return redirect(url_for("home"))

    data_treino = treino["data_treino"]

    if isinstance(data_treino, str):
        data_treino = datetime.strptime(data_treino, "%Y-%m-%d").date()

    data_inicio = datetime.combine(data_treino, datetime.min.time())
    data_iso = data_inicio.strftime("%Y-%m-%dT%H:%M:%SZ")

    titulo = escape(str(treino["titulo"]))
    distancia = float(treino["distancia_metros"])
    duracao_segundos = int(treino["duracao_minutos"]) * 60

    tcx = f"""<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase
    xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">

    <Activities>
        <Activity Sport="Other">
            <Id>{data_iso}</Id>

            <Lap StartTime="{data_iso}">
                <TotalTimeSeconds>{duracao_segundos}</TotalTimeSeconds>
                <DistanceMeters>{distancia}</DistanceMeters>
                <Calories>0</Calories>
                <Intensity>Active</Intensity>
                <TriggerMethod>Manual</TriggerMethod>

                <Track>
                    <Trackpoint>
                        <Time>{data_iso}</Time>
                        <DistanceMeters>0</DistanceMeters>
                    </Trackpoint>

                    <Trackpoint>
                        <Time>{data_iso}</Time>
                        <DistanceMeters>{distancia}</DistanceMeters>
                    </Trackpoint>
                </Track>
            </Lap>

            <Notes>{titulo}</Notes>
        </Activity>
    </Activities>

</TrainingCenterDatabase>
"""

    nome_arquivo = f"treino_{id}.tcx"

    return Response(
        tcx,
        mimetype="application/vnd.garmin.tcx+xml",
        headers={
            "Content-Disposition": f"attachment; filename={nome_arquivo}"
        }
    )


# ============================================================
# ROTAS DE MODELOS DE TREINO
# ============================================================

@app.route("/salvar-modelo", methods=["POST"])
@login_obrigatorio
def salvar_modelo():
    titulo = request.form["titulo"]
    estilo = request.form["estilo"]

    tamanho_piscina = float(request.form["tamanho_piscina"])
    voltas = int(request.form["voltas"])
    duracao_minutos = int(request.form["duracao_minutos"])

    observacoes = request.form.get("observacoes", "")

    equipamentos = request.form.getlist("equipamentos")
    equipamentos = ", ".join(equipamentos)

    distancia_metros = tamanho_piscina * voltas

    pace = calcular_pace(
        duracao_minutos,
        distancia_metros
    )

    usuario_id = session["usuario_id"]

    cadastrar_treino_modelo(
        usuario_id,
        titulo,
        estilo,
        tamanho_piscina,
        voltas,
        distancia_metros,
        duracao_minutos,
        pace,
        observacoes,
        equipamentos
    )

    return redirect(url_for("home"))


# ============================================================
# ROTAS DE USUÁRIOS / LOGIN
# ============================================================

@app.route("/cadastro-usuario")
def tela_cadastro_usuario():
    return render_template("cadastro_usuario.html")


@app.route("/cadastrar-usuario", methods=["POST"])
def cadastrar_usuario_app():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = generate_password_hash(request.form["senha"])

    usuario_existente = buscar_usuario_por_email(email)

    if usuario_existente:
        return "Email já cadastrado"

    cadastrar_usuario(nome, email, senha)

    return redirect(url_for("tela_login"))


@app.route("/login")
def tela_login():
    return render_template("login.html")


@app.route("/recuperar-senha")
def recuperar_senha():
    return render_template("recuperar_senha.html")


@app.route("/alterar-senha")
def tela_alterar_senha():
    return render_template(
        "alterar_senha.html"
    )


@app.route("/enviar-recuperacao", methods=["POST"])
def enviar_recuperacao():
    email = request.form["email"]

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return render_template(
            "recuperar_senha.html",
            erro="Email não encontrado"
        )

    return redirect(
        url_for(
            "tela_alterar_senha",
            email=email
        )
    )


@app.route("/salvar-nova-senha", methods=["POST"])
def salvar_nova_senha():
    email = request.form["email"]

    nova_senha = request.form["nova_senha"]
    confirmar_senha = request.form["confirmar_senha"]

    if nova_senha != confirmar_senha:
        return render_template(
            "alterar_senha.html",
            erro="As senhas não coincidem"
        )

    senha_hash = generate_password_hash(nova_senha)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET senha = %s
        WHERE email = %s
        """,
        (senha_hash, email)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(
        url_for("tela_login")
    )


@app.route("/logar", methods=["POST"])
def logar():
    email = request.form["email"]
    senha = request.form["senha"]

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return render_template(
            "login.html",
            erro="Usuário ou senha incorretos"
        )

    senha_salva = usuario["senha"]

    senha_valida = False

    if senha_salva.startswith("scrypt:"):
        senha_valida = check_password_hash(
            senha_salva,
            senha
        )
    else:
        senha_valida = senha_salva == senha

    if not senha_valida:
        return render_template(
            "login.html",
            erro="Usuário ou senha incorretos"
        )

    session["usuario_id"] = usuario["id"]
    session["usuario_nome"] = usuario["nome"]

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("tela_login"))

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if "usuario_id" not in session:
        return redirect(url_for("tela_login"))

    usuario_id = session["usuario_id"]

    if request.method == "POST":
        nome_exibicao = request.form.get("nome_exibicao") or None
        idade = request.form.get("idade") or None
        peso_kg = request.form.get("peso_kg") or None
        altura_cm = request.form.get("altura_cm") or None

        atualizar_perfil(
            usuario_id,
            nome_exibicao,
            idade,
            peso_kg,
            altura_cm
        )

        if nome_exibicao:
            session["usuario_nome"] = nome_exibicao

        return redirect(url_for("home"  ))

    usuario = buscar_usuario_por_id(usuario_id)

    return render_template(
        "perfil.html",
        usuario=usuario
    )

# ============================================================
# EXECUÇÃO DO APP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)