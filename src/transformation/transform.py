import pandas as pd


def limpar_dados(df):
    """
    Aplica as transformações de limpeza e padronização
    em uma base da PRF.
    """

    df = df.copy()

    # Tratamento dos valores nulos
    df["classificacao_acidente"] = (
        df["classificacao_acidente"]
        .fillna("Não informado")
    )

    colunas_administrativas = [
        "regional",
        "delegacia",
        "uop"
    ]

    df[colunas_administrativas] = (
        df[colunas_administrativas]
        .fillna("Não informado")
    )

    # Padronização do ID
    df["id"] = df["id"].astype("Int64")

    # Conversão da data
    df["data_inversa"] = pd.to_datetime(
        df["data_inversa"],
        errors="coerce"
    )

    # Conversão do KM
    df["km"] = (
        df["km"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    df["km"] = pd.to_numeric(
        df["km"],
        errors="coerce"
    )

    # Conversão de latitude e longitude
    for coluna in ["latitude", "longitude"]:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    return df


def transformar_dados(bases):
    """
    Recebe as bases extraídas, aplica a limpeza
    em cada uma e cria uma única base consolidada.
    """

    bases_processadas = []

    for ano, df_ano in bases.items():

        df_ano = limpar_dados(df_ano)

        bases_processadas.append(df_ano)

        print(
            f"{ano} processado -> "
            f"{df_ano.shape[0]} linhas e "
            f"{df_ano.shape[1]} colunas"
        )

    # União das bases
    df_prf = pd.concat(
        bases_processadas,
        ignore_index=True
    )

    print("\nTransformação concluída.")

    print(
        f"Base unificada -> "
        f"{df_prf.shape[0]} linhas e "
        f"{df_prf.shape[1]} colunas"
    )

    return df_prf


if __name__ == "__main__":

    from src.extraction.extract import extrair_dados

    print("Iniciando extração...\n")

    bases = extrair_dados()

    print("\nIniciando transformação...\n")

    df_prf = transformar_dados(bases)

    print("\nTipos das principais colunas:")

    print(
        df_prf[
            [
                "id",
                "data_inversa",
                "km",
                "latitude",
                "longitude"
            ]
        ].dtypes
    )

    print("\nPrimeiros registros:")

    print(df_prf.head())