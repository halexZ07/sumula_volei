import streamlit as st
from datetime import date


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
# VERIFICAR VENCEDOR DO SET
# ==========================================================

def verificar_vencedor_set():

    # TODOS os sets vão até 25 pontos
    # Não existe vantagem de 2 pontos

    limite = 25

    pontos_a = st.session_state.pontos_a
    pontos_b = st.session_state.pontos_b

    if pontos_a >= limite:
        return "A"

    if pontos_b >= limite:
        return "B"

    return None


# ==========================================================
# FINALIZAR SET
# ==========================================================

def finalizar_set():

    vencedor = verificar_vencedor_set()

    if vencedor is None:

        st.warning(
            "O set ainda não terminou. "
            "É necessário chegar a 25 pontos."
        )

        return

    # Salva o resultado do set

    resultado = {
        "set": st.session_state.set_atual,
        "pontos_a": st.session_state.pontos_a,
        "pontos_b": st.session_state.pontos_b,
        "vencedor": vencedor
    }

    st.session_state.resultados_sets.append(resultado)

    # Adiciona o set para a equipe vencedora

    if vencedor == "A":
        st.session_state.sets_a += 1
    else:
        st.session_state.sets_b += 1

    # Verifica se alguém já ganhou 3 sets

    if (
        st.session_state.sets_a == 3
        or st.session_state.sets_b == 3
    ):

        st.session_state.partida_finalizada = True

    else:

        # Vai para o próximo set

        st.session_state.set_atual += 1

        st.session_state.pontos_a = 0
        st.session_state.pontos_b = 0


# ==========================================================
# TÍTULO PRINCIPAL
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
            "📜 Histórico"
        ]
    )

    st.divider()

    st.caption("Regras da partida")

    st.write("🏆 Melhor de 5 sets")
    st.write("🏐 Todos os sets: 25 pontos")
    st.write("🏆 3 sets vencidos = vitória")
    


# ==========================================================
# PÁGINA DE CADASTRO
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


    # ======================================================
    # TITULARES EQUIPE 1
    # ======================================================

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


    # ======================================================
    # RESERVAS EQUIPE 1
    # ======================================================

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


    # ======================================================
    # TITULARES EQUIPE 2
    # ======================================================

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


    # ======================================================
    # RESERVAS EQUIPE 2
    # ======================================================

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
    # SALVAR CADASTRO
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
# PÁGINA DA PARTIDA
# ==========================================================

elif pagina == "🏐 Partida":

    st.header("🏐 Partida")


    if not st.session_state.cadastro_salvo:

        st.warning(
            "⚠️ Primeiro faça o cadastro das equipes."
        )


    else:

        # ==================================================
        # INFORMAÇÕES DAS EQUIPES
        # ==================================================

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


        # --------------------------------------------------
        # EQUIPE 1
        # --------------------------------------------------

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


        # --------------------------------------------------
        # EQUIPE 2
        # --------------------------------------------------

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

            st.subheader(
                f"🏆 SET {st.session_state.set_atual}"
            )

            st.info(
                "🏐 SET — vence quem chegar a 25 pontos."
            )


            # ==================================================
            # PLACAR
            # ==================================================

            col1, col2 = st.columns(2)


            # --------------------------------------------------
            # EQUIPE 1
            # --------------------------------------------------

            with col1:

                st.markdown(
                    f"# {st.session_state.equipe_a}"
                )

                st.metric(
                    "PONTOS",
                    st.session_state.pontos_a
                )

                if st.button(
                    "➕ PONTO",
                    key="ponto_a",
                    use_container_width=True
                ):

                    st.session_state.pontos_a += 1

                    st.rerun()


            # --------------------------------------------------
            # EQUIPE 2
            # --------------------------------------------------

            with col2:

                st.markdown(
                    f"# {st.session_state.equipe_b}"
                )

                st.metric(
                    "PONTOS",
                    st.session_state.pontos_b
                )

                if st.button(
                    "➕ PONTO",
                    key="ponto_b",
                    use_container_width=True
                ):

                    st.session_state.pontos_b += 1

                    st.rerun()


            st.divider()


            # ==================================================
            # PLACAR DOS SETS
            # ==================================================

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


            # ==================================================
            # CONFIRMAR SET
            # ==================================================

            if st.button(
                "✅ CONFIRMAR RESULTADO DO SET",
                use_container_width=True,
                type="primary"
            ):

                finalizar_set()

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


            # ==================================================
            # RESULTADOS DOS SETS
            # ==================================================

            st.subheader("📊 Resultado dos sets")

            for resultado in st.session_state.resultados_sets:

                st.write(
                    f"🏐 **Set {resultado['set']}:** "
                    f"{st.session_state.equipe_a} "
                    f"{resultado['pontos_a']} × "
                    f"{resultado['pontos_b']} "
                    f"{st.session_state.equipe_b}"
                )


            st.divider()


            # ==================================================
            # CONFIRMAR PARTIDA
            # ==================================================

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
                            st.session_state.resultados_sets.copy()
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


            # ==================================================
            # NOVA PARTIDA
            # ==================================================

            st.subheader("🔄 Nova partida")

            st.write(
                "Comece um novo cadastro sem apagar "
                "as partidas do histórico."
            )


            if st.button(
                "🔄 ZERAR E CADASTRAR NOVA PARTIDA",
                use_container_width=True
            ):

                nova_partida()

                st.rerun()


# ==========================================================
# PÁGINA DO HISTÓRICO
# ==========================================================

elif pagina == "📜 Histórico":

    st.header("📜 Histórico das partidas")


    if not st.session_state.historico:

        st.info(
            "📭 Nenhuma partida foi registrada ainda."
        )


    else:

        # ==================================================
        # SELECIONAR PARTIDA
        # ==================================================

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


        # ==================================================
        # INFORMAÇÕES DA PARTIDA
        # ==================================================

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


        # ==================================================
        # TÉCNICOS
        # ==================================================

        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                f"### 🏐 {partida['equipe_a']}"
            )

            st.write(
                f"**Técnico:** "
                f"{partida['tecnico_a']}"
            )


        with col2:

            st.markdown(
                f"### 🏐 {partida['equipe_b']}"
            )

            st.write(
                f"**Técnico:** "
                f"{partida['tecnico_b']}"
            )


        st.divider()


        # ==================================================
        # JOGADORES DO HISTÓRICO
        # ==================================================

        st.subheader(
            "👥 Jogadores da partida"
        )

        col1, col2 = st.columns(2)


        # --------------------------------------------------
        # EQUIPE 1
        # --------------------------------------------------

        with col1:

            st.markdown(
                f"### 🏐 {partida['equipe_a']}"
            )

            st.write("**Titulares:**")

            for jogador in partida["jogadores_a"]:

                if jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )


            st.write("**Reservas:**")

            for jogador in partida["jogadores_a"]:

                if not jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )


        # --------------------------------------------------
        # EQUIPE 2
        # --------------------------------------------------

        with col2:

            st.markdown(
                f"### 🏐 {partida['equipe_b']}"
            )

            st.write("**Titulares:**")

            for jogador in partida["jogadores_b"]:

                if jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )


            st.write("**Reservas:**")

            for jogador in partida["jogadores_b"]:

                if not jogador["titular"]:

                    st.write(
                        f"#{jogador['numero']} — "
                        f"{jogador['nome']}"
                    )


        st.divider()


        # ==================================================
        # RESULTADO FINAL
        # ==================================================

        st.header("🏆 Resultado")

        st.markdown(
            f"## {partida['equipe_a']} "
            f"**{partida['sets_a']} × "
            f"{partida['sets_b']}** "
            f"{partida['equipe_b']}"
        )


        st.success(
            f"🏆 Vencedor: **{partida['vencedor']}**"
        )


        # ==================================================
        # RESULTADO DOS SETS
        # ==================================================

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