from random import randrange, seed, choice
from operator import attrgetter

SPRINT_HOURS_TIME_SLOTS 			= 40

# Fitness variables weight
OUT_OF_SPRINT_DEPENDENCY_PENALTY 	= 0.6
IN_SPRINT_DEPENDENCY_PENALTY 		= 0.05
HAS_DEPENDANTS_BONUS 				= 0.1

# Genetic parameters
INITIAL_FITNESS 					= 0
INITIAL_POPIULATION_SIZE 			= 200
MUTATION_INTENSITY 					= 3
MUTATION_RATE 						= 0.3


def cria_tickets_aleatorios(numero_de_tickets):
	seed()
	tickets = []
	for key in range(numero_de_tickets):
		dependencias = []
		dependentes = []
		pontos = 1+randrange(0, 10, 1)
		numero_de_dependencias = randrange(0, 3, 1)
		numero_de_dependentes = randrange(0, 3, 1)
		importancia = 1+randrange(0, 100, 1)

		for i in range(numero_de_dependencias):
			dependencia = randrange(0, numero_de_tickets, 1)
			dependencias.append(dependencia)
		for i in range(key):
			if key in tickets[i].dependents:
				dependencias.append(i)

		for i in range(numero_de_dependentes):
			dependente = randrange(0, numero_de_tickets, 1)
			dependentes.append(dependente)
		for i in range(key):
			if key in tickets[i].dependencies:
				dependentes.append(i)

		tickets.append(Ticket(dependencias, dependentes, key, importancia, pontos))

	return tickets

def lowerNumerOfKeys(arr1, arr2):
	if len(arr1)>len(arr2):
		return len(arr2)
	return len(arr1)

class Ticket:

	@property
	def dependencies():
		return self.dependencies

	def __init__(self, dependencies, dependents, key, importance, points):
		self.dependencies = dependencies
		self.dependents = dependents
		self.key = key
		self.importance = importance
		self.points = points

	def computeTicketFitness(self, keys_inside_sprint):

		penalty_multiplier = 1;
		for dependency in self.dependencies:
			if dependency in keys_inside_sprint:
				penalty_multiplier-= IN_SPRINT_DEPENDENCY_PENALTY
			else:
				penalty_multiplier-= OUT_OF_SPRINT_DEPENDENCY_PENALTY

		bonus_multiplier = 1;
		for dependent in self.dependents:
			bonus_multiplier+= HAS_DEPENDANTS_BONUS

		if penalty_multiplier<0:
			return 0

		return self.importance*bonus_multiplier*penalty_multiplier

class Sprint:
	def ticket_array(self):
		return self.tickets

	def fitness(self):
		return self.fitness

	def __init__(self, all_tickets):#all_tickets devem estar organizados por points, de menos pra mais.
		points_left = SPRINT_HOURS_TIME_SLOTS;
		tickets = []
		tickets_left = all_tickets[:]


		while points_left > 0 and len(tickets_left)>0:
			selected_ticket = choice(tickets_left)

			if selected_ticket.points > points_left:
				ticket_out = tickets_left.pop()
				while ticket_out.points > points_left:
					if (len(tickets_left)==0):
						self.tickets = tickets
						return
					ticket_out = tickets_left.pop()
					

				tickets_left.append(ticket_out)
				selected_ticket = choice(tickets_left)
			
			tickets.append(selected_ticket)
			tickets_left.remove(selected_ticket)
			points_left -= selected_ticket.points

		self.tickets = tickets
		self.fitness = 0


	def computeSprintFitness(self):
		f = 0;

		keys = []
		fit = []
		temp = 0
		for ticket in self.tickets:
			keys.append(ticket.key)

		for ticket in self.tickets:
			f+=ticket.computeTicketFitness(keys)
		self.fitness = f

	def computeSprintPoints(self):
		points = 0
		for ticket in self.tickets:
			points += ticket.points
		self.points = points

	def printSprint(self):
		self.computeSprintPoints()
		print('pontos totais: {0}, fitness: {1}'.format(self.points, self.fitness))
		for ticket in self.tickets:
			print('Ticket #{0}:\nDependencias:{1}\nDependentes:{2}\nImportancia:{3}'.format(ticket.key, ticket.dependencies, ticket.dependents, ticket.importance))
		print('pontos totais: {0}, fitness: {1}'.format(self.points, self.fitness))
		return self.fitness


class Population:
	def __init__(self, all_tickets):
		self.population = []
		for i in range(INITIAL_POPIULATION_SIZE):
			self.population.append(Sprint(all_tickets))

	def computeFitness(self):
		for sprint in self.population:
			sprint.computeSprintFitness()
		(self.population).sort(key=attrgetter('fitness'))

	def printFitness(self):
		print('{0}'.format(self.population[INITIAL_POPIULATION_SIZE-1].fitness))

	def parents_select(self):
		#Type of selection: Prioritizes best parents.
		#Returns 2 vectors, with the tickets(chromossomes) of each selected parent
		first_parent_roll = 0.8 ** (randrange(0, 100)/(-5.077) - 1) - 1.2
		second_parent_roll = 0.8 ** (randrange(0, 100)/(-5.077) - 1) - 1.2

		# normalizing for population size
		first_parent_roll = INITIAL_POPIULATION_SIZE - 1 - int((first_parent_roll / 100.0) * len(self.population))
		second_parent_roll = INITIAL_POPIULATION_SIZE - 1 - int((second_parent_roll / 100.0) * len(self.population))

		first_parent = self.population[first_parent_roll]
		second_parent = self.population[second_parent_roll]

		return first_parent.ticket_array(), second_parent.ticket_array()

	def crossover(self):
		parent = [None] * 2
		child_tickets = []
		a, b = self.parents_select()
		parent = a[:] + b[:]

		points_left = SPRINT_HOURS_TIME_SLOTS

		#Each chromossome of child is a copy of parent's chromossome, parent randomly chosen:
		while points_left > 0 and len(parent)>0:
			dice = randrange(0, len(parent))
			ticket = parent[dice]
			if ticket not in child_tickets:
				child_tickets.append(ticket)
				points_left -= ticket.points
				if points_left <= 0:
					break
			parent.remove(parent[dice])
		child = Sprint(child_tickets)

		return child

	def createChildren(self, all_tickets, mutation_rate, mutation_intensity):
		children = []
		for i in range(INITIAL_POPIULATION_SIZE):
			children.append(self.crossover())
		self.mutation(children, all_tickets, mutation_rate, mutation_intensity)

		return children

	def evolve(self, all_tickets, mutation_rate, mutation_intensity):
		self.computeFitness()
		self.population += self.createChildren(all_tickets, mutation_rate, mutation_intensity)
		self.computeFitness()
		self.population = self.population[INITIAL_POPIULATION_SIZE:INITIAL_POPIULATION_SIZE*2]

	def run_generation(self, number_of_generations, all_tickets, mutation_rate):
		convergency_counter = 0
		mutation_intensity = MUTATION_INTENSITY
		best_fitness_vector = []

		for i in range(number_of_generations):
			self.evolve(all_tickets, mutation_rate, mutation_intensity)
			self.printFitness()
			best_fitness_vector.append(self.population[INITIAL_POPIULATION_SIZE-1].fitness)
			if i>5 and best_fitness_vector[-1] == best_fitness_vector[-2]:
				convergency_counter+=1
				if (mutation_rate!=0):
					mutation_rate += convergency_counter*0.1
				mutation_intensity += int(convergency_counter*0.2)
			else:
				convergency_counter=0
				mutation_intensity = MUTATION_INTENSITY
				if mutation_rate!=0:
					mutation_rate = MUTATION_RATE

		return self.population[INITIAL_POPIULATION_SIZE-1].ticket_array()

	def mutation(self, children, all_tickets, mutation_rate, mutation_intensity):
		#Mutation Mode: Plus_Minus
		temporary_population = []

		for sprint in children:
			new_tickets = []

			for ticket in sprint.tickets:
				chance = randrange(0, 100)/100.0
				if chance<=mutation_rate: #ocorre mutacao
					if randrange(0,2)==1:
						if ticket.key+mutation_intensity < INITIAL_POPIULATION_SIZE:
							new_tickets.append(all_tickets[ticket.key+mutation_intensity])
						else:
							new_tickets.append(all_tickets[ticket.key+mutation_intensity - INITIAL_POPIULATION_SIZE - 1])
					else:
						if ticket.key-mutation_intensity>=0:
							new_tickets.append(all_tickets[ticket.key-mutation_intensity])
						else:
							new_tickets.append(all_tickets[INITIAL_POPIULATION_SIZE + ticket.key-mutation_intensity])
				else:
					new_tickets.append(ticket)

			temporary_population.append(Sprint(new_tickets))
		children = temporary_population




def main(tickets=""):
	m = 0
	s = 0
	tickets = cria_tickets_aleatorios(1000)
	tickets.sort(key=attrgetter('points'))

	population = Population(tickets)
	sprint = population.run_generation(50, tickets, MUTATION_RATE)
	
if __name__ == '__main__' : main()