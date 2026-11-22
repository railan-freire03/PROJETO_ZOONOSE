"""Gera tabelas analíticas a partir dos CSVs validados da camada Prata."""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PRATA = RAIZ / 'dados' / 'prata'
OURO = RAIZ / 'dados' / 'ouro'


def gerar_camada_ouro():
    caminho = PRATA / 'atendimentos_completos.csv'
    if not caminho.is_file():
        raise FileNotFoundError(f'Execute primeiro o tratamento: {caminho}')
    df = pd.read_csv(caminho, dtype={'id_evento': 'string'}, encoding='utf-8-sig')
    exigidas = {'id_evento','data_evento','bairro','especie','tipo_servico'}
    faltantes = exigidas - set(df.columns)
    if faltantes:
        raise ValueError(f'Colunas ausentes na Prata: {sorted(faltantes)}')
    df['data_evento'] = pd.to_datetime(df['data_evento'], errors='coerce')
    if df['data_evento'].isna().any():
        raise ValueError('Há datas inválidas em atendimentos_completos.csv')
    for coluna in ('bairro','especie','tipo_servico'):
        df[coluna] = df[coluna].fillna('NAO INFORMADO').astype(str).str.strip()
        df.loc[df[coluna].eq(''),coluna] = 'NAO INFORMADO'
    df['ano'] = df['data_evento'].dt.year
    df['mes'] = df['data_evento'].dt.month
    df['ano_mes'] = df['data_evento'].dt.strftime('%Y-%m')
    # A Ouro não exporta CPF, hash ou outros identificadores pessoais.
    fato = df[['id_evento','data_evento','ano','mes','ano_mes','bairro','especie','tipo_servico']].copy()
    fato['data_evento'] = fato['data_evento'].dt.strftime('%Y-%m-%d')
    OURO.mkdir(parents=True, exist_ok=True)
    fato.to_csv(OURO/'fato_atendimentos.csv',index=False,encoding='utf-8-sig')
    for coluna,arquivo in [('bairro','dim_bairro.csv'),('especie','dim_especie.csv'),('tipo_servico','dim_servico.csv')]:
        pd.DataFrame({coluna: sorted(df[coluna].unique())}).to_csv(OURO/arquivo,index=False,encoding='utf-8-sig')
    pd.DataFrame({'data_evento': sorted(fato['data_evento'].unique())}).to_csv(OURO/'dim_tempo.csv',index=False,encoding='utf-8-sig')
    resumo = pd.DataFrame([{'atendimentos_validos':len(fato),'bairros':df['bairro'].nunique(),'especies':df['especie'].nunique(),'tipos_servico':df['tipo_servico'].nunique()}])
    resumo.to_csv(OURO/'resumo_indicadores.csv',index=False,encoding='utf-8-sig')
    print(f'Camada Ouro gerada: {len(fato)} atendimentos válidos em {OURO}')
    return fato

if __name__ == '__main__':
    gerar_camada_ouro()
