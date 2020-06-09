import math
from matplotlib import pyplot as plt
import numpy.random as rand


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def magnitude(self):
        mag = math.sqrt(self.x ** 2 + self.y ** 2)
        return mag

    def add(self, vector):
        """ Add the x and y components, and return a new Vector. """
        xf = self.x + vector.x
        yf = self.y + vector.y
        return Vector(xf, yf)

    def subtract(self, vector):
        """ Subtract other Vector from this vector, return a new Vector. """
        xf = self.x - vector.x
        yf = self.y - vector.y
        return Vector(xf, yf)

    def v_multiply(self, vector):
        """ Multiply two Vectors by components. """
        xf = self.x * vector.x
        yf = self.y * vector.y
        return Vector(xf, yf)

    def s_multiply(self, c):
        """ Multiply this Vector by a scalar. """
        xf = self.x * c
        yf = self.y * c
        return Vector(xf, yf)


class Planet:
    def __init__(self, mass, radius, pos, vel, name):
        self.name = name
        self.r = radius
        self.m = mass
        # pos parameter is a Vector
        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        self.vel = vel
        # Momentum equals mass*velocity
        self.momentum = vel.s_multiply(self.m)

    def force(self, planet):
        # Initialize the force vector at 0
        force_vector = Vector(0, 0)
        G = 0.1
        e = 0.0001
        # neg_vector unused
        # neg_vector = self.pos.s_multiply(-1)
        # parameter planet is a list of all planets to check
        for i in range(len(planet)):
            # check if the planet i is the current planet
            if planet[i].name != self.name:
                # distance vector between planets = current pos - pos[i]
                # dot notation: use Vector.subtract method from pos
                # distance Vector points from current planet to planet[i]
                dist_vec = self.pos.subtract(planet[i].pos)
                # distance magnitude
                dist = dist_vec.magnitude()
                # F vector = G*m1*m2/(r+e)**3 * distance vector
                # e = small additive value, unknown
                # distvec/dist**3 gives the unit vector divided by dist**2
                force_vector1 = dist_vec.s_multiply(G * planet[i].m * self.m / (dist + e) ** 3)
                # if the distance is less than the current planet's radius,
                # make the force negative (magnitude still the same?)
                # if dist < self.r:
                #    force_vector1 = force_vector1.s_multiply(-1)
                # Add the result to the total force vector
                force_vector = force_vector.add(force_vector1)
        # return the force vector negated?
        return force_vector.s_multiply(-1)


def main(n):
    # Time resolution delta t
    dt = 0.001
    # List of all the planets
    planet = []
    # Create n randomly generated planets
    for i in range(n):
        # Create a list of 4 random numbers 0-1 for pos and vel components
        a = rand.random(4)
        p = Planet(rand.randint(1, 5),
                   0.001,
                   Vector(a[0], a[1]),
                   Vector(a[2], a[3]),
                   str(i))
        planet.append(p)
    # p1 = Planet(100, 0.001, Vector(0.1, 0.2), Vector(0.5, 0.75), 'p1')
    # p2 = Planet(1, 0.001, Vector(0.2, 0.1), Vector(0.2, 0.5), 'p2')
    # p3 = Planet(1, 0.001, Vector(0.2, 0.15), Vector(0.75, 1), 'p3')
    # p4 = Planet(1, 0.001, Vector(0.15, 0.15), Vector(0.75, 0.75), 'p4')
    # planet = [p1, p2, p3, p4]
    # Number of calculation steps
    steps = 2000
    X = []
    Y = []
    for i in range(len(planet)):
        # for each planet, add a list to X and Y lists
        # replace this block with list comprehensions ?
        # X = [[] for i in range(len(planet))]
        X.append([])
        Y.append([])
    # loop through the number of steps, counting down from initial steps value
    for step in range(steps):
        # for each planet, by index
        for i in range(len(planet)):
            # planet's momentum changes by F*dt
            planet[i].momentum = planet[i].momentum.add(planet[i].force(planet).s_multiply(dt))
            # planet's position changes by momentum*dt/mass = v*dt
            planet[i].pos = planet[i].pos.add((planet[i].momentum.s_multiply(dt)).s_multiply(1/planet[i].m))
            # Add each position component to the position lists for this planet
            X[i].append(planet[i].pos.x)
            Y[i].append(planet[i].pos.y)
    # for each planet, plot the position components over time
    for i in range(len(planet)):
        plt.plot(X[i], Y[i])
        plt.scatter(X[i][-1], Y[i][-1], s=30)
    plt.title('N Body Problem (n = ' + str(n) + ')\n')
    plt.show()

if __name__ == '__main__':
    main(3)
