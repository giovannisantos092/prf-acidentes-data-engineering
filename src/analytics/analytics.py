import pandas as pd
from pathlib import Path


CAMINHO_PARQUET = Path(
    "data/processed/prf_2022_2026.parquet"
)

PASTA_ANALYTICS = Path(
    "data/analytics"
)


def carregar_base():
    """
    Carrega a base processada da PRF.
    """

    return pd.read_parquet(CAMINHO_PARQUET)


def acidentes_por_uf(df):
    """
    Calcula a quantidade de acidentes por UF.
    """

    return (
        df.groupby("uf")
        .size()
        .reset_index(name="quantidade_acidentes")
        .sort_values(
            "quantidade_acidentes",
            ascending=False
        )
    )


def acidentes_por_ano(df):
    """
    Calcula a quantidade de acidentes por ano.
    """

    return (
        df.groupby(
            df["data_inversa"].dt.year
        )
        .size()
        .reset_index(name="quantidade_acidentes")
        .rename(
            columns={
                "data_inversa": "ano"
            }
        )
        .sort_values("ano")
    )


def acidentes_por_br(df):
    """
    Calcula a quantidade de acidentes por BR.
    """

    return (
        df.groupby("br")
        .size()
        .reset_index(name="quantidade_acidentes")
        .sort_values(
            "quantidade_acidentes",
            ascending=False
        )
    )


def acidentes_por_classificacao(df):
    """
    Calcula os acidentes por classificação.
    """

    return (
        df.groupby("classificacao_acidente")
        .size()
        .reset_index(name="quantidade_acidentes")
        .sort_values(
            "quantidade_acidentes",
            ascending=False
        )
    )


def salvar_camadas_analiticas(df):
    """
    Gera e salva as tabelas analíticas em Parquet.
    """

    PASTA_ANALYTICS.mkdir(
        parents=True,
        exist_ok=True
    )

    tabelas = {
        "acidentes_por_uf": acidentes_por_uf(df),
        "acidentes_por_ano": acidentes_por_ano(df),
        "acidentes_por_br": acidentes_por_br(df),
        "acidentes_por_classificacao":
            acidentes_por_classificacao(df)
    }

    for nome, tabela in tabelas.items():

        caminho = (
            PASTA_ANALYTICS /
            f"{nome}.parquet"
        )

        tabela.to_parquet(
            caminho,
            index=False
        )

        print(
            f"{nome} salvo -> {caminho}"
        )


if __name__ == "__main__":

    print(
        "Carregando base processada...\n"
    )

    df_prf = carregar_base()

    print(
        f"Registros carregados: "
        f"{len(df_prf):,}\n"
    )

    salvar_camadas_analiticas(df_prf)

    print(
        "\nCamada analítica criada com sucesso."
    )