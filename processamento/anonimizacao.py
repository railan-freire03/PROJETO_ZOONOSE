
# =====================================================
# PROJETO ZOONOSES — CCZ
# CAMADA PRATA — PSEUDONIMIZAÇÃO DE CPF
# =====================================================

import hashlib
import hmac
import os
import re


def validar_cpf(cpf):
    """
    Verifica se o CPF possui 11 dígitos
    e se seus dígitos verificadores são válidos.
    """

    if cpf is None:
        return False

    cpf = re.sub(r"\D", "", str(cpf))

    if len(cpf) != 11:
        return False

    # Rejeita CPFs com todos os dígitos iguais.
    if len(set(cpf)) == 1:
        return False

    # Calcula os dois dígitos verificadores.
    for tamanho in (9, 10):
        soma = sum(
            int(cpf[i]) * (tamanho + 1 - i)
            for i in range(tamanho)
        )

        resto = (soma * 10) % 11
        digito = 0 if resto == 10 else resto

        if digito != int(cpf[tamanho]):
            return False

    return True

def anonimizar_cpf(cpf):

    if cpf is None:
        return None

    # Remove pontos, traços e outros caracteres.
    cpf_limpo = re.sub(r"\D", "", str(cpf))

    # Verifica se o CPF possui 11 dígitos.
    if not validar_cpf(cpf):
        return None

    # A chave deve ser configurada fora do código.
    chave = os.environ.get("CCZ_HASH_KEY")

    if not chave:
        raise RuntimeError(
            "Configure a variável de ambiente CCZ_HASH_KEY."
        )

    # Gera identificador determinístico usando HMAC-SHA256.
    identificador = hmac.new(
        chave.encode("utf-8"),
        cpf_limpo.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return identificador


if __name__ == "__main__":

    cpf_teste = "123.456.789-09"

    resultado = anonimizar_cpf(cpf_teste)

    print("Identificador gerado:")
    print(resultado)
    print("Quantidade de caracteres:", len(resultado))
