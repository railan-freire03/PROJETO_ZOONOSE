
# =====================================================
# PROJETO ZOONOSES — CCZ
# CAMADA PRATA — TRATAMENTO INICIAL DO CSV
# =====================================================

from pathlib import Path
import pandas as pd

from padronizacao import padronizar_texto, padronizar_data
from anonimizacao import anonimizar_cpf
from deduplicacao import identificar_duplicidades

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auditoria.qualidade_dados import verificar_qualidade


# 1. CAMINHOS

PASTA_PROJETO = Path(__file__).resolve().parent.parent

PASTA_BRONZE = PASTA_PROJETO / "dados" / "bronze"
PASTA_PRATA = PASTA_PROJETO / "dados" / "prata"

NOME_ARQUIVO = "atendimentos_teste.csv"


# 2. LOCALIZAR O CSV NA BRONZE

def localizar_arquivo():

    arquivos = list(
        PASTA_BRONZE.glob(f"*/{NOME_ARQUIVO}")
    )

    if not arquivos:
        raise FileNotFoundError(
            "Arquivo CSV não encontrado na Bronze."
        )

    # Seleciona o arquivo do lote mais recente.
    return sorted(arquivos)[-1]


# 3. TRATAMENTO

def executar_tratamento():

    caminho_arquivo = localizar_arquivo()

    print("Arquivo encontrado:", caminho_arquivo.name)

    # Leitura do arquivo bruto
    df = pd.read_csv(
        caminho_arquivo,
        dtype=str,
        encoding="utf-8-sig"
    )

    # IDENTIFICADOR TÉCNICO DE ORIGEM

    df["id_registro_origem"] = range(1, len(df) + 1)

    print("Identificadores de origem gerados.")


    print("Registros recebidos:", len(df))

    # Colunas de texto que serão padronizadas
    colunas_texto = [
        "bairro",
        "especie",
        "tipo_servico"
    ]

    for coluna in colunas_texto:

        if coluna in df.columns:
            df[coluna] = df[coluna].apply(
                padronizar_texto
            )

    # Padronização das datas
    if "data_evento" in df.columns:
        df["data_evento"] = df["data_evento"].apply(
            padronizar_data
        )

    # Criação da pasta Prata
    PASTA_PRATA.mkdir(parents=True, exist_ok=True)

    
    # PSEUDONIMIZAÇÃO DOS CPFs

    if "cpf" not in df.columns:
        raise ValueError("Coluna CPF não encontrada.")

    df["id_cidadao_hash"] = df["cpf"].apply(
        anonimizar_cpf
    )

    # REMOÇÃO DOS DADOS PESSOAIS DIRETOS

    colunas_sensiveis = [
        "nome",
        "cpf"
    ]

    df = df.drop(
        columns=colunas_sensiveis,
        errors="ignore"
    )

    print("Identificadores gerados.")
    print("Nome e CPF removidos dos dados tratados.")


    # 4. VERIFICAÇÃO DE QUALIDADE

    dados_completos, dados_revisao = verificar_qualidade(df)

    # IDENTIFICAÇÃO DE DUPLICIDADES

    dados_unicos, dados_duplicados, revisao_chaves = (
        identificar_duplicidades(dados_completos)
    )

    # Reúne os registros que precisam de revisão.
    dados_revisao = pd.concat(
        [dados_revisao, revisao_chaves],
        ignore_index=True
    )

    # VERIFICAÇÃO AUTOMÁTICA DE INTEGRIDADE

    total_recebidos = len(df)

    total_classificados = (
        len(dados_unicos)
        + len(dados_revisao)
        + len(dados_duplicados)
    )

    print("=" * 50)
    print("VERIFICAÇÃO DE INTEGRIDADE")
    print("=" * 50)

    print(f"Registros recebidos: {total_recebidos}")
    print(f"Registros classificados: {total_classificados}")

    if total_recebidos != total_classificados:
        raise ValueError(
            "Falha de integridade: quantidade de registros diferente."
        )

    print("Integridade dos registros: OK")

    # VERIFICAR SOBREPOSIÇÃO ENTRE OS GRUPOS

    todos_ids = pd.concat(
        [
            dados_unicos["id_registro_origem"],
            dados_revisao["id_registro_origem"],
            dados_duplicados["id_registro_origem"]
        ],
        ignore_index=True
    )

    ids_repetidos = todos_ids.duplicated().sum()

    print("-" * 50)
    print("VERIFICAÇÃO DE RASTREABILIDADE")
    print(f"Registros presentes em mais de um grupo: {ids_repetidos}")

    if ids_repetidos > 0:
        raise ValueError(
            "Falha de rastreabilidade: registros classificados "
            "mais de uma vez."
        )

    print("Rastreabilidade dos registros: OK")



    # 5. CRIAÇÃO DA PASTA PRATA

    PASTA_PRATA.mkdir(parents=True, exist_ok=True)

    # 6. SALVAR REGISTROS COMPLETOS

    caminho_completos = (
        PASTA_PRATA / "atendimentos_completos.csv"
    )

    dados_unicos.to_csv(
       caminho_completos,
       index=False,
       encoding="utf-8-sig"
    )

    # 7. SALVAR REGISTROS PARA REVISÃO

    caminho_revisao = (
        PASTA_PRATA / "atendimentos_revisao.csv"
    )

    dados_revisao.to_csv(
        caminho_revisao,
        index=False,
        encoding="utf-8-sig"
    )

    print("-" * 50)
    print("Arquivos gerados:")
    print(caminho_completos)
    print(caminho_revisao)
    print("Verificação de qualidade finalizada.")

    # SALVAR DUPLICIDADES IDENTIFICADAS

    caminho_duplicados = (
        PASTA_PRATA / "atendimentos_duplicados.csv"
    )

    dados_duplicados.to_csv(
        caminho_duplicados,
        index=False,
        encoding="utf-8-sig"
    )

    print("Arquivo de duplicidades:", caminho_duplicados)

if __name__ == "__main__":
    executar_tratamento()
