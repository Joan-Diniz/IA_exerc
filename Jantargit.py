import random

# Parâmetros da Simulação

NUM_FILOSOFOS = 5         # Número de filósofos (e garfos)
TEMPO_COMER = 1.0         # Duração em que um filósofo "come" e mantém os garfos
INTERVALO_TEMPO = (0, 10) # Intervalo permitido para os atrasos

# Função de simulação do problema dos filósofos
def simular(delays):
    # Inicializa os garfos: cada garfo terá uma lista de intervalos ocupados.
    garfos = [[] for _ in range(NUM_FILOSOFOS)]
    sucesso = 0  # Contador de filósofos que conseguiram comer

    # Cria uma lista de eventos: (atraso, índice do filósofo)
    eventos = sorted([(d, i) for i, d in enumerate(delays)], key=lambda x: x[0])
    
    # Processa cada evento em ordem de chegada (menor atraso primeiro)
    for d, i in eventos:
        garfo_esq = i
        garfo_dir = (i + 1) % NUM_FILOSOFOS
        
        # Verifica se um garfo está livre no instante 'd'
        def esta_livre(intervalos):
            for (inicio, fim) in intervalos:
                if d >= inicio and d < fim:
                    return False
            return True

        # Se ambos os garfos estão livres, o filósofo come e ocupa os garfos
        if esta_livre(garfos[garfo_esq]) and esta_livre(garfos[garfo_dir]):
            sucesso += 1
            garfos[garfo_esq].append((d, d + TEMPO_COMER))
            garfos[garfo_dir].append((d, d + TEMPO_COMER))
    
    return sucesso

# Parâmetros do Algoritmo Genético

POPULACAO = 50             # Tamanho da população
GERACOES = 100             # Número de gerações
TAXA_CROSSOVER = 0.8       # Probabilidade de crossover
TAXA_MUTACAO = 0.3         # Probabilidade de mutação (alta para promover variedade)
STDDEV_MUTACAO = 0.5       # Desvio padrão para o ruído na mutação

# Cria um indivíduo aleatório
def criar_individuo():
    return [random.uniform(*INTERVALO_TEMPO) for _ in range(NUM_FILOSOFOS)]

# Operador de crossover de um ponto
def crossover(pai1, pai2):
    if random.random() < TAXA_CROSSOVER:
        ponto = random.randint(1, NUM_FILOSOFOS - 1)
        filho = pai1[:ponto] + pai2[ponto:]
        return filho
    else:
        return pai1.copy()

# Operador de mutação: adiciona ruído gaussiano ao gene
def mutacao(individuo):
    for i in range(len(individuo)):
        if random.random() < TAXA_MUTACAO:
            individuo[i] += random.gauss(0, STDDEV_MUTACAO)
            individuo[i] = max(INTERVALO_TEMPO[0], min(INTERVALO_TEMPO[1], individuo[i]))
    return individuo

# Função principal do algoritmo genético
def algoritmo_genetico():
    populacao = [criar_individuo() for _ in range(POPULACAO)]
    melhor_individuo = None
    melhor_fitness = -1

    for geracao in range(GERACOES):
        # Avalia a aptidão de cada indivíduo
        fitness = [simular(ind) for ind in populacao]
        
        # Atualiza o melhor indivíduo encontrado
        for i, fit in enumerate(fitness):
            if fit > melhor_fitness:
                melhor_fitness = fit
                melhor_individuo = populacao[i]
        
        print(f"Geração {geracao} - Melhor aptidão: {melhor_fitness}")

        # Seleção por torneio
        nova_populacao = []
        while len(nova_populacao) < POPULACAO:
            torneio = 3
            candidatos = random.sample(list(zip(populacao, fitness)), torneio)
            pai1 = max(candidatos, key=lambda x: x[1])[0]
            candidatos = random.sample(list(zip(populacao, fitness)), torneio)
            pai2 = max(candidatos, key=lambda x: x[1])[0]
            
            # Aplica crossover e mutação
            filho = crossover(pai1, pai2)
            filho = mutacao(filho)
            nova_populacao.append(filho)
        
        populacao = nova_populacao

    return melhor_individuo, melhor_fitness

# Execução do algoritmo genético com exibição da melhor solução em porcentagem
if __name__ == "__main__":
    melhor_solucao, aptidao = algoritmo_genetico()
    # Calcula a porcentagem da melhor aptidão em relação ao máximo (NUM_FILOSOFOS)
    porcentagem = (aptidao / NUM_FILOSOFOS) * 100

    print("\nMelhor solução encontrada (vetor de atrasos):")
    print(melhor_solucao)
    print("Aptidão (número de filósofos que comeram):", aptidao)
    print("Porcentagem de sucesso: {:.2f}%".format(porcentagem))
