import sys
import duckdb
from pathlib import Path


CAMINHO_BANCO = Path("data/prf.duckdb")


def executar_sql(caminho_sql):
    caminho_sql = Path(caminho_sql)

    if not caminho_sql.exists():
        print(f"Arquivo SQL não encontrado: {caminho_sql}")
        return

    conexao = duckdb.connect(
        str(CAMINHO_BANCO)
    )

    consulta = caminho_sql.read_text(
        encoding="utf-8"
    )

    resultado = conexao.execute(
        consulta
    ).fetchdf()

    print(resultado)

    conexao.close()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            "Uso: python -m src.database.run_sql "
            "caminho_do_arquivo.sql"
        )
    else:
        executar_sql(sys.argv[1])