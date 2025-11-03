import time
import solucao

# Variável global para contar expansões
nos_expandidos = 0

def main():
    # Estado inicial a ser analisado
    estado = "2_3541687"
    
    print("\nAnálise para A* com heurística de Hamming:")
    print("-" * 50)
    
    # Reseta o contador
    global nos_expandidos
    nos_expandidos = 0
    
    # Executa A* com Hamming
    inicio = time.time()
    solucao_hamming = solucao.astar_hamming(estado)
    tempo_hamming = time.time() - inicio
    
    expandidos_hamming = nos_expandidos
    
    print(f"Nós expandidos: {expandidos_hamming}")
    print(f"Tempo decorrido: {tempo_hamming:.3f} segundos")
    print(f"Custo da solução: {len(solucao_hamming) if solucao_hamming else None} movimentos")
    
    print("\nAnálise para A* com heurística de Manhattan:")
    print("-" * 50)
    
    # Reseta o contador
    nos_expandidos = 0
    
    # Executa A* com Manhattan
    inicio = time.time()
    solucao_manhattan = solucao.astar_manhattan(estado)
    tempo_manhattan = time.time() - inicio
    
    expandidos_manhattan = nos_expandidos
    
    print(f"Nós expandidos: {expandidos_manhattan}")
    print(f"Tempo decorrido: {tempo_manhattan:.3f} segundos")
    print(f"Custo da solução: {len(solucao_manhattan) if solucao_manhattan else None} movimentos")

if __name__ == '__main__':
    main()