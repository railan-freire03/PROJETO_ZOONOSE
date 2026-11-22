
# ============================================================
# PROJETO ZOONOSES — ENGENHARIA DE DADOS CCZ
# CAMADA BRONZE — INGESTÃO DE DADOS BRUTOS
# ============================================================

from pathlib import Path
from datetime import datetime
import shutil

from validacao import validar_arquivo
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auditoria.registro_auditoria import registrar_auditoria


# 1. CAMINHOS DO PROJETO

PASTA_PROJETO = Path(__file__).resolve().parent.parent

PASTA_ENTRADA = PASTA_PROJETO / "dados" / "entrada"
PASTA_BRONZE = PASTA_PROJETO / "dados" / "bronze"


# 2. FUNÇÃO DE INGESTÃO

def executar_ingestao():

    PASTA_ENTRADA.mkdir(parents=True, exist_ok=True)
    PASTA_BRONZE.mkdir(parents=True, exist_ok=True)

    arquivos = sorted(
        arquivo
        for arquivo in PASTA_ENTRADA.iterdir()
        if arquivo.is_file()
    )

    if not arquivos:
        print("Nenhum arquivo encontrado na entrada.")
        return

    # Identificador único da execução
    id_lote = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    pasta_lote = PASTA_BRONZE / id_lote
    pasta_lote.mkdir(parents=True, exist_ok=True)

    total_validos = 0
    total_com_problemas = 0
    total_copiados = 0

    print("=" * 55)
    print("INGESTÃO DE DADOS BRUTOS — CAMADA BRONZE")
    print("=" * 55)

    for arquivo in arquivos:

        # Verifica o arquivo, mas não impede sua preservação.
        valido, mensagem = validar_arquivo(arquivo)

        destino = pasta_lote / arquivo.name

        try:
            # Preserva uma cópia do arquivo original.
            shutil.copy2(arquivo, destino)
            total_copiados += 1

        except OSError as erro:
            print(f"[ERRO DE CÓPIA] {arquivo.name}: {erro}")
            continue

        
        if valido:
            total_validos += 1
            situacao = "VALIDO"
            print(f"[VÁLIDO] {arquivo.name}")

        else:
            total_com_problemas += 1
            situacao = "COM_PROBLEMAS"
            print(f"[COM PROBLEMAS] {arquivo.name}")
            print(f"Motivo: {mensagem}")

        registrar_auditoria(
            id_lote=id_lote,
            arquivo=arquivo.name,
            situacao=situacao,
            motivo=mensagem
        )

    print("-" * 55)
    print(f"Arquivos armazenados: {total_copiados}")
    print(f"Arquivos válidos: {total_validos}")
    print(f"Arquivos com problemas: {total_com_problemas}")
    print(f"Lote criado: {id_lote}")
    print("Ingestão finalizada.")


# 3. EXECUÇÃO

if __name__ == "__main__":
    executar_ingestao()
