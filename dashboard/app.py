import streamlit as st
import duckdb
import altair as alt
from pathlib import Path


# ---------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------

st.set_page_config(
    page_title="Acidentes Rodoviários - PRF",
    page_icon="🚗",
    layout="wide"
)


# ---------------------------------------------------
# CAMINHO DO BANCO
# ---------------------------------------------------

CAMINHO_BANCO = Path("data/prf.duckdb")


# ---------------------------------------------------
# CONEXÃO COM DUCKDB
# ---------------------------------------------------

conexao = duckdb.connect(
    str(CAMINHO_BANCO),
    read_only=True
)


# ---------------------------------------------------
# TÍTULO
# ---------------------------------------------------

st.title("🚗 Acidentes Rodoviários - PRF")

st.caption(
    "Análise dos acidentes registrados nas rodovias federais "
    "entre 2022 e 2026."
)


# ---------------------------------------------------
# FILTROS
# ---------------------------------------------------

st.sidebar.header("Filtros")


anos = conexao.execute(
    """
    SELECT DISTINCT ano
    FROM acidentes
    ORDER BY ano
    """
).fetchdf()["ano"].tolist()


ufs = conexao.execute(
    """
    SELECT DISTINCT uf
    FROM acidentes
    ORDER BY uf
    """
).fetchdf()["uf"].tolist()


ano_selecionado = st.sidebar.selectbox(
    "Ano",
    ["Todos"] + anos
)


uf_selecionada = st.sidebar.selectbox(
    "UF",
    ["Todas"] + ufs
)


# ---------------------------------------------------
# FILTROS SQL
# ---------------------------------------------------

filtros = []
parametros = []


if ano_selecionado != "Todos":
    filtros.append("ano = ?")
    parametros.append(ano_selecionado)


if uf_selecionada != "Todas":
    filtros.append("uf = ?")
    parametros.append(uf_selecionada)


if filtros:
    where = "WHERE " + " AND ".join(filtros)
else:
    where = ""


# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

consulta_kpis = f"""
SELECT
    COUNT(*) AS acidentes,
    SUM(mortos) AS mortos,
    SUM(feridos) AS feridos,
    SUM(veiculos) AS veiculos
FROM acidentes
{where}
"""


kpis = conexao.execute(
    consulta_kpis,
    parametros
).fetchdf()


total_acidentes = int(kpis["acidentes"][0])
total_mortos = int(kpis["mortos"][0])
total_feridos = int(kpis["feridos"][0])
total_veiculos = int(kpis["veiculos"][0])


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Acidentes",
    f"{total_acidentes:,}".replace(",", ".")
)


col2.metric(
    "Mortos",
    f"{total_mortos:,}".replace(",", ".")
)


col3.metric(
    "Feridos",
    f"{total_feridos:,}".replace(",", ".")
)


col4.metric(
    "Veículos envolvidos",
    f"{total_veiculos:,}".replace(",", ".")
)


st.divider()


# ---------------------------------------------------
# AVISO SOBRE 2026
# ---------------------------------------------------

if ano_selecionado == 2026 or ano_selecionado == "Todos":

    st.info(
        "ℹ️ Os dados de 2026 são parciais. "
        "Por isso, o total desse ano não deve ser comparado "
        "diretamente com anos completos."
    )


# ---------------------------------------------------
# EVOLUÇÃO DOS ACIDENTES
# ---------------------------------------------------

st.subheader("📈 Evolução dos acidentes")


consulta_ano = f"""
SELECT
    ano,
    COUNT(*) AS total_acidentes
FROM acidentes
{where}
GROUP BY ano
ORDER BY ano
"""


df_ano = conexao.execute(
    consulta_ano,
    parametros
).fetchdf()


if ano_selecionado == "Todos":

    grafico_ano = alt.Chart(
        df_ano
    ).mark_line(
        point=True
    ).encode(

        x=alt.X(
            "ano:O",
            title="Ano"
        ),

        y=alt.Y(
            "total_acidentes:Q",
            title="Total de acidentes"
        ),

        tooltip=[
            alt.Tooltip(
                "ano:O",
                title="Ano"
            ),
            alt.Tooltip(
                "total_acidentes:Q",
                title="Acidentes",
                format=","
            )
        ]
    ).properties(
        height=350
    )

else:

    grafico_ano = alt.Chart(
        df_ano
    ).mark_bar().encode(

        x=alt.X(
            "ano:O",
            title="Ano"
        ),

        y=alt.Y(
            "total_acidentes:Q",
            title="Total de acidentes"
        ),

        tooltip=[
            alt.Tooltip(
                "ano:O",
                title="Ano"
            ),
            alt.Tooltip(
                "total_acidentes:Q",
                title="Acidentes",
                format=","
            )
        ]
    ).properties(
        height=350
    )


st.altair_chart(
    grafico_ano,
    use_container_width=True
)


st.divider()


# ---------------------------------------------------
# ACIDENTES POR UF E TOP BRs
# ---------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------
# ACIDENTES POR UF
# ---------------------------------------------------

with col1:

    st.subheader("🗺️ Acidentes por UF")

    consulta_uf = f"""
    SELECT
        uf,
        COUNT(*) AS total_acidentes
    FROM acidentes
    {where}
    GROUP BY uf
    ORDER BY total_acidentes DESC
    """


    df_uf = conexao.execute(
        consulta_uf,
        parametros
    ).fetchdf()


    grafico_uf = alt.Chart(
        df_uf
    ).mark_bar().encode(

        x=alt.X(
            "total_acidentes:Q",
            title="Total de acidentes"
        ),

        y=alt.Y(
            "uf:N",
            sort="-x",
            title="UF"
        ),

        tooltip=[
            alt.Tooltip(
                "uf:N",
                title="UF"
            ),
            alt.Tooltip(
                "total_acidentes:Q",
                title="Acidentes",
                format=","
            )
        ]
    ).properties(
        height=600
    )


    st.altair_chart(
        grafico_uf,
        use_container_width=True
    )


# ---------------------------------------------------
# BRs COM MAIS ACIDENTES
# ---------------------------------------------------

with col2:

    st.subheader("🛣️ BRs com mais acidentes")

    consulta_br = f"""
    SELECT
        br,
        COUNT(*) AS total_acidentes
    FROM acidentes
    {where}
    GROUP BY br
    ORDER BY total_acidentes DESC
    LIMIT 10
    """


    df_br = conexao.execute(
        consulta_br,
        parametros
    ).fetchdf()


    df_br["br"] = (
        "BR-"
        + df_br["br"].astype(int).astype(str)
    )


    grafico_br = alt.Chart(
        df_br
    ).mark_bar().encode(

        x=alt.X(
            "total_acidentes:Q",
            title="Total de acidentes"
        ),

        y=alt.Y(
            "br:N",
            sort="-x",
            title="BR"
        ),

        tooltip=[
            alt.Tooltip(
                "br:N",
                title="BR"
            ),
            alt.Tooltip(
                "total_acidentes:Q",
                title="Acidentes",
                format=","
            )
        ]
    ).properties(
        height=400
    )


    st.altair_chart(
        grafico_br,
        use_container_width=True
    )


st.divider()


# ---------------------------------------------------
# PRINCIPAIS CAUSAS
# ---------------------------------------------------

st.subheader("⚠️ Principais causas de acidentes")


consulta_causas = f"""
SELECT
    causa_acidente,
    COUNT(*) AS total_acidentes
FROM acidentes
{where}
GROUP BY causa_acidente
ORDER BY total_acidentes DESC
LIMIT 10
"""


df_causas = conexao.execute(
    consulta_causas,
    parametros
).fetchdf()


grafico_causas = alt.Chart(
    df_causas
).mark_bar().encode(

    x=alt.X(
        "total_acidentes:Q",
        title="Total de acidentes"
    ),

    y=alt.Y(
        "causa_acidente:N",
        sort="-x",
        title="Causa do acidente"
    ),

    tooltip=[
        alt.Tooltip(
            "causa_acidente:N",
            title="Causa"
        ),
        alt.Tooltip(
            "total_acidentes:Q",
            title="Acidentes",
            format=","
        )
    ]
).properties(
    height=400
)


st.altair_chart(
    grafico_causas,
    use_container_width=True
)


st.divider()


# ---------------------------------------------------
# CLASSIFICAÇÃO E TIPOS
# ---------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------
# CLASSIFICAÇÃO DOS ACIDENTES
# ---------------------------------------------------

with col1:

    st.subheader("📊 Classificação dos acidentes")

    consulta_classificacao = f"""
    SELECT
        classificacao_acidente,
        COUNT(*) AS total_acidentes
    FROM acidentes
    {where}
    GROUP BY classificacao_acidente
    ORDER BY total_acidentes DESC
    """


    df_classificacao = conexao.execute(
        consulta_classificacao,
        parametros
    ).fetchdf()


    grafico_classificacao = alt.Chart(
        df_classificacao
    ).mark_bar().encode(

        x=alt.X(
            "total_acidentes:Q",
            title="Total de acidentes"
        ),

        y=alt.Y(
            "classificacao_acidente:N",
            sort="-x",
            title="Classificação"
        ),

        tooltip=[
            alt.Tooltip(
                "classificacao_acidente:N",
                title="Classificação"
            ),
            alt.Tooltip(
                "total_acidentes:Q",
                title="Acidentes",
                format=","
            )
        ]
    ).properties(
        height=300
    )


    st.altair_chart(
        grafico_classificacao,
        use_container_width=True
    )


# ---------------------------------------------------
# TIPOS DE ACIDENTES
# ---------------------------------------------------

with col2:

    st.subheader("🚘 Tipos de acidentes")

    consulta_tipos = f"""
    SELECT
        tipo_acidente,
        COUNT(*) AS total_acidentes
    FROM acidentes
    {where}
    GROUP BY tipo_acidente
    ORDER BY total_acidentes DESC
    LIMIT 10
    """


    df_tipos = conexao.execute(
        consulta_tipos,
        parametros
    ).fetchdf()


    grafico_tipos = alt.Chart(
        df_tipos
    ).mark_bar().encode(

        x=alt.X(
            "total_acidentes:Q",
            title="Total de acidentes"
        ),

        y=alt.Y(
            "tipo_acidente:N",
            sort="-x",
            title="Tipo de acidente"
        ),

        tooltip=[
            alt.Tooltip(
                "tipo_acidente:N",
                title="Tipo"
            ),
            alt.Tooltip(
                "total_acidentes:Q",
                title="Acidentes",
                format=","
            )
        ]
    ).properties(
        height=400
    )


    st.altair_chart(
        grafico_tipos,
        use_container_width=True
    )


st.divider()


# ---------------------------------------------------
# RESUMO POR ANO
# ---------------------------------------------------

st.subheader("📋 Resumo por ano")


consulta_resumo = f"""
SELECT
    ano,
    COUNT(*) AS acidentes,
    SUM(mortos) AS mortos,
    SUM(feridos) AS feridos,
    SUM(veiculos) AS veiculos
FROM acidentes
{where}
GROUP BY ano
ORDER BY ano
"""


df_resumo = conexao.execute(
    consulta_resumo,
    parametros
).fetchdf()


st.dataframe(
    df_resumo,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------
# RODAPÉ
# ---------------------------------------------------

st.divider()


st.caption(
    "Fonte: Polícia Rodoviária Federal (PRF) | "
    "Projeto de Engenharia de Dados"
)


# ---------------------------------------------------
# FECHA A CONEXÃO
# ---------------------------------------------------

conexao.close()