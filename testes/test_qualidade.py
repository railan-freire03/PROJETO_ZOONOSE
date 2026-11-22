
import unittest
import pandas as pd

from auditoria.qualidade_dados import verificar_qualidade


class TesteQualidadeDados(unittest.TestCase):

    # TESTE 1 — IDENTIFICADOR INVÁLIDO

    def test_identificador_invalido(self):

        dados = pd.DataFrame([{
            "id_evento": "ABC",
            "id_cidadao_hash": "hash_teste",
            "especie": "CACHORRO",
            "tipo_servico": "VACINACAO",
            "data_evento": "2026-11-10"
        }])

        completos, revisao = verificar_qualidade(dados)

        self.assertEqual(len(completos), 0)
        self.assertEqual(len(revisao), 1)

        self.assertIn(
            "id_evento invalido",
            revisao.iloc[0]["motivo_revisao"]
        )

    # TESTE 2 — DATA FUTURA

    def test_data_futura(self):

        dados = pd.DataFrame([{
            "id_evento": "10",
            "id_cidadao_hash": "hash_teste",
            "especie": "GATO",
            "tipo_servico": "ATENDIMENTO",
            "data_evento": "2099-12-31"
        }])

        completos, revisao = verificar_qualidade(dados)

        self.assertEqual(len(completos), 0)
        self.assertEqual(len(revisao), 1)

        self.assertEqual(
            revisao.iloc[0]["data_evento_original"],
            "2099-12-31"
        )

        self.assertIn(
            "data_evento futura",
            revisao.iloc[0]["motivo_revisao"]
        )


if __name__ == "__main__":
    unittest.main()
