
# =====================================================
# PROJETO ZOONOSES — CCZ
# CAMADA BRONZE — VALIDAÇÃO INICIAL DOS ARQUIVOS
# =====================================================

from pathlib import Path
import csv
import json
import xml.etree.ElementTree as ET

FORMATOS_PERMITIDOS = {".csv", ".json", ".xml", ".txt"}


def validar_arquivo(caminho):

    arquivo = Path(caminho)

    if not arquivo.is_file():
        return False, "Arquivo não encontrado."

    if arquivo.suffix.lower() not in FORMATOS_PERMITIDOS:
        return False, "Formato não permitido."

    if arquivo.stat().st_size == 0:
        return False, "Arquivo vazio."

    try:
        formato = arquivo.suffix.lower()

        if formato == ".csv":
            with arquivo.open(
                "r", encoding="utf-8-sig", newline=""
            ) as f:
                leitor = csv.reader(f)
                cabecalho = next(leitor, None)

                if not cabecalho or not any(
                    coluna.strip() for coluna in cabecalho
                ):
                    return False, "CSV sem cabeçalho válido."

                for linha in leitor:
                    pass

        elif formato == ".json":
            with arquivo.open("r", encoding="utf-8-sig") as f:
                json.load(f)

        elif formato == ".xml":
            ET.parse(arquivo)

        elif formato == ".txt":
            with arquivo.open("r", encoding="utf-8-sig") as f:
                conteudo = f.read()

                if not conteudo.strip():
                    return False, "TXT sem conteúdo."

        return True, "Validação inicial concluída."

    except (
        UnicodeError,
        csv.Error,
        json.JSONDecodeError,
        ET.ParseError,
        OSError,
        ValueError
    ) as erro:
        return False, f"Erro de leitura: {erro}"


# EXECUÇÃO DO TESTE

if __name__ == "__main__":

    PASTA_PROJETO = Path(__file__).resolve().parent.parent
    PASTA_ENTRADA = PASTA_PROJETO / "dados" / "entrada"

    for arquivo in sorted(PASTA_ENTRADA.iterdir()):

        if arquivo.is_file():

            valido, mensagem = validar_arquivo(arquivo)

            situacao = "VÁLIDO" if valido else "INVÁLIDO"

            print(f"{arquivo.name}: {situacao}")
            print(f"Motivo: {mensagem}")
            print("-" * 50)
