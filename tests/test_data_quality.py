import pandas as pd
from pathlib import Path


CAMINHO_PARQUET = Path(
    "data/processed/prf_2022_2026.parquet"
)


def carregar_dados():
    return pd.read_parquet(CAMINHO_PARQUET)


def test_arquivo_parquet_existe():
    assert CAMINHO_PARQUET.exists()


def test_base_nao_esta_vazia():
    df = carregar_dados()

    assert len(df) > 0


def test_id_nao_possui_nulos():
    df = carregar_dados()

    assert df["id"].isnull().sum() == 0


def test_id_nao_possui_duplicados():
    df = carregar_dados()

    assert df["id"].duplicated().sum() == 0


def test_colunas_principais_existem():
    df = carregar_dados()

    colunas_obrigatorias = [
        "id",
        "data_inversa",
        "uf",
        "br",
        "km",
        "latitude",
        "longitude",
    ]

    for coluna in colunas_obrigatorias:
        assert coluna in df.columns