from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Usuario:
    id: Optional[int]
    nome: str
    email: str
    senha_hash: str

@dataclass
class Categoria:
    id: Optional[int]
    usuario_id: int
    nome: str
    teto: Optional[float] = None

@dataclass
class Transacao:
    id: Optional[int]
    usuario_id: int
    categoria_id: Optional[int]
    descricao: str
    valor: float
    tipo: str  # "ENTRADA" ou "SAIDA"
    data: date

@dataclass
class CategoriaSaldoDTO:
    id: Optional[int]
    nome: str
    teto: Optional[float]
    gastos: float
    disponivel: Optional[float]

@dataclass
class SaldoGeralDTO:
    saldo_total: float
    total_entradas: float
    total_saidas: float