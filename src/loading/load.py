from pathlib import Path


def salvar_dados(df):
    """
    Salva a base processada no formato Parquet.
    """

    pasta_saida = Path("data/processed")

    pasta_saida.mkdir(
        parents=True,
        exist_ok=True
    )

    caminho_saida = (
        pasta_saida / "prf_2022_2026.parquet"
    )

    df.to_parquet(
        caminho_saida,
        index=False
    )

    print(
        f"Base salva com sucesso em: "
        f"{caminho_saida}"
    )


if __name__ == "__main__":

    from src.extraction.extract import extrair_dados
    from src.transformation.transform import transformar_dados

    print("Iniciando extração...\n")

    bases = extrair_dados()

    print("\nIniciando transformação...\n")

    df_prf = transformar_dados(bases)

    print("\nIniciando carregamento...\n")

    salvar_dados(df_prf)

    print("\nPipeline concluído com sucesso.")