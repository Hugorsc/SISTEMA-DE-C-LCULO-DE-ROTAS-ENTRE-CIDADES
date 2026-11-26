"""
Sistema de rotas entre cidades com o algoritmo de Dijkstra.

Representação: lista de adjacência (dict de dicts), grafo não direcionado.
    cidades: {id: nome}
    estradas: {id_a: {id_b: km, ...}, ...}  (cada estrada guardada nos dois sentidos)

Uso:
    python rotas_dijkstra.py            -> abre o menu
    python rotas_dijkstra.py --teste    -> executa os 10 testes obrigatórios
"""
import heapq
import sys


class Grafo:
    def __init__(self):
        self.cidades = {}   # id -> nome
        self.adj = {}       # id -> {vizinho: distancia}

    # ---------- cadastro ----------
    def add_cidade(self, id_, nome):
        if id_ in self.cidades:
            raise ValueError(f"Já existe uma cidade com o id {id_}.")
        if not nome.strip():
            raise ValueError("O nome da cidade não pode ser vazio.")
        self.cidades[id_] = nome.strip()
        self.adj[id_] = {}

    def add_estrada(self, a, b, km):
        for c in (a, b):
            if c not in self.cidades:
                raise ValueError(f"Cidade {c} não existe.")
        if a == b:
            raise ValueError("Uma estrada precisa ligar duas cidades diferentes.")
        if km < 0:
            raise ValueError("A distância não pode ser negativa.")
        if b in self.adj[a]:
            raise ValueError("Essa estrada já está cadastrada.")
        self.adj[a][b] = km
        self.adj[b][a] = km

    # ---------- remoção ----------
    def remover_estrada(self, a, b):
        if a not in self.cidades or b not in self.cidades:
            raise ValueError("Cidade informada não existe.")
        if b not in self.adj[a]:
            raise ValueError("Essa estrada não existe.")
        del self.adj[a][b]
        del self.adj[b][a]

    def remover_cidade(self, id_):
        if id_ not in self.cidades:
            raise ValueError("Cidade informada não existe.")
        for viz in list(self.adj[id_]):
            del self.adj[viz][id_]
        del self.adj[id_]
        del self.cidades[id_]

    # ---------- Dijkstra ----------
    def menor_rota(self, origem, destino):
        """Retorna (distancia, [ids do caminho]) ou None se não houver rota."""
        for c in (origem, destino):
            if c not in self.cidades:
                raise ValueError(f"Cidade {c} não existe.")
        dist = {c: float("inf") for c in self.cidades}
        anterior = {}
        dist[origem] = 0
        fila = [(0, origem)]
        while fila:
            d, u = heapq.heappop(fila)
            if d > dist[u]:
                continue            # entrada desatualizada
            if u == destino:
                break
            for v, peso in self.adj[u].items():
                nd = d + peso
                if nd < dist[v]:
                    dist[v] = nd
                    anterior[v] = u
                    heapq.heappush(fila, (nd, v))
        if dist[destino] == float("inf"):
            return None
        caminho = [destino]
        while caminho[-1] != origem:
            caminho.append(anterior[caminho[-1]])
        return dist[destino], caminho[::-1]


# ---------- dados iniciais (distâncias fictícias, em km) ----------
def grafo_inicial():
    g = Grafo()
    nomes = ["Viçosa", "Coimbra", "Teixeiras", "Ervália", "Cajuri",
             "Paula Cândido", "São Miguel do Anta", "Porto Firme",
             "Araponga", "Canaã"]
    for i, n in enumerate(nomes, 1):
        g.add_cidade(i, n)
    estradas = [
        (1, 2, 20),  # Viçosa - Coimbra
        (2, 4, 30),  # Coimbra - Ervália      (Viçosa→Coimbra→Ervália = 50)
        (1, 4, 60),  # Viçosa - Ervália       (direta, mas maior que 50)
        (1, 5, 25),  # Viçosa - Cajuri
        (5, 4, 25),  # Cajuri - Ervália       (empate: Viçosa→Cajuri→Ervália = 50)
        (1, 3, 35),  # Viçosa - Teixeiras
        (3, 7, 15),  # Teixeiras - São Miguel do Anta
        (1, 7, 40),  # Viçosa - São Miguel do Anta (direta, menor que 50 via Teixeiras)
        (1, 6, 15),  # Viçosa - Paula Cândido
        (6, 8, 20),  # Paula Cândido - Porto Firme (única ligação de Porto Firme)
        (2, 3, 30),  # Coimbra - Teixeiras
        (3, 5, 40),  # Teixeiras - Cajuri
        (6, 2, 35),  # Paula Cândido - Coimbra
        (4, 6, 45),  # Ervália - Paula Cândido
        (9, 10, 18), # Araponga - Canaã (ilhado: sem rota para as demais)
    ]
    for a, b, km in estradas:
        g.add_estrada(a, b, km)
    return g


# ---------- interface ----------
def ler_int(msg):
    try:
        return int(input(msg).strip())
    except ValueError:
        raise ValueError("Entrada inválida: digite um número inteiro.")


def ler_num(msg):
    try:
        return float(input(msg).strip().replace(",", "."))
    except ValueError:
        raise ValueError("Entrada inválida: digite um número.")


def fmt_km(x):
    return f"{x:g} km"


def listar(g):
    if not g.cidades:
        print("Nenhuma cidade cadastrada.")
    for id_, nome in sorted(g.cidades.items()):
        print(f"[{id_}] {nome}")
        if not g.adj[id_]:
            print("     (sem estradas)")
        for viz, km in sorted(g.adj[id_].items()):
            print(f"     -> [{viz}] {g.cidades[viz]}: {fmt_km(km)}")


def mostrar_rota(g, o, d):
    r = g.menor_rota(o, d)
    print(f"Origem: {g.cidades[o]} | Destino: {g.cidades[d]}")
    if r is None:
        print("Não existe rota disponível entre as cidades informadas.")
        return
    km, caminho = r
    print(" → ".join(g.cidades[c] for c in caminho) + f" | Distância total: {fmt_km(km)}")


MENU = """
===== ROTAS =====
1 - Cadastrar cidade
2 - Cadastrar estrada
3 - Listar cidades e estradas
4 - Calcular menor rota
5 - Verificar existência de rota
6 - Remover estrada
7 - Remover cidade
8 - Encerrar
"""


def menu():
    g = grafo_inicial()
    while True:
        print(MENU)
        op = input("Opção: ").strip()
        try:
            if op == "1":
                g.add_cidade(ler_int("Id: "), input("Nome: "))
                print("Cidade cadastrada.")
            elif op == "2":
                a, b = ler_int("Id cidade A: "), ler_int("Id cidade B: ")
                g.add_estrada(a, b, ler_num("Distância (km): "))
                print("Estrada cadastrada.")
            elif op == "3":
                listar(g)
            elif op == "4":
                mostrar_rota(g, ler_int("Id origem: "), ler_int("Id destino: "))
            elif op == "5":
                o, d = ler_int("Id origem: "), ler_int("Id destino: ")
                r = g.menor_rota(o, d)
                print("Existe rota." if r else "Não existe rota disponível.")
            elif op == "6":
                g.remover_estrada(ler_int("Id cidade A: "), ler_int("Id cidade B: "))
                print("Estrada removida.")
            elif op == "7":
                g.remover_cidade(ler_int("Id da cidade: "))
                print("Cidade removida.")
            elif op == "8":
                print("Encerrando.")
                break
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


# ---------- testes obrigatórios ----------
def testes():
    def erro(f, *a):
        try:
            f(*a)
        except ValueError:
            return True
        return False

    g = grafo_inicial()
    # 1 origem = destino
    assert g.menor_rota(1, 1) == (0, [1])
    # 2 estrada direta (Viçosa - São Miguel do Anta: 40 < 50 via Teixeiras)
    assert g.menor_rota(1, 7) == (40, [1, 7])
    # 3 rota com intermediárias (Viçosa → Coimbra → Ervália = 50 < 60 direta)
    km, cam = g.menor_rota(1, 4)
    assert km == 50 and cam in ([1, 2, 4], [1, 5, 4])
    # 4 empate: as duas rotas de 50 km são válidas (verificado acima)
    # 5 sem conexão
    assert g.menor_rota(1, 9) is None
    # 6 remover estrada recalcula (remove Viçosa-São Miguel: passa a 50 via Teixeiras)
    g.remover_estrada(1, 7)
    assert g.menor_rota(1, 7) == (50, [1, 3, 7])
    assert erro(g.remover_estrada, 1, 7)           # estrada inexistente
    # 7 remover cidade (Paula Cândido isola Porto Firme)
    assert g.menor_rota(1, 8) == (35, [1, 6, 8])
    g.remover_cidade(6)
    assert g.menor_rota(1, 8) is None
    assert 6 not in g.adj[1]
    # 8 cidade inexistente
    assert erro(g.menor_rota, 1, 99)
    assert erro(g.add_estrada, 1, 99, 10)
    # 9 distância negativa
    assert erro(g.add_estrada, 1, 8, -5)
    # 10 estrada duplicada (nos dois sentidos)
    assert erro(g.add_estrada, 1, 2, 20)
    assert erro(g.add_estrada, 2, 1, 20)
    print("Todos os 10 testes passaram.")


if __name__ == "__main__":
    testes() if "--teste" in sys.argv else menu()