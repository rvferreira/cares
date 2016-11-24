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
NUMBER_OF_GENERATIONS 				= 50

def cria_tickets_aleatorios(numero_de_tickets):
	seed()
	tickets = []
	for key in range(numero_de_tickets):
		dependencias = []
		dependentes = []
		pontos = 1+randrange(0, 10, 1)
		numero_de_dependencias = randrange(0, 3, 1)
		importancia = 1+randrange(0, 100, 1)

		for i in range(numero_de_dependencias):
			dependencia = randrange(0, numero_de_tickets, 1)
			dependencias.append(dependencia)

		tickets.append(Ticket(dependencias, key, key, importancia, pontos))

	return tickets

class Ticket:

	def __init__(self, dependencies, key, iid, importance, estimated_time):
		self.dependencies = dependencies
		self.key = key
		self.importance = importance
		self.estimated_time = estimated_time
		self.id = iid

	def saveDependents(self, dependents):
		self.number_of_dependents = dependents

	def computeTicketFitness(self, keys_inside_sprint):

		penalty_multiplier = 1;
		for dependency in self.dependencies:
			if dependency in keys_inside_sprint:
				penalty_multiplier-= IN_SPRINT_DEPENDENCY_PENALTY
			else:
				penalty_multiplier-= OUT_OF_SPRINT_DEPENDENCY_PENALTY

		bonus_multiplier = 1;
		
		bonus_multiplier+= HAS_DEPENDANTS_BONUS*self.number_of_dependents

		if penalty_multiplier<0:
			return 0

		return self.importance*bonus_multiplier*penalty_multiplier

class Sprint:
	def ticket_array(self):
		return self.tickets

	def fitness(self):
		return self.fitness

	def __init__(self, all_tickets):#all_tickets devem estar organizados por points, de menos pra mais.
		time_left = SPRINT_HOURS_TIME_SLOTS;
		tickets = []
		tickets_left = all_tickets[:]


		while time_left > 0 and len(tickets_left)>0:
			selected_ticket = choice(tickets_left)

			if selected_ticket.estimated_time > time_left:#nao cabe
				ticket_out = tickets_left.pop()
				while ticket_out.estimated_time > time_left:#enquanto existir um q nao cabe
					if (len(tickets_left)==0):
						self.tickets = tickets
						self.fitness = 0
						return
					ticket_out = tickets_left.pop()
				tickets_left.append(ticket_out)
				selected_ticket = choice(tickets_left)
			
			tickets.append(selected_ticket)
			tickets_left.remove(selected_ticket)
			time_left -= selected_ticket.estimated_time

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


class Population:
	def __init__(self, all_tickets):
		self.population = []
		for i in range(INITIAL_POPIULATION_SIZE):
			self.population.append(Sprint(all_tickets))
		self.population_size = INITIAL_POPIULATION_SIZE

	def computeFitness(self):
		for sprint in self.population:
			sprint.computeSprintFitness()
		(self.population).sort(key=attrgetter('fitness'))

	def printFitness(self):
		print('{0}'.format(self.population[INITIAL_POPIULATION_SIZE-1].fitness))

	def parents_select(self):
		#Type of selection: Prioritizes best parents.
		#Returns a vector, with the tickets(chromossomes) of each selected parent
		first_parent_roll = 0.8 ** (randrange(0, 100)/(-5.077) - 1) - 1.2
		second_parent_roll = 0.8 ** (randrange(0, 100)/(-5.077) - 1) - 1.2

		# normalizing for population size
		first_parent_roll = self.population_size - 1 - int((first_parent_roll / 100.0) * len(self.population))
		second_parent_roll = self.population_size - 1 - int((second_parent_roll / 100.0) * len(self.population))

		first_parent = self.population[first_parent_roll]
		second_parent = self.population[second_parent_roll]

		return first_parent.ticket_array()+second_parent.ticket_array()

	def crossover(self):
		child_tickets = []
		temp_parent = self.parents_select()
		parent = temp_parent[:]

		time_left = SPRINT_HOURS_TIME_SLOTS

		#Each chromossome of child is a copy of parent's chromossome, parent randomly chosen:
		while time_left > 0 and len(parent)>0:
			dice = randrange(0, len(parent))
			ticket = parent[dice]
			if ticket not in child_tickets:
				child_tickets.append(ticket)
				time_left -= ticket.estimated_time
				if time_left <= 0:
					return Sprint(child_tickets)
			parent.remove(ticket)

		return Sprint(child_tickets)

	def mutation(self, children, all_tickets, mutation_rate, mutation_intensity):
		#Mutation Mode: Plus_Minus
		temporary_population = []

		for sprint in children:
			new_tickets = []

			for ticket in sprint.tickets:
				chance = randrange(0, 100)/100.0
				if chance<=mutation_rate: #ocorre mutacao
					if randrange(0,2)==1:
						if ticket.key+mutation_intensity < len(all_tickets):
							new_tickets.append(all_tickets[ticket.key+mutation_intensity])
						else:
							new_tickets.append(all_tickets[ticket.key+mutation_intensity - len(all_tickets) - 1])
					else:
						if ticket.key-mutation_intensity>=0:
							new_tickets.append(all_tickets[ticket.key-mutation_intensity])
						else:
							new_tickets.append(all_tickets[len(all_tickets) + ticket.key-mutation_intensity])
				else:
					new_tickets.append(ticket)

			temporary_population.append(Sprint(new_tickets))
		children = temporary_population

	def createChildren(self, all_tickets, mutation_rate, mutation_intensity):
		children = []
		for i in range(self.population_size):
			children.append(self.crossover())
		self.mutation(children, all_tickets, mutation_rate, mutation_intensity)

		return children

	def evolve(self, all_tickets, mutation_rate, mutation_intensity):
		self.computeFitness()
		self.population += self.createChildren(all_tickets, mutation_rate, mutation_intensity)
		self.computeFitness()
		self.population = self.population[self.population_size : self.population_size*2]

	def run_generations(self, number_of_generations, all_tickets):
		mutation_intensity = MUTATION_INTENSITY
		mutation_rate = MUTATION_RATE

		for i in range(number_of_generations):
			self.evolve(all_tickets, mutation_rate, mutation_intensity)
			self.printFitness()

		return self.population[INITIAL_POPIULATION_SIZE-1].ticket_array()


def getId(array):
	ids = []

	for ticket in array:
		ids.append(ticket.id)

	return ids

def setDependents(array):
	for ticket in array:
		dependents = 0
		for dep in array:
			if ticket.id in dep.dependencies:
				dependents += 1
		ticket.saveDependents(dependents)

def main(ext_tickets):
	all_tickets = []
	all_time = 0
	for i in range(len(ext_tickets)):
		obj = ext_tickets[i]
		all_time += obj.estimated_time
		all_tickets.append(Ticket(obj.dependencies, i, obj.id, obj.importance, obj.estimated_time))


	if all_time <= SPRINT_HOURS_TIME_SLOTS:
		return getId(all_tickets)

	all_tickets.sort(key=attrgetter('estimated_time'))

	setDependents(all_tickets)

	population = Population(all_tickets)

	return getId(population.run_generations(NUMBER_OF_GENERATIONS, all_tickets))


if __name__ == '__main__' : main()