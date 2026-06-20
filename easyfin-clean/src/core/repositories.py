from abc import ABC, abstractmethod
from typing import List
from .entities import Transacao, Categoria 
from typing import List, Optional

class TransacaoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, transacao: Transacao) -> Transacao:
        pass
    @abstractmethod
    def buscar_por_periodo(self, usuario_id: int, inicio, fim) -> List[Transacao]:
        """Transacao com inicio <= data < fim """
        pass

    @abstractmethod
    def buscar_por_usuario(self, usuario_id: int, limite: int = 20) -> List[Transacao]:
        pass

    @abstractmethod
    def deletar(self, transacao_id: int, usuario_id: int) -> bool:
        pass

class CategoriaRepositoryInterface(ABC):
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: int) -> List[Categoria]:
        pass
    
    @abstractmethod
    def buscar_por_id(self, categoria_id: int, usuario_id:int) -> Optional[Categoria]:
        pass
    
    @abstractmethod
    def salvar(self, categoria: Categoria) -> Categoria:
        pass