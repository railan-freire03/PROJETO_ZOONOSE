"""Painel de atendimentos CCZ: apenas dados analíticos da camada Ouro."""
from pathlib import Path
import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
OURO = RAIZ / 'dados' / 'ouro'
PRATA = RAIZ / 'dados' / 'prata'
st.set_page_config(page_title='CCZ | Painel de Zoonoses', page_icon='🐾', layout='wide')
st.title('🐾 CCZ — Painel de Zoonoses')
st.caption('Indicadores de atendimentos | Camada Ouro | Dados do projeto')

@st.cache_data(ttl=30)
def carregar(caminho, modificacao):
    return pd.read_csv(caminho,encoding='utf-8-sig')

arquivo = OURO/'fato_atendimentos.csv'
if not arquivo.is_file():
    st.warning('Camada Ouro ainda não gerada. Execute: python processamento/camada_ouro.py')
    st.stop()

df = carregar(str(arquivo), arquivo.stat().st_mtime_ns)
if df.empty:
    st.info('Nenhum atendimento válido disponível para análise.')
    st.stop()

df['data_evento'] = pd.to_datetime(df['data_evento'],errors='coerce')
with st.sidebar:
    st.header('Filtros')
    bairros = st.multiselect('Bairro',sorted(df['bairro'].dropna().unique()))
    especies = st.multiselect('Espécie',sorted(df['especie'].dropna().unique()))
    servicos = st.multiselect('Tipo de serviço',sorted(df['tipo_servico'].dropna().unique()))
    anos = st.multiselect('Ano',sorted(df['ano'].dropna().astype(int).unique().tolist()))
filtrado = df.copy()
for coluna,selecionados in [('bairro',bairros),('especie',especies),('tipo_servico',servicos),('ano',anos)]:
    if selecionados:filtrado=filtrado[filtrado[coluna].isin(selecionados)]

c1,c2,c3,c4=st.columns(4)
c1.metric('Atendimentos',len(filtrado))
c2.metric('Bairros',filtrado['bairro'].nunique())
c3.metric('Espécies',filtrado['especie'].nunique())
c4.metric('Tipos de serviço',filtrado['tipo_servico'].nunique())
if filtrado.empty:
    st.info('Nenhum registro corresponde aos filtros selecionados.')
    st.stop()

def grafico(coluna,titulo):
    st.subheader(titulo)
    contagem=filtrado[coluna].value_counts().rename_axis(coluna).reset_index(name='Atendimentos')
    st.bar_chart(contagem.set_index(coluna)['Atendimentos'])

esq,dir=st.columns(2)
with esq:grafico('especie','Atendimentos por espécie')
with dir:grafico('tipo_servico','Atendimentos por serviço')
esq,dir=st.columns(2)
with esq:grafico('bairro','Atendimentos por bairro')
with dir:
    st.subheader('Evolução mensal')
    serie=filtrado.groupby('ano_mes').size().sort_index()
    st.line_chart(serie)
st.subheader('Atendimentos consolidados')
st.dataframe(filtrado.sort_values('data_evento',ascending=False),use_container_width=True,hide_index=True)
st.download_button('Baixar dados filtrados (CSV)',filtrado.to_csv(index=False).encode('utf-8-sig'),file_name='atendimentos_ccz_filtrados.csv',mime='text/csv')
st.divider()
st.subheader('Qualidade do processamento')
metricas=[]
for nome,rotulo in [('atendimentos_completos.csv','Válidos'),('atendimentos_revisao.csv','Revisão'),('atendimentos_duplicados.csv','Duplicados')]:
    caminho=PRATA/nome
    if caminho.is_file():
        metricas.append((rotulo,len(pd.read_csv(caminho,encoding='utf-8-sig'))))
if metricas:
    cols=st.columns(len(metricas))
    for col,(rotulo,quantidade) in zip(cols,metricas):col.metric(rotulo,quantidade)
else:st.caption('Arquivos de qualidade da Prata indisponíveis.')
st.caption('Painel analítico: não exibe nome, CPF ou hash de cidadão. Sem mapa geográfico nesta versão.')
