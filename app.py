from flask import Flask, render_template, request, redirect

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

import calendar
from datetime import date, datetime


app = Flask(__name__)


def calcular_pace(duracao_minutos, distancia_metros):

    if distancia_metros == 0:
        return "0:00"

    pace_decimal = duracao_minutos / (distancia_metros / 100)

    pace_minutos = int(pace_decimal)
    pace_segundos = int((pace_decimal - pace_minutos) * 60)

    return f"{pace_minutos}:{pace_segundos:02d}"


@app.route('/')
def home():

    treinos = listar_treinos()
    treinos_modelo = listar_treinos_modelo()
    resumo = buscar_resumo()

    return render_template(
        'index.html',
        treinos=treinos,
        treinos_modelo=treinos_modelo,
        resumo=resumo
    )


@app.route('/calendario')
def calendario():

    hoje = date.today()

    ano = int(request.args.get('ano', hoje.year))
    mes = int(request.args.get('mes', hoje.month))

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

    treinos = listar_treinos()
    treinos_por_dia = {}

    for treino in treinos:

        data_treino = treino['data_treino']

        if isinstance(data_treino, str):
            data_treino = datetime.strptime(
                data_treino,
                '%Y-%m-%d'
            ).date()

        if data_treino.year == ano and data_treino.month == mes:

            dia = data_treino.day

            if dia not in treinos_por_dia:
                treinos_por_dia[dia] = []

            treinos_por_dia[dia].append(treino)

    calendario_mes = calendar.monthcalendar(ano, mes)

    treinos_modelo = listar_treinos_modelo()

    return render_template(
        'calendario.html',
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


@app.route('/treino/<int:id>')
def detalhe_treino(id):

    treino = buscar_treino_por_id(id)

    return render_template(
        'detalhe_treino.html',
        treino=treino
    )


@app.route('/salvar', methods=['POST'])
def salvar():

    data_treino = request.form['data_treino']
    titulo = request.form['titulo']
    estilo = request.form['estilo']

    tamanho_piscina = float(request.form['tamanho_piscina'])
    voltas = int(request.form['voltas'])
    duracao_minutos = int(request.form['duracao_minutos'])

    observacoes = request.form.get('observacoes', '')

    equipamentos = request.form.getlist('equipamentos')
    equipamentos = ', '.join(equipamentos)

    distancia_metros = tamanho_piscina * voltas

    pace = calcular_pace(
        duracao_minutos,
        distancia_metros
    )

    cadastrar_treino(
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

    return redirect('/')


@app.route('/salvar-modelo', methods=['POST'])
def salvar_modelo():

    titulo = request.form['titulo']
    estilo = request.form['estilo']

    tamanho_piscina = float(request.form['tamanho_piscina'])
    voltas = int(request.form['voltas'])
    duracao_minutos = int(request.form['duracao_minutos'])

    observacoes = request.form.get('observacoes', '')

    equipamentos = request.form.getlist('equipamentos')
    equipamentos = ', '.join(equipamentos)

    distancia_metros = tamanho_piscina * voltas

    pace = calcular_pace(
        duracao_minutos,
        distancia_metros
    )

    cadastrar_treino_modelo(
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

    return redirect('/')


@app.route('/agendar-treino', methods=['POST'])
def agendar_treino():

    modelo_id = int(request.form['modelo_id'])
    data_treino = request.form['data_treino']

    treino_modelo = buscar_treino_modelo_por_id(modelo_id)

    if treino_modelo is None:
        return redirect('/calendario')

    cadastrar_treino(
        data_treino,
        treino_modelo['titulo'],
        treino_modelo['estilo'],
        treino_modelo['tamanho_piscina'],
        treino_modelo['voltas'],
        treino_modelo['distancia_metros'],
        treino_modelo['duracao_minutos'],
        treino_modelo['pace'],
        treino_modelo['observacoes'],
        treino_modelo['equipamentos'],
        status="programado"
    )

    return redirect('/calendario')


@app.route('/mover-treino', methods=['POST'])
def mover_treino():

    treino_id = int(request.form['treino_id'])
    nova_data = request.form['nova_data']

    mover_treino_programado(treino_id, nova_data)

    return redirect('/calendario')


@app.route('/concluir-treino/<int:id>', methods=['POST'])
def concluir_treino(id):

    concluir_treino_por_id(id)

    return redirect('/')


@app.route('/treino/<int:id>/editar')
def editar_treino(id):

    treino = buscar_treino_por_id(id)

    return render_template(
        'editar_treino.html',
        treino=treino
    )


@app.route('/treino/<int:id>/atualizar', methods=['POST'])
def atualizar(id):

    data_treino = request.form['data_treino']
    titulo = request.form['titulo']
    estilo = request.form['estilo']

    tamanho_piscina = float(request.form['tamanho_piscina'])
    voltas = int(request.form['voltas'])
    duracao_minutos = int(request.form['duracao_minutos'])

    observacoes = request.form.get('observacoes', '')

    equipamentos = request.form.getlist('equipamentos')
    equipamentos = ', '.join(equipamentos)

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

    return redirect(f'/treino/{id}')


@app.route('/treino/<int:id>/excluir', methods=['POST'])
def excluir_treino(id):

    excluir_treino_por_id(id)

    return redirect('/')

@app.route('/treino/<int:id>/realizar', methods=['POST'])
def realizar_treino(id):
    marcar_treino_realizado(id)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)