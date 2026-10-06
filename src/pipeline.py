from src.extraction.extract import extrair_dados
from src.transformation.transform import transformar_dados
from src.loading.load import salvar_dados


def executar_pipeline():
    print("Iniciando pipeline ETL...\n")

    print("1. Extraindo dados...")
    bases = extrair_dados()

    print("\n2. Transformando dados...")
    df_prf = transformar_dados(bases)

    print("\n3. Salvando dados...")
    salvar_dados(df_prf)

    print("\nPipeline ETL concluído com sucesso.")


if __name__ == "__main__":
    executar_pipeline()