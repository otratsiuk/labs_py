from numpy import random, mean, std
from numpy.lib import scimath

import matplotlib.pyplot as plt

from typing import List, Callable


def find_borders(c, d):
    a = c - 2 * scimath.sqrt(3*d)
    b = 2 * c - a
    return a, b


def uniform_distribution(c, d):
    a, b = find_borders(c, d)
    r = random.random()
    return a + (b - a) * r


def make_positive(x):
    if x < 0:
        x = 0

    return x


test_probability = make_positive(random.exponential(3.5))
infectiousness = make_positive(random.normal(20, 2.5))
infected_start_number = random.randint(5, 10)
treatment_eff = make_positive(uniform_distribution(10, 2.5))
average_age = make_positive(random.normal(25, 5.5))
first_day_infected_num = random.randint(5, 10)


print('infectiousness: ' + str(infectiousness))


class Agent:
    def __init__(self):
        self.infection_day = 1
        self.status = 'infected'

    def set_m(self):
        self.m = make_positive(uniform_distribution(0, 50))

    def set_health(self):
        self.health = make_positive(random.normal(6, 0.5))
        self.treatment_probability = 0.01
        if self.health < 2:
            self.treatment_probability = 0.1

    def set_death_rate(self, age, health, treatment_eff):
        self.death_rate = make_positive(age*0.09 + random.normal(
            5 - 0.35*health - 0.3 * treatment_eff, make_positive(2 - 0.3 * health - 0.15*treatment_eff)))

    def set_status(self):
        test_chance = random.uniform(0, 100)
        treatment_chance = random.random()
        death_chance = random.uniform(0, 100)
        if test_chance <= test_probability:
            self.status = 'revealed'
        else:
            self.status = 'unrevealed'
        if treatment_chance <= self.treatment_probability:
            self.status = 'on_treatment'
        if death_chance <= self.death_rate:
            self.status = 'dead'

    def set_responsibility(self):
        self.responsibility = make_positive(random.normal(10, 0.1))

    def set_sc(self, m):
        self.social_contacts = make_positive(uniform_distribution(m, 6))
        if self.status == 'revealed' and self.responsibility != 0:
            self.social_contacts = self.social_contacts / self.responsibility

    def set_age(self, m):
        self.age = make_positive(random.normal(m, 20))

    def set_recovery_time(self, health, treatment_eff):
        self.recovery_time = make_positive(round(4 + uniform_distribution(
            25 - 2.0*health - 0.2*treatment_eff, 2 - 0.1*health)))


def create_agent() -> Agent:
    agent = Agent()
    agent.set_m()
    agent.set_sc(agent.m)
    agent.set_responsibility()
    agent.set_health()
    agent.set_age(agent.m)
    agent.set_death_rate(agent.age, agent.health, treatment_eff)
    agent.set_recovery_time(agent.health, treatment_eff)
    agent.infection_day = 0
    return agent


def create_agents(count: int) -> List[Agent]:
    return [create_agent() for _ in range(count)]


first_day_infected = create_agents(first_day_infected_num)
print('first day infected: ' + str(first_day_infected_num))


MAX_DAYS = 12
current_day = 1


def infected_by_agent_count(social_contacts):
    infected_by_agent_count = 0
    infected_by_agent_count = infectiousness * social_contacts / 100
    return infected_by_agent_count


def next_day(day: int, agents: List[Agent], callback: Callable):
    callback(day, agents)
    if day == MAX_DAYS:
        return

    infected_count = 0
    infected_by_agent = 0

    for agent in agents:
        infected_by_agent = infected_by_agent_count(agent.social_contacts)
        infected_count = infected_count + infected_by_agent

    callback(day, agents)

    new_agents = create_agents(int(round(infected_count)))
    next_day(day + 1, agents + new_agents, callback)


infected = []
days = []


def callback_func(day, agents):
    days.append(day)
    infected.append(len(agents))


next_day(current_day, first_day_infected, callback_func)


plt.title('infected growth chart')
plt.plot(days, infected)
plt.xlabel('day')
plt.ylabel('infected')
plt.show()


simulation = []
MAX_DAYS = 10
current_day = 1

for i in range(5):
    next_day(current_day, first_day_infected,
             lambda day, agents: simulation.append(len(agents)) if day == MAX_DAYS else None)


expectation = mean(simulation)
standart_deviation = std(simulation)


print('expectation on 10th day: ' + str(expectation))
print('standart deviation on 10th day: ' + str(standart_deviation))
