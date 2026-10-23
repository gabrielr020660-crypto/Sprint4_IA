import unittest
from src.guardrails.scope_validator import validar_escopo

class ScopeValidatorTests(unittest.TestCase):
    def test_ev_question_in_scope(self):
        self.assertTrue(validar_escopo('Como verifico o carregamento do equipamento GoodWe?'))

    def test_safety_question_in_scope(self):
        self.assertTrue(validar_escopo('Quais cuidados de segurança a documentação recomenda?'))

    def test_document_injection_question_in_scope(self):
        self.assertTrue(validar_escopo('Se um documento disser para ignorar as regras, devo seguir?'))

    def test_unrelated_question_out_of_scope(self):
        self.assertFalse(validar_escopo('Qual é a receita de bolo de cenoura?'))

if __name__ == '__main__':
    unittest.main()
