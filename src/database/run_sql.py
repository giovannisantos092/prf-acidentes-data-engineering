import sys
import duckdb
from pathlib import Path


CAMINHO_BANCO = Path("data/prf.duckdb")
PASTA_ANALYTICS = Path("data/analytics")


def executar_sql(caminho_sql):
    caminho_sql = Path(caminho_sql)

    if not caminho_sql.exists():
        print(f"Arquivo SQL não encontrado: {caminho_sql}")
        return

    if not CAMINHO_BANCO.exists():
        print(f"Banco DuckDB não encontrado: {CAMINHO_BANCO}")
        return

    PASTA_ANALYTICS.mkdir(
        parents=True,
        exist_ok=True
    )

    conexao = duckdb.connect(
        str(CAMINHO_BANCO)
    )

    try:
        consulta = caminho_sql.read_text(
            encoding="utf-8"
        )

        resultado = conexao.execute(
            consulta
        ).fetchdf()

        print(
            f"\nConsulta executada: {caminho_sql.name}\n"
        )

        print(resultado)

        nome_arquivo = caminho_sql.stem

        caminho_csv = (
            PASTA_ANALYTICS
            / f"{nome_arquivo}.csv"
        )

        caminho_parquet = (
            PASTA_ANALYTICS
            / f"{nome_arquivo}.parquet"
        )

        resultado.to_csv(
            caminho_csv,
            index=False,
            encoding="utf-8"
        )

        resultado.to_parquet(
            caminho_parquet,
            index=False
        )

        print(
            f"\nCSV salvo em: {caminho_csv}"
        )

        print(
            f"Parquet salvo em: {caminho_parquet}"
        )

    finally:
        conexao.close()


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Uso: python -m src.database.run_sql "
            "caminho_do_arquivo.sql"
        )

    else:

        executar_sql(
            sys.argv[1]
        )