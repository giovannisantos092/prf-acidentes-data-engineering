import duckdb
from pathlib import Path


CAMINHO_PARQUET = Path(
    "data/processed/prf_2022_2026.parquet"
)

CAMINHO_BANCO = Path(
    "data/prf.duckdb"
)


def criar_banco():
    print("Criando banco DuckDB...")

    conexao = duckdb.connect(
        str(CAMINHO_BANCO)
    )

    conexao.execute(
        f"""
        CREATE OR REPLACE VIEW acidentes AS

        SELECT *
        FROM read_parquet(
            '{CAMINHO_PARQUET.as_posix()}'
        );
        """
    )

    print(
        "View 'acidentes' criada com sucesso."
    )

    quantidade = conexao.execute(
        """
        SELECT COUNT(*)
        FROM acidentes;
        """
    ).fetchone()[0]

    print(
        f"Total de registros: {quantidade}"
    )

    conexao.close()


if __name__ == "__main__":
    criar_banco()