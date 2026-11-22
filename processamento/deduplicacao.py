
# =====================================================
# PROJETO ZOONOSES — CCZ
# CAMADA PRATA — IDENTIFICAÇÃO DE DUPLICIDADES
# =====================================================

import pandas as pd


COLUNAS_CHAVE = [
    "id_cidadao_hash",
    "data_evento",
    "tipo_servico",
    "especie"
]


def identificar_duplicidades(df):

    dados = df.copy()

    # Verificar se todas as colunas necessárias existem.
    ausentes = [
        coluna
        for coluna in COLUNAS_CHAVE
        if coluna not in dados.columns
    ]

    if ausentes:
        raise ValueError(
            f"Colunas necessárias ausentes: {ausentes}"
        )

    # Não deduplicar registros com chave incompleta.
    chave_incompleta = (
        dados[COLUNAS_CHAVE]
        .isna()
        .any(axis=1)
    )

    dados_revisao = dados.loc[chave_incompleta].copy()
    dados_analisaveis = dados.loc[~chave_incompleta].copy()

    # Identificar ocorrências repetidas.
    duplicados = dados_analisaveis.duplicated(
        subset=COLUNAS_CHAVE,
        keep="first"
    )

    dados_unicos = dados_analisaveis.loc[
        ~duplicados
    ].copy()

    dados_duplicados = dados_analisaveis.loc[
        duplicados
    ].copy()

    print("=" * 50)
    print("RELATÓRIO DE DUPLICIDADES")
    print("=" * 50)
    print(f"Registros recebidos: {len(dados)}")
    print(f"Registros únicos: {len(dados_unicos)}")
    print(f"Duplicidades identificadas: {len(dados_duplicados)}")
    print(f"Chaves incompletas: {len(dados_revisao)}")

    return dados_unicos, dados_duplicados, dados_revisao
