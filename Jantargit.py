import random

# Número de filósofos (e, consequentemente, número de garfos = 5)
NUM_FILOSOFOS = 5

# -----------------------------
# SIMULAÇÃO DO JANTAR DOS FILÓSOFOS
# -----------------------------
def simula_jantar(config):
 
    # Inicializa os 5 garfos como disponíveis (True = disponível)
    garfos = [True] * NUM_FILOSOFOS
    # Gera uma ordem aleatória para os filósofos tentarem comer
    ordem_filosofos = list(range(NUM_FILOSOFOS))
    random.shuffle(ordem_filosofos)
    # Contador de filósofos que conseguiram comer
    comedores = 0

    for i in ordem_filosofos:
        # Determina a ordem de pegar os garfos conforme a estratégia do filósofo i
        if config[i] == 0:  # Estratégia: pegar o garfo esquerdo primeiro
            primeiro = i
            segundo = (i + 1) % NUM_FILOSOFOS
        else:             # Estratégia: pegar o garfo direito primeiro
            primeiro = (i + 1) % NUM_FILOSOFOS
            segundo = i

        # Tenta pegar o primeiro garfo
        if garfos[primeiro]:
            # "Pega" o primeiro garfo (marca como indisponível)
            garfos[primeiro] = False
            # Verifica se o segundo garfo está disponível
            if garfos[segundo]:
                # Consegue pegar o segundo garfo: o filósofo come
                garfos[segundo] = False
                comedores += 1
                # Após comer, libera os dois garfos
                garfos[primeiro] = True
                garfos[segundo] = True
            else:
                # Não conseguiu pegar o segundo garfo; libera o primeiro
                garfos[primeiro] = True

    return comedores

def avalia_fitness(config, num_simulacoes=100):
   
    soma = 0
    for _ in range(num_simulacoes):
        soma += simula_jantar(config)
    return soma / num_simulacoes

# -----------------------------
# COMPONENTES DO ALGORITMO GENÉTICO
# -----------------------------
def gera_populacao(tamanho):
   
    populacao = []
    for _ in range(tamanho):
        cromossomo = [random.randint(0, 1) for _ in range(NUM_FILOSOFOS)]
        populacao.append(cromossomo)
    return populacao

def selecao_roleta(populacao, fitnesses):
   
    total_fitness = sum(fitnesses)
    # Se todas as fitness forem zero, seleciona aleatoriamente
    if total_fitness == 0:
        return random.choice(populacao)
    pick = random.uniform(0, total_fitness)
    current = 0
    for cromossomo, fit in zip(populacao, fitnesses):
        current += fit
        if current >= pick:
            return cromossomo

def crossover(pai1, pai2):
   
    ponto = random.randint(1, NUM_FILOSOFOS - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

def mutacao(cromossomo, taxa_mutacao=0.1):
   
    for i in range(NUM_FILOSOFOS):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]
    return cromossomo

# -----------------------------
# ALGORITMO GENÉTICO PRINCIPAL
# -----------------------------
def algoritmo_genetico(tamanho_pop=20, geracoes=50, taxa_mutacao=0.1):
   
    # Gera a população inicial
    populacao = gera_populacao(tamanho_pop)
    melhor_config = None
    melhor_fitness = -1

    for geracao in range(geracoes):
        fitnesses = [avalia_fitness(cromo) for cromo in populacao]

        # Atualiza o melhor cromossomo até o momento
        for cromo, fit in zip(populacao, fitnesses):
            if fit > melhor_fitness:
                melhor_fitness = fit
                melhor_config = cromo

        nova_populacao = []
        # Gera nova população aplicando seleção, crossover e mutação
        while len(nova_populacao) < tamanho_pop:
            # Seleciona dois pais
            pai1 = selecao_roleta(populacao, fitnesses)
            pai2 = selecao_roleta(populacao, fitnesses)
            # Realiza o crossover para gerar dois filhos
            filho1, filho2 = crossover(pai1, pai2)
            # Aplica mutação em cada filho
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        # Garante que a nova população tenha o tamanho correto
        populacao = nova_populacao[:tamanho_pop]

        # Exibe informações de progresso
        print(f"Geração {geracao+1} | Melhor fitness: {melhor_fitness:.2f} | Melhor configuração: {melhor_config}")

    return melhor_config, melhor_fitness

# -----------------------------
# EXECUÇÃO DO ALGORITMO
# -----------------------------
if __name__ == '__main__':
    melhor, fit = algoritmo_genetico(tamanho_pop=20, geracoes=50, taxa_mutacao=0.1)
    print("\nMelhor solução encontrada:")
    print("Configuração (estratégia por filósofo):", melhor)
    print(f"Fitness (média de filósofos que comeram): {fit:.2f}")
