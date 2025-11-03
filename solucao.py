from typing import Iterable, Set, Tuple

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai:'Nodo', acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __eq__(self, other):
        """Dois nós são iguais se tiverem o mesmo estado."""
        return isinstance(other, Nodo) and self.estado == other.estado

    def __hash__(self):
        """Permite usar Nodo em conjuntos e dicionários."""
        return hash(self.estado)


def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    sucessores = set()
    pos = estado.index('_')

    if pos not in (0, 1, 2): #pode mover o '0' para cima
        novo_estado = list(estado)
        novo_estado[pos], novo_estado[pos - 3] = novo_estado[pos - 3], novo_estado[pos]
        sucessores.add(("acima", ''.join(novo_estado)))
    
    if pos not in (6, 7, 8):  # pode mover o '0' para baixo
        novo_estado = list(estado)
        novo_estado[pos], novo_estado[pos + 3] = novo_estado[pos + 3], novo_estado[pos]
        sucessores.add(("abaixo", ''.join(novo_estado)))

    if pos not in (0, 3, 6):
        novo_estado = list(estado)
        novo_estado[pos], novo_estado[pos - 1] = novo_estado[pos - 1], novo_estado[pos]
        sucessores.add(("esquerda", ''.join(novo_estado)))

    if pos not in (2, 5, 8):
        novo_estado = list(estado)
        novo_estado[pos], novo_estado[pos + 1] = novo_estado[pos + 1], novo_estado[pos]
        sucessores.add(("direita", ''.join(novo_estado)))
    
    return sucessores


def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return: conjunto de nodos sucessores
    """
    # Obter o conjunto de tuplas (ação, novo_estado) do estado atual
    sucessores = sucessor(nodo.estado)
    
    # Criar um conjunto para armazenar os nodos sucessores
    nodos_sucessores = set()
    
    # Para cada ação e estado sucessor, criar um novo nodo
    for acao, novo_estado in sucessores:
        # Criar um novo nodo com:
        # - o novo estado
        # - o nodo atual como pai
        # - a ação que levou a este estado
        # - o custo do caminho até aqui (custo do pai + 1)
        novo_nodo = Nodo(novo_estado, nodo, acao, nodo.custo + 1)
        nodos_sucessores.add(novo_nodo)
    
    return nodos_sucessores


def calcula_hamming(estado: str) -> int:
    """
    Calcula a distância de Hamming (número de peças fora do lugar)
    em relação ao estado objetivo "12345678_"
    """
    objetivo = "12345678_"
    return sum(1 for i in range(9) if estado[i] != objetivo[i] and estado[i] != '_')

def calcula_manhattan(estado: str) -> int:
    """
    Calcula a soma das distâncias Manhattan de cada peça até sua posição objetivo
    """
    objetivo = "12345678_"
    distancia = 0
    
    # Posições x,y de cada índice no tabuleiro 3x3
    posicoes = {i: (i // 3, i % 3) for i in range(9)}
    
    for i in range(9):
        if estado[i] != '_':
            # Encontra a posição objetivo desta peça
            pos_obj = objetivo.index(estado[i])
            # Calcula a distância Manhattan entre a posição atual e a objetivo
            x1, y1 = posicoes[i]
            x2, y2 = posicoes[pos_obj]
            distancia += abs(x1 - x2) + abs(y1 - y2)
    
    return distancia

def constroi_caminho(nodo: Nodo) -> list[str]:
    """
    Constrói o caminho do nó inicial até o nó atual,
    retornando a lista de ações realizadas
    """
    caminho = []
    while nodo.pai is not None:
        caminho.append(nodo.acao)
        nodo = nodo.pai
    return list(reversed(caminho))

def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return: list[str] com sequência de ações ou None se não houver solução
    """
    from heapq import heappush, heappop
    
    # Nodo inicial
    inicial = Nodo(estado, None, None, 0)
    objetivo = "12345678_"
    
    # Fronteira (fila de prioridade) e conjunto de visitados
    fronteira = []
    visitados = set()
    
    # Adiciona o nodo inicial à fronteira com prioridade f(n) = g(n) + h(n)
    heappush(fronteira, (calcula_hamming(estado), 0, inicial))  # (f, contador, nodo)
    contador = 1  # Para desempate quando f for igual
    
    while fronteira:
        f, _, nodo_atual = heappop(fronteira)
        
        # Se chegou ao objetivo, reconstrói o caminho
        if nodo_atual.estado == objetivo:
            return constroi_caminho(nodo_atual)
            
        # Se já visitou este estado, continua
        if nodo_atual.estado in visitados:
            continue
            
        # Marca como visitado
        visitados.add(nodo_atual.estado)
        
        # Expande o nodo atual e adiciona sucessores à fronteira
        for sucessor in expande(nodo_atual):
            if sucessor.estado not in visitados:
                f = sucessor.custo + calcula_hamming(sucessor.estado)  # f = g + h
                heappush(fronteira, (f, contador, sucessor))
                contador += 1
    
    # Se não encontrou solução
    return None

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return: list[str] com sequência de ações ou None se não houver solução
    """
    from heapq import heappush, heappop
    
    # Nodo inicial
    inicial = Nodo(estado, None, None, 0)
    objetivo = "12345678_"
    
    # Fronteira (fila de prioridade) e conjunto de visitados
    fronteira = []
    visitados = set()
    
    # Adiciona o nodo inicial à fronteira com prioridade f(n) = g(n) + h(n)
    heappush(fronteira, (calcula_manhattan(estado), 0, inicial))  # (f, contador, nodo)
    contador = 1  # Para desempate quando f for igual
    
    while fronteira:
        f, _, nodo_atual = heappop(fronteira)
        
        # Se chegou ao objetivo, reconstrói o caminho
        if nodo_atual.estado == objetivo:
            return constroi_caminho(nodo_atual)
            
        # Se já visitou este estado, continua
        if nodo_atual.estado in visitados:
            continue
            
        # Marca como visitado
        visitados.add(nodo_atual.estado)
        
        # Expande o nodo atual e adiciona sucessores à fronteira
        for sucessor in expande(nodo_atual):
            if sucessor.estado not in visitados:
                f = sucessor.custo + calcula_manhattan(sucessor.estado)  # f = g + h
                heappush(fronteira, (f, contador, sucessor))
                contador += 1
    
    # Se não encontrou solução
    return None

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return: list[str] com sequência de ações ou None se não houver solução
    """
    from collections import deque
    
    # Nodo inicial
    inicial = Nodo(estado, None, None, 0)
    objetivo = "12345678_"
    
    # Se já começa no objetivo
    if estado == objetivo:
        return []
    
    # Fila para BFS e conjunto de visitados
    fila = deque([inicial])
    visitados = {estado}
    
    # Enquanto houver nodos para explorar
    while fila:
        nodo_atual = fila.popleft()
        
        # Expande o nodo atual
        for sucessor in expande(nodo_atual):
            # Se este estado ainda não foi visitado
            if sucessor.estado not in visitados:
                if sucessor.estado == objetivo:
                    return constroi_caminho(sucessor)
                    
                # Adiciona à fila e marca como visitado
                fila.append(sucessor)
                visitados.add(sucessor.estado)
    
    # Se não encontrou solução
    return None

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return: list[str] com sequência de ações ou None se não houver solução
    """
    # Nodo inicial
    inicial = Nodo(estado, None, None, 0)
    objetivo = "12345678_"
    
    # Se já começa no objetivo
    if estado == objetivo:
        return []
    
    # Pilha para DFS e conjunto de visitados
    pilha = [inicial]
    visitados = {estado}
    
    # Enquanto houver nodos para explorar
    while pilha:
        nodo_atual = pilha.pop()  # Remove e retorna o último elemento (topo da pilha)
        
        # Expande o nodo atual
        # Invertemos a ordem dos sucessores para manter a ordem das ações consistente
        for sucessor in reversed(list(expande(nodo_atual))):
            # Se este estado ainda não foi visitado
            if sucessor.estado not in visitados:
                if sucessor.estado == objetivo:
                    return constroi_caminho(sucessor)
                    
                # Adiciona à pilha e marca como visitado
                pilha.append(sucessor)
                visitados.add(sucessor.estado)
    
    # Se não encontrou solução
    return None

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
