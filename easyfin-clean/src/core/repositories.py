from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Transacao

class TransacaoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, transacao: Transacao) -> Transacao:
        pass

    @abstractmethod
    def buscar_por_usuario(self, usuario_id: int, limite: int = 20) -> List[Transacao]:
        pass

    @abstractmethod
    def deletar(self, transacao_id: int, usuario_id: int) -> bool:
        pass