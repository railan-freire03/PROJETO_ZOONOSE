# Projeto CCZ — Pipeline de Engenharia de Dados

## Arquitetura
- **Bronze**: `processamento/ingestao.py` valida e preserva arquivos originais por lote.
- **Prata**: `processamento/tratamento.py` lê o CSV `atendimentos_teste.csv` do lote Bronze mais recente, padroniza, pseudonimiza, valida e separa duplicados/revisão.
- **Ouro**: `processamento/camada_ouro.py` gera fatos, dimensões simples e indicadores a partir dos atendimentos válidos.
- **Interface**: `interface/app.py` mostra indicadores e filtros sem expor hashes ou CPF.

## Executar no VS Code, a partir da pasta raiz
```bash
source .venv/bin/activate
python -m unittest discover -s testes -p 'test_*.py' -v
python processamento/ingestao.py
python processamento/tratamento.py
python processamento/camada_ouro.py
streamlit run interface/app.py
```

**Atenção:** antes da ingestão, coloque `atendimentos_teste.csv` em `dados/entrada/`. A variável `CCZ_HASH_KEY` precisa estar configurada e **ser a mesma usada nas execuções anteriores**. Não envie a chave, CPF, arquivos brutos ou dados da camada Prata para repositórios públicos. A pasta `.venv` e os dados de entrada/Prata/Bronze não acompanham este pacote.

## Limitações desta entrega
- A ingestão valida CSV/JSON/XML/TXT, mas o tratamento integrado está limitado ao CSV com nome fixo.
- A camada Ouro usa CSVs e dimensões descritivas simples; não é um esquema estrela com chaves substitutas.
- O dashboard não contém mapa ou integração geográfica.
- O identificador de origem é único apenas dentro do arquivo processado, não globalmente.
- Os dados do dashboard refletem a última execução da camada Ouro; execute novamente após atualizar a Prata.
- A Bronze pode conter dados pessoais originais e exige controle de acesso.
