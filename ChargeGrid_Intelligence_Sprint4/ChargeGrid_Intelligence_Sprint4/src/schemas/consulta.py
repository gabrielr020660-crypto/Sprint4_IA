from pydantic import BaseModel, Field, field_validator

class ConsultaRecarga(BaseModel):
    id_carregador: str = Field(description="Identificador único do carregador GoodWe")
    estado: str = Field(description="Estado atual do carregador (ex: Disponivel, Carregando, Erro)")
    potencia_kw: float = Field(description="Potência de carregamento em kW")
    valor_faturamento: float = Field(description="Valor estimado da recarga em Reais (R$)")

    @field_validator("potencia_kw")
    @classmethod
    def validar_potencia(cls, v: float) -> float:
        if v < 0 or v > 350:
            raise ValueError("A potência de recarga deve estar entre 0kW e 350kW.")
        return v