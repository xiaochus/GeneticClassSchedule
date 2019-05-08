import copy
import numpy as np

from schedule import schedule_cost


class GeneticOptimize:
    """Genetic Algorithm.
    """
    def __init__(self, popsize=30, mutprob=0.3, elite=5, maxiter=100):
        # size of population
        self.popsize = popsize
        # prob of mutation
        self.mutprob = mutprob
        # number of elite
        self.elite = elite
        # iter times
        self.maxiter = maxiter

    def init_population(self, schedules, roomRange):
        """Init population

        Arguments:
            schedules: List, population of class schedules.
            roomRange: int, number of classrooms.
        """
        self.population = []

        for i in range(self.popsize):
            entity = []

            for s in schedules:
                s.random_init(roomRange)
                entity.append(copy.deepcopy(s))

            self.population.append(entity)

    def mutate(self, eiltePopulation, roomRange):
        """Mutation Operation

        Arguments:
            eiltePopulation: List, population of elite schedules.
            roomRange: int, number of classrooms.

        Returns:
            ep: List, population after mutation. 
        """
        e = np.random.randint(0, self.elite, 1)[0]
        pos = np.random.randint(0, 2, 1)[0]

        ep = copy.deepcopy(eiltePopulation[e])
    
        for p in ep:
            pos = np.random.randint(0, 3, 1)[0]
            operation = np.random.rand()

            if pos == 0:
                p.roomId = self.addSub(p.roomId, operation, roomRange)
            if pos == 1:
                p.weekDay = self.addSub(p.weekDay, operation, 5)
            if pos == 2:
                p.slot = self.addSub(p.slot, operation, 5)

        return ep

    def addSub(self, value, op, valueRange):
        """Add or sub operation in mutation.

        Arguments:
            value: int, value to be mutated.
            op: double, prob of operation.
            valueRange: int, range of value.

        Returns:
            value: int, mutated value. 
        """
        if op > 0.5:
            if value < valueRange:
                value += 1
            else:
                value -= 1
        else:
            if value - 1 > 0:
                value -= 1
            else:
                value += 1

        return value

    def crossover(self, eiltePopulation):
        """Crossover Operation

        Arguments:
            eiltePopulation: List, population of elite schedules.

        Returns:
            ep: List, population after crossover. 
        """
        e1 = np.random.randint(0, self.elite, 1)[0]
        e2 = np.random.randint(0, self.elite, 1)[0]

        pos = np.random.randint(0, 2, 1)[0]

        ep1 = copy.deepcopy(eiltePopulation[e1])
        ep2 = eiltePopulation[e2]

        for p1, p2 in zip(ep1, ep2):
            if pos == 0:
                p1.weekDay = p2.weekDay
                p1.slot = p2.slot
            if pos == 1:
                p1.roomId = p2.roomId

        return ep1

    def evolution(self, schedules, roomRange):
        """evolution
        
        Arguments:
            schedules: class schedules for optimization.
            elite: int, number of best result.

        Returns:
            index of best result.
            best conflict score.
        """
        # Main loop .
        bestScore = 0
        bestSchedule = None

        self.init_population(schedules, roomRange)

        for i in range(self.maxiter):
            eliteIndex, bestScore = schedule_cost(self.population, self.elite)

            print('Iter: {} | conflict: {}'.format(i + 1, bestScore))

            if bestScore == 0:
                bestSchedule = self.population[eliteIndex[0]]
                break

            # Start with the pure winners
            newPopulation = [self.population[index] for index in eliteIndex]

            # Add mutated and bred forms of the winners
            while len(newPopulation) < self.popsize:
                if np.random.rand() < self.mutprob:
                    # Mutation
                    newp = self.mutate(newPopulation, roomRange)
                else:
                    # Crossover
                    newp = self.crossover(newPopulation)

                newPopulation.append(newp)

            self.population = newPopulation

        return bestSchedule
