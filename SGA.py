import random
# 図を生成するために、matplotlibを導入
import matplotlib.pyplot as plt

# 毎回の計算結果を同じくするため
random.seed(39)


# 個体と世帯を定義
def CreateIndividual():
    return [random.randint(0, 1) for _ in range(100)]


def CreatePopulation(size):
    return [CreateIndividual() for _ in range(size)]


# select関数
# Tournament Selectionを使用する
def tournament(population, size):
    participants = random.sample(population, size)
    winner = max(participants, key=lambda ind: fitness(ind))
    return winner.copy()


def select(population, size):
    return [tournament(population, size) for _ in range(len(population))]


# 交配
# 二つの個体を交配し、ランダムの位置の後ろの遺伝子を全部交換する
def SinglePointCrossover(ind1, ind2):
    loc = random.randint(0, len(ind1) - 1)
    genes1 = ind1[loc:]
    genes2 = ind2[loc:]
    ind1[loc:] = genes2
    ind2[loc:] = genes1
    return [ind1.copy(), ind2.copy()]


# 世帯の全ての隣の個体を一定の確率で交配する　交配しない個体はそのままに次世帯にいく
def mate(population, probability):
    new_population = []
    for i in range(0, len(population), 2):
        ind1 = population[i].copy()
        ind2 = population[i + 1].copy()
        if random.random() < probability:
            new_population.extend(SinglePointCrossover(ind1, ind2))
        else:
            new_population.extend([ind1, ind2])
    return new_population


# 突然変異
# 個体の一つの遺伝子をランダムに変異する
def flipOneGene(ind):
    loc = random.randint(0, len(ind) - 1)
    ind[loc] = 1 - ind[loc]  # 0->1 or 1->0
    return ind.copy()


# 世帯の全ての個体を一定の確率で変異する
def mutate(population, probability):
    new_population = []
    for ind in population:
        if random.random() < probability:
            new_population.append(flipOneGene(ind))
        else:
            new_population.append(ind.copy())
    return new_population


# 個体のfitnessの計算　
def fitness(individual):
    return sum(individual)


# 世帯のデータを統計する
def population_score_max(population):
    return max([fitness(ind) for ind in population])


def population_score_mean(population):
    return sum([fitness(ind) for ind in population]) / len(population)


# GA遺伝アルゴリズムを開始する
def main(
        POPULATION_SIZE=100,
        TOURNAMENT_SIZE=3,
        CROSSOVER_PROB=0.9,
        MUTATE_PROB=0.1,
        MAX_GENERATIONS=100
        # 世帯の大きさ、TournamentのSize、交配確率、変異確率、最大の世帯数
):
    # 初期化
    generation = 0
    population = CreatePopulation(POPULATION_SIZE)
    max_scores = [population_score_max(population)]
    mean_scores = [population_score_mean(population)]
    best_individual = []
    while generation < MAX_GENERATIONS:
        population = select(population, TOURNAMENT_SIZE)
        population = mate(population, CROSSOVER_PROB)
        population = mutate(population, MUTATE_PROB)
        max_scores.append(population_score_max(population))
        mean_scores.append(population_score_mean(population))
        best_individual = max(
            best_individual,
            max(population, key=lambda ind: fitness(ind))
        ).copy()
        print("Generation : ", generation, best_individual)
        if fitness(best_individual) == 100:
            break
        generation += 1

    # 結果を出力
    print("Best Solution:")
    print(best_individual)
    plt.plot(max_scores, color='red', label="Max Score")
    plt.plot(mean_scores, color='green', label="Mean Score")
    plt.legend()
    plt.xlabel("Generations")
    plt.ylabel("Fitness Score")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
