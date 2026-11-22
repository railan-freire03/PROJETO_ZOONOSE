
import unittest
import pandas as pd

from processamento.deduplicacao import identificar_duplicidades


class TesteDeduplicacao(unittest.TestCase):

    def test_registros_duplicados(self):

        # Dois registros do mesmo atendimento.
        dados = pd.DataFrame([
            {
                "id_evento": 1,
                "id_cidadao_hash": "hash_teste",
                "data_evento": "2026-11-10",
                "tipo_servico": "VACINACAO",
                "especie": "CACHORRO"
            },
            {
                "id_evento": 2,
                "id_cidadao_hash": "hash_teste",
                "data_evento": "2026-11-10",
                "tipo_servico": "VACINACAO",
                "especie": "CACHORRO"
            }
        ])

        unicos, duplicados, revisao = identificar_duplicidades(
            dados
        )

        # Apenas um registro deve permanecer como único.
        self.assertEqual(len(unicos), 1)

        # O outro deve ser identificado como duplicado.
        self.assertEqual(len(duplicados), 1)

        # Nenhum deve precisar de revisão das chaves.
        self.assertEqual(len(revisao), 0)


if __name__ == "__main__":
    unittest.main()
