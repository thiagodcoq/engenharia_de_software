from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Transacao, Categoria 

class TransacaoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, transacao: Transacao) -> Transacao:
        pass

    @abstractmethod
    def buscar_por_usuario(self, usuario_id: int, limite: int = 20) -> List[Transacao]:
        pass
    
    @abstractmethod
    def buscar_por_id(self, transacao_id: int, usuario_id: int) -> Optional[Transacao]:
        pass

    @abstractmethod
    def deletar(self, transacao_id: int, usuario_id: int) -> bool:
        pass
        
class CategoriaRepositoryInterface(ABC):
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: int) -> List[Categoria]:
        pass
    
    @abstractmethod
    def salvar(self, categoria: Categoria) -> Categoria:
        pass