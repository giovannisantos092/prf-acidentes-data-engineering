import pandas as pd
from pathlib import Path


def extrair_dados():
    pasta_raw = Path("data/raw")

    arquivos = {
        2022: pasta_raw / "datatran2022.csv",
        2023: pasta_raw / "datatran2023.csv",
        2024: pasta_raw / "datatran2024.csv",
        2025: pasta_raw / "datatran2025.csv",
        2026: pasta_raw / "datatran2026.csv",
    }

    bases = {}

    for ano, caminho in arquivos.items():
        df = pd.read_csv(
            caminho,
            sep=";",
            encoding="latin1"
        )

        bases[ano] = df

        print(f"{ano}: {df.shape}")

    return bases


if __name__ == "__main__":
    from src.extraction.extract import extrair_dados

    bases = extrair_dados()
    df_prf = transformar_dados(bases)

    print(df_prf.head())