import pandas as pd


ARQUIVO_ENTRADA = "data/processed/prf_2022_2026.parquet"
ARQUIVO_SAIDA = "data/processed/prf_2022_2026_clean.parquet"


def transformar_dados():

    # Carrega os dados
    df = pd.read_parquet(ARQUIVO_ENTRADA)

    print("Arquivo carregado com sucesso.")
    print("Shape inicial:", df.shape)

    # Converte a coluna de data
    df["data_inversa"] = pd.to_datetime(
        df["data_inversa"],
        errors="coerce"
    )

    # Cria novas colunas de data
    df["ano"] = df["data_inversa"].dt.year
    df["mes"] = df["data_inversa"].dt.month
    df["dia"] = df["data_inversa"].dt.day

    print("Datas transformadas com sucesso.")

    # Padroniza colunas de texto
    colunas_texto = [
        "uf",
        "dia_semana",
        "municipio",
        "causa_acidente",
        "tipo_acidente",
        "classificacao_acidente",
        "fase_dia",
        "sentido_via",
        "condicao_metereologica",
        "tipo_pista",
        "tracado_via",
        "uso_solo"
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    print("Colunas de texto padronizadas.")

    # Verifica IDs duplicados
    duplicados = df["id"].duplicated().sum()

    print("IDs duplicados:", duplicados)

    # Verifica valores nulos
    nulos = df.isnull().sum().sum()

    print("Valores nulos:", nulos)

    # Verifica valores negativos
    colunas_numericas = [
        "pessoas",
        "mortos",
        "feridos_leves",
        "feridos_graves",
        "ilesos",
        "ignorados",
        "feridos",
        "veiculos"
    ]

    print("\nValores negativos:")

    for coluna in colunas_numericas:

        negativos = (df[coluna] < 0).sum()

        print(f"{coluna}: {negativos}")

    # Verifica consistência da coluna feridos
    soma_feridos = (
        df["feridos_leves"]
        + df["feridos_graves"]
    )

    inconsistencias_feridos = (
        soma_feridos != df["feridos"]
    ).sum()

    print(
        "\nInconsistências em feridos:",
        inconsistencias_feridos
    )

    # Salva os dados transformados
    df.to_parquet(
        ARQUIVO_SAIDA,
        index=False
    )

    print("\nArquivo transformado salvo com sucesso.")
    print("Shape final:", df.shape)


if __name__ == "__main__":
    transformar_dados()