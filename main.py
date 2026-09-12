import streamlit as st
from datetime import date, datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Súmula Digital de Vôlei",
    page_icon="🏐",
    layout="wide"
)


# ==========================================================
# ESTADOS INICIAIS
# ==========================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "equipe_a" not in st.session_state:
    st.session_state.equipe_a = ""

if "equipe_b" not in st.session_state:
    st.session_state.equipe_b = ""

if "tecnico_a" not in st.session_state:
    st.session_state.tecnico_a = ""

if "tecnico_b" not in st.session_state:
    st.session_state.tecnico_b = ""

if "arbitro" not in st.session_state:
    st.session_state.arbitro = ""

if "jogadores_a" not in st.session_state:
    st.session_state.jogadores_a = []

if "jogadores_b" not in st.session_state:
    st.session_state.jogadores_b = []

if "pontos_a" not in st.session_state:
    st.session_state.pontos_a = 0

if "pontos_b" not in st.session_state:
    st.session_state.pontos_b = 0

if "sets_a" not in st.session_state:
    st.session_state.sets_a = 0

if "sets_b" not in st.session_state:
    st.session_state.sets_b = 0

if "set_atual" not in st.session_state:
    st.session_state.set_atual = 1

if "resultados_sets" not in st.session_state:
    st.session_state.resultados_sets = []

if "partida_iniciada" not in st.session_state:
    st.session_state.partida_iniciada = False

if "partida_finalizada" not in st.session_state:
    st.session_state.partida_finalizada = False

if "cadastro_salvo" not in st.session_state:
    st.session_state.cadastro_salvo = False

if "partida_salva" not in st.session_state:
    st.session_state.partida_salva = False

if "eventos_set" not in st.session_state:
    st.session_state.eventos_set = []

if "ocorrencias" not in st.session_state:
    st.session_state.ocorrencias = []


# ==========================================================
# FUNÇÃO PARA NOVA PARTIDA
# ==========================================================

def nova_partida():

    st.session_state.equipe_a = ""
    st.session_state.equipe_b = ""

    st.session_state.tecnico_a = ""
    st.session_state.tecnico_b = ""

    st.session_state.arbitro = ""

    st.session_state.jogadores_a = []
    st.session_state.jogadores_b = []

    st.session_state.pontos_a = 0
    st.session_state.pontos_b = 0

    st.session_state.sets_a = 0
    st.session_state.sets_b = 0

    st.session_state.set_atual = 1

    st.session_state.resultados_sets = []

    st.session_state.partida_iniciada = False
    st.session_state.partida_finalizada = False
    st.session_state.cadastro_salvo = False
    st.session_state.partida_salva = False

    st.session_state.eventos_set = []
    st.session_state.ocorrencias = []

    chaves = list(st.session_state.keys())

    for chave in chaves:

        if (
            chave.startswith("nome_a_")
            or chave.startswith("numero_a_")
            or chave.startswith("reserva_nome_a_")
            or chave.startswith("reserva_numero_a_")
            or chave.startswith("nome_b_")
            or chave.startswith("numero_b_")
            or chave.startswith("reserva_nome_b_")
            or chave.startswith("reserva_numero_b_")
            or chave in [
                "campo_equipe_a",
                "campo_equipe_b",
                "campo_tecnico_a",
                "campo_tecnico_b",
                "campo_arbitro"
            ]
        ):
            del st.session_state[chave]


# ==========================================================
# LIMITE DO SET
# ==========================================================

def limite_do_set():

    if st.session_state.set_atual == 5:
        return 15

    return 25


# ==========================================================
# VERIFICAR VENCEDOR DO SET
# ==========================================================

def verificar_vencedor_set():

    limite = limite_do_set()

    pontos_a = st.session_state.pontos_a
    pontos_b = st.session_state.pontos_b

    # Regra oficial:
    # precisa atingir o limite e ter 2 pontos de vantagem.

    if pontos_a >= limite and pontos_a - pontos_b >= 2:
        return "A"

    if pontos_b >= limite and pontos_b - pontos_a >= 2:
        return "B"

    return None


# ==========================================================
# ADICIONAR PONTO
# ==========================================================

def adicionar_ponto(equipe, responsavel):

    if equipe == "A":

        st.session_state.pontos_a += 1

        novo_ponto = st.session_state.pontos_a

        equipe_nome = st.session_state.equipe_a

    else:

        st.session_state.pontos_b += 1

        novo_ponto = st.session_state.pontos_b

        equipe_nome = st.session_state.equipe_b

    evento = {
        "set": st.session_state.set_atual,
        "ponto": novo_ponto,
        "equipe": equipe_nome,
        "equipe_codigo": equipe,
        "responsavel": responsavel,
        "tipo": "Ponto"
    }

    st.session_state.eventos_set.append(evento)


# ==========================================================
# FINALIZAR SET
# ==========================================================

def finalizar_set():

    vencedor = verificar_vencedor_set()

    if vencedor is None:

        limite = limite_do_set()

        st.warning(
            f"O set ainda não terminou. "
            f"É necessário chegar a {limite} pontos "
            f"com 2 pontos de vantagem."
        )

        return False

    resultado = {
        "set": st.session_state.set_atual,
        "pontos_a": st.session_state.pontos_a,
        "pontos_b": st.session_state.pontos_b,
        "vencedor": vencedor,

        "eventos": [
            evento.copy()
            for evento in st.session_state.eventos_set
        ]
    }

    st.session_state.resultados_sets.append(resultado)

    if vencedor == "A":
        st.session_state.sets_a += 1
    else:
        st.session_state.sets_b += 1

    if (
        st.session_state.sets_a == 3
        or st.session_state.sets_b == 3
    ):

        st.session_state.partida_finalizada = True

    else:

        st.session_state.set_atual += 1

        st.session_state.pontos_a = 0
        st.session_state.pontos_b = 0

        st.session_state.eventos_set = []

    return True


# ==========================================================
# REGISTRAR OCORRÊNCIA
# ==========================================================

def registrar_ocorrencia(
    equipe,
    pessoa,
    tipo,
    descricao
):

    equipe_nome = (
        st.session_state.equipe_a
        if equipe == "A"
        else st.session_state.equipe_b
    )

    ocorrencia = {
        "data": str(date.today()),
        "set": st.session_state.set_atual,
        "equipe": equipe_nome,
        "pessoa": pessoa,
        "tipo": tipo,
        "descricao": descricao
    }

    st.session_state.ocorrencias.append(
        ocorrencia
    )


# ==========================================================
# GERAR PDF
# ==========================================================

def gerar_pdf(partida):

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "Titulo",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Heading2"],
        fontSize=13,
        spaceBefore=10,
        spaceAfter=8
    )

    normal = ParagraphStyle(
        "NormalCustom",
        parent=estilos["Normal"],
        fontSize=9,
        leading=12
    )

    elementos = []

    # ------------------------------------------------------
    # TÍTULO
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "SÚMULA DIGITAL DE VÔLEI",
            titulo
        )
    )

    elementos.append(
        Paragraph(
            "Relatório oficial da partida",
            ParagraphStyle(
                "Centro",
                parent=normal,
                alignment=TA_CENTER
            )
        )
    )

    elementos.append(Spacer(1, 15))

    # ------------------------------------------------------
    # INFORMAÇÕES
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "1. INFORMAÇÕES DA PARTIDA",
            subtitulo
        )
    )

    info = [
        ["Data", partida["data"]],
        ["Equipe 1", partida["equipe_a"]],
        ["Técnico", partida["tecnico_a"]],
        ["Equipe 2", partida["equipe_b"]],
        ["Técnico", partida["tecnico_b"]],
        ["Árbitro", partida["arbitro"]],
        [
            "Resultado",
            f"{partida['sets_a']} × {partida['sets_b']}"
        ],
        ["Vencedor", partida["vencedor"]]
    ]

    tabela = Table(
        info,
        colWidths=[4 * cm, 13 * cm]
    )

    tabela.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elementos.append(tabela)

    # ------------------------------------------------------
    # JOGADORES
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "2. JOGADORES",
            subtitulo
        )
    )

    jogadores_tabela = [
        [
            partida["equipe_a"],
            partida["equipe_b"]
        ]
    ]

    max_jogadores = max(
        len(partida["jogadores_a"]),
        len(partida["jogadores_b"])
    )

    for i in range(max_jogadores):

        jogador_a = ""

        jogador_b = ""

        if i < len(partida["jogadores_a"]):

            j = partida["jogadores_a"][i]

            tipo = (
                "Titular"
                if j["titular"]
                else "Reserva"
            )

            jogador_a = (
                f"#{j['numero']} - "
                f"{j['nome']} ({tipo})"
            )

        if i < len(partida["jogadores_b"]):

            j = partida["jogadores_b"][i]

            tipo = (
                "Titular"
                if j["titular"]
                else "Reserva"
            )

            jogador_b = (
                f"#{j['numero']} - "
                f"{j['nome']} ({tipo})"
            )

        jogadores_tabela.append(
            [jogador_a, jogador_b]
        )

    tabela_jogadores = Table(
        jogadores_tabela,
        colWidths=[8.5 * cm, 8.5 * cm]
    )

    tabela_jogadores.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    elementos.append(tabela_jogadores)

    # ------------------------------------------------------
    # RESULTADO DOS SETS
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "3. RESULTADO DOS SETS",
            subtitulo
        )
    )

    sets_tabela = [
        [
            "Set",
            partida["equipe_a"],
            partida["equipe_b"],
            "Vencedor"
        ]
    ]

    for resultado in partida["resultados"]:

        vencedor = (
            partida["equipe_a"]
            if resultado["vencedor"] == "A"
            else partida["equipe_b"]
        )

        sets_tabela.append([
            str(resultado["set"]),
            str(resultado["pontos_a"]),
            str(resultado["pontos_b"]),
            vencedor
        ])

    tabela_sets = Table(
        sets_tabela,
        colWidths=[
            2 * cm,
            4.5 * cm,
            4.5 * cm,
            6 * cm
        ]
    )

    tabela_sets.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ])
    )

    elementos.append(tabela_sets)

    # ------------------------------------------------------
    # PONTOS
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "4. REGISTRO DOS PONTOS",
            subtitulo
        )
    )

    for resultado in partida["resultados"]:

        elementos.append(
            Paragraph(
                f"Set {resultado['set']}: "
                f"{resultado['pontos_a']} × "
                f"{resultado['pontos_b']}",
                normal
            )
        )

        eventos = resultado.get("eventos", [])

        if not eventos:

            elementos.append(
                Paragraph(
                    "Nenhum ponto detalhado registrado.",
                    normal
                )
            )

        else:

            pontos_tabela = [
                [
                    "Ponto",
                    "Equipe",
                    "Responsável"
                ]
            ]

            for evento in eventos:

                pontos_tabela.append([
                    str(evento["ponto"]),
                    evento["equipe"],
                    evento["responsavel"]
                ])

            tabela_pontos = Table(
                pontos_tabela,
                colWidths=[
                    2.5 * cm,
                    6 * cm,
                    8.5 * cm
                ]
            )

            tabela_pontos.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8
                    ),
                ])
            )

            elementos.append(tabela_pontos)

            elementos.append(Spacer(1, 8))

    # ------------------------------------------------------
    # OCORRÊNCIAS / PUNIÇÕES
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "5. OCORRÊNCIAS E PUNIÇÕES",
            subtitulo
        )
    )

    ocorrencias = partida.get(
        "ocorrencias",
        []
    )

    if not ocorrencias:

        elementos.append(
            Paragraph(
                "Nenhuma ocorrência ou punição registrada.",
                normal
            )
        )

    else:

        ocorrencias_tabela = [
            [
                "Set",
                "Equipe",
                "Pessoa",
                "Tipo",
                "Descrição"
            ]
        ]

        for ocorrencia in ocorrencias:

            ocorrencias_tabela.append([
                str(ocorrencia["set"]),
                ocorrencia["equipe"],
                ocorrencia["pessoa"],
                ocorrencia["tipo"],
                ocorrencia["descricao"]
            ])

        tabela_ocorrencias = Table(
            ocorrencias_tabela,
            colWidths=[
                1.2 * cm,
                4 * cm,
                3.5 * cm,
                3.5 * cm,
                5.5 * cm
            ],
            repeatRows=1
        )

        tabela_ocorrencias.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )

        elementos.append(
            tabela_ocorrencias
        )

    # ------------------------------------------------------
    # OBSERVAÇÕES
    # ------------------------------------------------------

    elementos.append(
        Paragraph(
            "6. OBSERVAÇÕES",
            subtitulo
        )
    )

    if partida.get("observacao"):

        elementos.append(
            Paragraph(
                partida["observacao"],
                normal
            )
        )

    else:

        elementos.append(
            Paragraph(
                "Nenhuma observação registrada.",
                normal
            )
        )

    # ------------------------------------------------------
    # ASSINATURA
    # ------------------------------------------------------

    elementos.append(Spacer(1, 30))

    elementos.append(
        Paragraph(
            "________________________________________",
            ParagraphStyle(
                "Assinatura",
                parent=normal,
                alignment=TA_CENTER
            )
        )
    )

    elementos.append(
        Paragraph(
            "Árbitro",
            ParagraphStyle(
                "AssinaturaTexto",
                parent=normal,
                alignment=TA_CENTER
            )
        )
    )

    documento.build(elementos)

    buffer.seek(0)

    return buffer


# ==========================================================
# TÍTULO
# ==========================================================

st.title("🏐 Súmula Digital de Vôlei")

st.caption(
    "Sistema digital para cadastro e acompanhamento de partidas"
)


# ==========================================================
# MENU LATERAL
# ==========================================================

with st.sidebar:

    st.header("🏐 SÚMULA")

    st.divider()

    pagina = st.selectbox(
        "Menu",
        [
            "📋 Cadastro das equipes",
            "🏐 Partida",
            "📜 Histórico",
            "📄 Relatório"
        ]
    )

    st.divider()

    st.caption("Regras da partida")

    st.write("🏆 Melhor de 5 sets")
    st.write("🏐 Sets 1 a 4: 25 pontos")
    st.write("🔥 5º set: 15 pontos")
    st.write("➕ Diferença mínima de 2 pontos")


# ==========================================================
# CADASTRO
# ==========================================================

if pagina == "📋 Cadastro das equipes":

    st.header("📋 Cadastro das equipes")

    st.info(
        "Cadastre as equipes, técnicos, jogadores "
        "titulares, reservas e árbitro."
    )

    # ======================================================
    # EQUIPE 1
    # ======================================================

    st.subheader("🏐 Equipe 1")

    col1, col2 = st.columns(2)

    with col1:

        nome_a = st.text_input(
            "Nome da equipe",
            value=st.session_state.equipe_a,
            key="campo_equipe_a"
        )

    with col2:

        tecnico_a = st.text_input(
            "Técnico",
            value=st.session_state.tecnico_a,
            key="campo_tecnico_a"
        )

    st.write("### 👕 Jogadores titulares")

    jogadores_a = []

    for i in range(6):

        col1, col2 = st.columns([4, 1])

        with col1:

            nome = st.text_input(
                f"Jogador {i + 1}",
                key=f"nome_a_{i}"
            )

        with col2:

            numero = st.number_input(
                "Nº",
                min_value=1,
                max_value=99,
                value=i + 1,
                key=f"numero_a_{i}"
            )

        if nome.strip():

            jogadores_a.append({
                "nome": nome,
                "numero": numero,
                "titular": True
            })

    st.write("### 🔄 Jogadores reservas")

    for i in range(6):

        col1, col2 = st.columns([4, 1])

        with col1:

            nome = st.text_input(
                f"Reserva {i + 1}",
                key=f"reserva_nome_a_{i}"
            )

        with col2:

            numero = st.number_input(
                "Nº",
                min_value=1,
                max_value=99,
                value=i + 7,
                key=f"reserva_numero_a_{i}"
            )

        if nome.strip():

            jogadores_a.append({
                "nome": nome,
                "numero": numero,
                "titular": False
            })

    st.divider()

    # ======================================================
    # EQUIPE 2
    # ======================================================

    st.subheader("🏐 Equipe 2")

    col1, col2 = st.columns(2)

    with col1:

        nome_b = st.text_input(
            "Nome da equipe",
            value=st.session_state.equipe_b,
            key="campo_equipe_b"
        )

    with col2:

        tecnico_b = st.text_input(
            "Técnico",
            value=st.session_state.tecnico_b,
            key="campo_tecnico_b"
        )

    st.write("### 👕 Jogadores titulares")

    jogadores_b = []

    for i in range(6):

        col1, col2 = st.columns([4, 1])

        with col1:

            nome = st.text_input(
                f"Jogador {i + 1}",
                key=f"nome_b_{i}"
            )

        with col2:

            numero = st.number_input(
                "Nº",
                min_value=1,
                max_value=99,
                value=i + 1,
                key=f"numero_b_{i}"
            )

        if nome.strip():

            jogadores_b.append({
                "nome": nome,
                "numero": numero,
                "titular": True
            })

    st.write("### 🔄 Jogadores reservas")

    for i in range(6):

        col1, col2 = st.columns([4, 1])

        with col1:

            nome = st.text_input(
                f"Reserva {i + 1}",
                key=f"reserva_nome_b_{i}"
            )

        with col2:

            numero = st.number_input(
                "Nº",
                min_value=1,
                max_value=99,
                value=i + 7,
                key=f"reserva_numero_b_{i}"
            )

        if nome.strip():

            jogadores_b.append({
                "nome": nome,
                "numero": numero,
                "titular": False
            })

    st.divider()

    # ======================================================
    # ÁRBITRO
    # ======================================================

    st.subheader("👨‍⚖️ Arbitragem")

    arbitro = st.text_input(
        "Nome do árbitro",
        value=st.session_state.arbitro,
        key="campo_arbitro"
    )

    st.divider()

    # ======================================================
    # SALVAR
    # ======================================================

    if st.button(
        "💾 SALVAR CADASTRO",
        use_container_width=True,
        type="primary"
    ):

        if not nome_a.strip():

            st.error(
                "Digite o nome da Equipe 1."
            )

        elif not nome_b.strip():

            st.error(
                "Digite o nome da Equipe 2."
            )

        else:

            st.session_state.equipe_a = nome_a
            st.session_state.equipe_b = nome_b

            st.session_state.tecnico_a = tecnico_a
            st.session_state.tecnico_b = tecnico_b

            st.session_state.jogadores_a = jogadores_a
            st.session_state.jogadores_b = jogadores_b

            st.session_state.arbitro = arbitro

            st.session_state.cadastro_salvo = True

            st.success(
                "✅ Cadastro salvo com sucesso!"
            )


# ==========================================================
# PARTIDA
# ==========================================================

elif pagina == "🏐 Partida":

    st.header("🏐 Partida")

    if not st.session_state.cadastro_salvo:

        st.warning(
            "⚠️ Primeiro faça o cadastro das equipes."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                f"🏐 {st.session_state.equipe_a}"
            )

            st.write(
                f"**Técnico:** "
                f"{st.session_state.tecnico_a}"
            )

        with col2:

            st.subheader(
                f"🏐 {st.session_state.equipe_b}"
            )

            st.write(
                f"**Técnico:** "
                f"{st.session_state.tecnico_b}"
            )

        st.write(
            f"👨‍⚖️ **Árbitro:** "
            f"{st.session_state.arbitro}"
        )

        st.divider()

        # ==================================================
        # JOGADORES
        # ==================================================

        st.subheader("👥 Jogadores")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"### 🏐 {st.session_state.equipe_a}"
            )

            st.write("**Titulares:**")

            for jogador in st.session_state.jogadores_a:

                if jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )

            st.write("**Reservas:**")

            for jogador in st.session_state.jogadores_a:

                if not jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )

        with col2:

            st.markdown(
                f"### 🏐 {st.session_state.equipe_b}"
            )

            st.write("**Titulares:**")

            for jogador in st.session_state.jogadores_b:

                if jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )

            st.write("**Reservas:**")

            for jogador in st.session_state.jogadores_b:

                if not jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )

        st.divider()

        # ==================================================
        # INICIAR PARTIDA
        # ==================================================

        if not st.session_state.partida_iniciada:

            st.subheader("▶️ Iniciar partida")

            st.markdown(
                f"## {st.session_state.equipe_a} "
                f"× "
                f"{st.session_state.equipe_b}"
            )

            if st.button(
                "▶️ INICIAR PARTIDA",
                use_container_width=True,
                type="primary"
            ):

                st.session_state.partida_iniciada = True

                st.rerun()

        # ==================================================
        # PARTIDA EM ANDAMENTO
        # ==================================================

        elif not st.session_state.partida_finalizada:

            limite = limite_do_set()

            st.subheader(
                f"🏆 SET {st.session_state.set_atual}"
            )

            if st.session_state.set_atual == 5:

                st.info(
                    "🔥 5º SET — até 15 pontos, "
                    "com diferença mínima de 2."
                )

            else:

                st.info(
                    "🏐 SET — até 25 pontos, "
                    "com diferença mínima de 2."
                )

            # ==============================================
            # PLACAR
            # ==============================================

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"# {st.session_state.equipe_a}"
                )

                st.metric(
                    "PONTOS",
                    st.session_state.pontos_a
                )

                jogadores_nomes_a = [
                    f"#{j['numero']} - {j['nome']}"
                    for j in st.session_state.jogadores_a
                ]

                jogador_ponto_a = st.selectbox(
                    "Quem fez o ponto?",
                    jogadores_nomes_a
                    + ["Erro do adversário"],
                    key=f"responsavel_a_{st.session_state.set_atual}_{st.session_state.pontos_a}"
                )

                if st.button(
                    "➕ PONTO",
                    key="ponto_a",
                    use_container_width=True
                ):

                    adicionar_ponto(
                        "A",
                        jogador_ponto_a
                    )

                    st.rerun()

            with col2:

                st.markdown(
                    f"# {st.session_state.equipe_b}"
                )

                st.metric(
                    "PONTOS",
                    st.session_state.pontos_b
                )

                jogadores_nomes_b = [
                    f"#{j['numero']} - {j['nome']}"
                    for j in st.session_state.jogadores_b
                ]

                jogador_ponto_b = st.selectbox(
                    "Quem fez o ponto?",
                    jogadores_nomes_b
                    + ["Erro do adversário"],
                    key=f"responsavel_b_{st.session_state.set_atual}_{st.session_state.pontos_b}"
                )

                if st.button(
                    "➕ PONTO",
                    key="ponto_b",
                    use_container_width=True
                ):

                    adicionar_ponto(
                        "B",
                        jogador_ponto_b
                    )

                    st.rerun()

            st.divider()

            # ==============================================
            # PLACAR DOS SETS
            # ==============================================

            st.subheader("📊 Placar dos sets")

            st.write(
                f"**{st.session_state.equipe_a}: "
                f"{st.session_state.sets_a} sets**"
            )

            st.write(
                f"**{st.session_state.equipe_b}: "
                f"{st.session_state.sets_b} sets**"
            )

            if st.session_state.resultados_sets:

                for resultado in st.session_state.resultados_sets:

                    vencedor_nome = (
                        st.session_state.equipe_a
                        if resultado["vencedor"] == "A"
                        else st.session_state.equipe_b
                    )

                    st.write(
                        f"🏐 **Set {resultado['set']}:** "
                        f"{st.session_state.equipe_a} "
                        f"{resultado['pontos_a']} × "
                        f"{resultado['pontos_b']} "
                        f"{st.session_state.equipe_b} "
                        f"— 🏆 {vencedor_nome}"
                    )

            st.divider()

            # ==============================================
            # OCORRÊNCIAS / CARTÕES
            # ==============================================

            with st.expander(
                "🟨🟥 Registrar ocorrência / cartão"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    equipe_ocorrencia = st.selectbox(
                        "Equipe",
                        ["A", "B"],
                        format_func=lambda x:
                        st.session_state.equipe_a
                        if x == "A"
                        else st.session_state.equipe_b,
                        key="equipe_ocorrencia"
                    )

                jogadores_ocorrencia = (
                    st.session_state.jogadores_a
                    if equipe_ocorrencia == "A"
                    else st.session_state.jogadores_b
                )

                nomes_ocorrencia = [
                    f"#{j['numero']} - {j['nome']}"
                    for j in jogadores_ocorrencia
                ]

                nomes_ocorrencia.append(
                    "Técnico"
                )

                with col2:

                    pessoa_ocorrencia = st.selectbox(
                        "Responsável",
                        nomes_ocorrencia,
                        key="pessoa_ocorrencia"
                    )

                tipo_ocorrencia = st.selectbox(
                    "Tipo de ocorrência",
                    [
                        "Advertência — cartão amarelo",
                        "Penalidade — cartão vermelho",
                        "Expulsão",
                        "Desqualificação",
                        "Atraso",
                        "Outra ocorrência"
                    ],
                    key="tipo_ocorrencia"
                )

                descricao_ocorrencia = st.text_input(
                    "Descrição",
                    placeholder="Ex.: reclamação com a arbitragem",
                    key="descricao_ocorrencia"
                )

                if st.button(
                    "📝 REGISTRAR OCORRÊNCIA",
                    use_container_width=True
                ):

                    registrar_ocorrencia(
                        equipe_ocorrencia,
                        pessoa_ocorrencia,
                        tipo_ocorrencia,
                        descricao_ocorrencia
                        if descricao_ocorrencia.strip()
                        else "Sem descrição."
                    )

                    # Penalidade com cartão vermelho:
                    # ponto para o adversário.

                    if (
                        tipo_ocorrencia
                        == "Penalidade — cartão vermelho"
                    ):

                        equipe_punida = equipe_ocorrencia

                        equipe_adversaria = (
                            "B"
                            if equipe_punida == "A"
                            else "A"
                        )

                        adicionar_ponto(
                            equipe_adversaria,
                            "Penalidade adversária"
                        )

                        st.warning(
                            "🟥 Penalidade registrada. "
                            "Um ponto foi atribuído à equipe adversária."
                        )

                    else:

                        st.success(
                            "✅ Ocorrência registrada."
                        )

                    st.rerun()

            st.divider()

            # ==============================================
            # OCORRÊNCIAS DO SET
            # ==============================================

            if st.session_state.ocorrencias:

                st.subheader(
                    "📝 Ocorrências registradas"
                )

                for ocorrencia in reversed(
                    st.session_state.ocorrencias
                ):

                    if (
                        ocorrencia["set"]
                        == st.session_state.set_atual
                    ):

                        st.write(
                            f"**Set {ocorrencia['set']} — "
                            f"{ocorrencia['equipe']} — "
                            f"{ocorrencia['pessoa']}**: "
                            f"{ocorrencia['tipo']} — "
                            f"{ocorrencia['descricao']}"
                        )

            st.divider()

            # ==============================================
            # CONFIRMAR SET
            # ==============================================

            if st.button(
                "✅ CONFIRMAR RESULTADO DO SET",
                use_container_width=True,
                type="primary"
            ):

                if finalizar_set():

                    st.rerun()

        # ==================================================
        # PARTIDA FINALIZADA
        # ==================================================

        else:

            st.success(
                "🏆 PARTIDA FINALIZADA!"
            )

            if st.session_state.sets_a == 3:

                vencedor = st.session_state.equipe_a

            else:

                vencedor = st.session_state.equipe_b

            st.header("🏆 Resultado final")

            st.markdown(
                f"## {st.session_state.equipe_a} "
                f"**{st.session_state.sets_a} × "
                f"{st.session_state.sets_b}** "
                f"{st.session_state.equipe_b}"
            )

            st.success(
                f"🏆 Vencedor: **{vencedor}**"
            )

            st.subheader(
                "📊 Resultado dos sets"
            )

            for resultado in st.session_state.resultados_sets:

                st.write(
                    f"🏐 **Set {resultado['set']}:** "
                    f"{st.session_state.equipe_a} "
                    f"{resultado['pontos_a']} × "
                    f"{resultado['pontos_b']} "
                    f"{st.session_state.equipe_b}"
                )

            st.divider()

            # ==============================================
            # CONFIRMAR PARTIDA
            # ==============================================

            if not st.session_state.partida_salva:

                if st.button(
                    "💾 CONFIRMAR PARTIDA",
                    use_container_width=True,
                    type="primary"
                ):

                    partida = {

                        "data": str(date.today()),

                        "equipe_a":
                            st.session_state.equipe_a,

                        "equipe_b":
                            st.session_state.equipe_b,

                        "tecnico_a":
                            st.session_state.tecnico_a,

                        "tecnico_b":
                            st.session_state.tecnico_b,

                        "arbitro":
                            st.session_state.arbitro,

                        "jogadores_a":
                            st.session_state.jogadores_a.copy(),

                        "jogadores_b":
                            st.session_state.jogadores_b.copy(),

                        "sets_a":
                            st.session_state.sets_a,

                        "sets_b":
                            st.session_state.sets_b,

                        "vencedor":
                            vencedor,

                        "resultados":
                            st.session_state.resultados_sets.copy(),

                        "ocorrencias":
                            st.session_state.ocorrencias.copy(),

                        "observacao":
                            ""
                    }

                    st.session_state.historico.append(
                        partida
                    )

                    st.session_state.partida_salva = True

                    st.success(
                        "✅ Partida salva no histórico!"
                    )

            else:

                st.success(
                    "📜 Esta partida já está salva no histórico."
                )

            st.divider()

            # ==============================================
            # NOVA PARTIDA
            # ==============================================

            st.subheader("🔄 Nova partida")

            if st.button(
                "🔄 ZERAR E CADASTRAR NOVA PARTIDA",
                use_container_width=True
            ):

                nova_partida()

                st.rerun()


# ==========================================================
# HISTÓRICO
# ==========================================================

elif pagina == "📜 Histórico":

    st.header("📜 Histórico das partidas")

    if not st.session_state.historico:

        st.info(
            "📭 Nenhuma partida foi registrada ainda."
        )

    else:

        opcoes = []

        for i, partida in enumerate(
            st.session_state.historico
        ):

            opcoes.append(
                f"{i + 1} — "
                f"{partida['equipe_a']} × "
                f"{partida['equipe_b']} "
                f"({partida['data']})"
            )

        partida_escolhida = st.selectbox(
            "Selecione uma partida",
            opcoes
        )

        indice = opcoes.index(
            partida_escolhida
        )

        partida = st.session_state.historico[
            indice
        ]

        st.divider()

        st.subheader(
            f"🏐 {partida['equipe_a']} "
            f"× "
            f"{partida['equipe_b']}"
        )

        st.write(
            f"📅 **Data:** {partida['data']}"
        )

        st.write(
            f"👨‍⚖️ **Árbitro:** "
            f"{partida['arbitro']}"
        )

        st.write(
            f"🏆 **Vencedor:** "
            f"{partida['vencedor']}"
        )

        st.divider()

        st.subheader(
            "📊 Resultado dos sets"
        )

        for resultado in partida["resultados"]:

            st.write(
                f"🏐 **Set {resultado['set']}:** "
                f"{partida['equipe_a']} "
                f"{resultado['pontos_a']} × "
                f"{resultado['pontos_b']} "
                f"{partida['equipe_b']}"
            )

        st.divider()

        st.subheader(
            "📝 Ocorrências e punições"
        )

        if not partida.get("ocorrencias"):

            st.info(
                "Nenhuma ocorrência registrada."
            )

        else:

            for ocorrencia in partida["ocorrencias"]:

                st.write(
                    f"**Set {ocorrencia['set']} — "
                    f"{ocorrencia['equipe']} — "
                    f"{ocorrencia['pessoa']}**"
                )

                st.write(
                    f"{ocorrencia['tipo']} — "
                    f"{ocorrencia['descricao']}"
                )

                st.divider()


# ==========================================================
# RELATÓRIO
# ==========================================================

elif pagina == "📄 Relatório":

    st.header("📄 Relatório da partida")

    st.info(
        "Selecione uma partida já registrada para "
        "visualizar e gerar o relatório em PDF."
    )

    if not st.session_state.historico:

        st.warning(
            "⚠️ Nenhuma partida disponível."
        )

    else:

        opcoes = []

        for i, partida in enumerate(
            st.session_state.historico
        ):

            opcoes.append(
                f"{i + 1} — "
                f"{partida['equipe_a']} × "
                f"{partida['equipe_b']} "
                f"({partida['data']})"
            )

        partida_escolhida = st.selectbox(
            "Escolha a partida",
            opcoes,
            key="relatorio_partida"
        )

        indice = opcoes.index(
            partida_escolhida
        )

        partida = st.session_state.historico[
            indice
        ]

        # --------------------------------------------------
        # RESUMO
        # --------------------------------------------------

        st.subheader("🏆 Resumo")

        st.markdown(
            f"## {partida['equipe_a']} "
            f"**{partida['sets_a']} × "
            f"{partida['sets_b']}** "
            f"{partida['equipe_b']}"
        )

        st.success(
            f"🏆 Vencedor: **{partida['vencedor']}**"
        )

        st.write(
            f"📅 Data: **{partida['data']}**"
        )

        st.write(
            f"👨‍⚖️ Árbitro: **{partida['arbitro']}**"
        )

        st.divider()

        # --------------------------------------------------
        # SETS
        # --------------------------------------------------

        st.subheader("📊 Sets")

        for resultado in partida["resultados"]:

            st.write(
                f"Set {resultado['set']}: "
                f"**{resultado['pontos_a']} × "
                f"{resultado['pontos_b']}**"
            )

        st.divider()

        # --------------------------------------------------
        # OCORRÊNCIAS
        # --------------------------------------------------

        st.subheader(
            "📝 Ocorrências e punições"
        )

        if not partida.get("ocorrencias"):

            st.write(
                "Nenhuma ocorrência registrada."
            )

        else:

            for ocorrencia in partida["ocorrencias"]:

                st.write(
                    f"Set {ocorrencia['set']} — "
                    f"{ocorrencia['equipe']} — "
                    f"{ocorrencia['pessoa']} — "
                    f"{ocorrencia['tipo']}"
                )

        st.divider()

        # --------------------------------------------------
        # GERAR PDF
        # --------------------------------------------------

        pdf = gerar_pdf(partida)

        nome_pdf = (
            f"relatorio_"
            f"{partida['equipe_a']}_"
            f"x_"
            f"{partida['equipe_b']}.pdf"
        )

        nome_pdf = (
            nome_pdf
            .replace(" ", "_")
            .replace("/", "-")
            .replace("\\", "-")
        )

        st.download_button(
            label="📥 BAIXAR RELATÓRIO EM PDF",
            data=pdf,
            file_name=nome_pdf,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )