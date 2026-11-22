
# =====================================================
# PROJETO ZOONOSES — CCZ
# CAMADA PRATA — PADRONIZAÇÃO DOS DADOS
# =====================================================

from datetime import datetime
from unidecode import unidecode


# PADRONIZAÇÃO DE TEXTOS


def padronizar_texto(valor):

    # Verifica se o valor está ausente.
    if valor is None:
        return None

    texto = str(valor).strip()

    # Identifica valores ausentes representados como texto.
    if texto.lower() in {"", "nan", "none", "null"}:
        return None

    # Remove espaços repetidos.
    texto = " ".join(texto.split())

    # Remove acentos e converte para maiúsculas.
    texto = unidecode(texto).upper()

    return texto


# PADRONIZAÇÃO DE DATAS

def padronizar_data(valor):

    if valor is None:
        return None

    texto = str(valor).strip()

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d"
    ]

    for formato in formatos:

        try:
            data = datetime.strptime(texto, formato)
            return data.strftime("%Y-%m-%d")

        except ValueError:
            continue

    return None


# TESTES DAS FUNÇÕES

if __name__ == "__main__":

    print("TESTE DE PADRONIZAÇÃO")

    print(padronizar_texto("  centro  "))
    print(padronizar_texto("  São   Francisco "))
    print(padronizar_texto("cachorro"))

    print(padronizar_data("10/11/2026"))
    print(padronizar_data("2026-11-10"))
    print(padronizar_data("11-11-2026"))
