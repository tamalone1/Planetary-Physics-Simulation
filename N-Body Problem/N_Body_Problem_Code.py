import math
import matplotlib.pyplot as plt
import numpy.random as rand

plt.rcParams['figure.dpi'] = 280


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def magnitude(self):
        mag = math.hypot(self.x, self.y)
        return mag

    def add(self, vector):
        """ Add the x and y components, and return a new Vector. """
        xf = self.x + vector.x
        yf = self.y + vector.y
        return Vector(xf, yf)

    def __add__(self, vector):
        """ Add the x and y components, and return a new Vector. """
        # Check if the vector parameter is a Vector or a scalar
        if isinstance(vector, Vector):
            # the parameter is a Vector, add the components
            xf = self.x + vector.x
            yf = self.y + vector.y
        elif not hasattr(vector, '__len__'):
            # the vector parameter is a scalar, add it to each component
            xf = self.x + vector
            yf = self.y + vector
        else:
            return NotImplemented
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
        # Note that momentum should not be a vector.
        self.momentum = vel.s_multiply(self.m)
        self.accel = None

    def force(self, planet):
        # Initialize the force vector at 0
        force_vector = Vector(0, 0)
        G = 0.004
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
                if dist < self.r:
                    force_vector1 = force_vector1.s_multiply(-1)
                # Add the result to the total force vector
                force_vector = force_vector.add(force_vector1)
        # return the force vector negated?
        return force_vector.s_multiply(-1)


def simulate(planets, nsteps):
    # Time resolution delta t
    dt = 0.001
    # Number of calculation steps
    X = [[] for i in range(len(planets))]
    Y = [[] for i in range(len(planets))]
    # loop through the number of steps, counting down from initial steps value
    for step in range(nsteps):
        # for each planet, by index
        for i in range(len(planets)):
            # Acceleration = F/m
            planets[i].accel = planets[i].force(planets).s_multiply(1/planets[i].m)
            # Velocity changes by accel*dt
            planets[i].vel = planets[i].vel.add(planets[i].accel.s_multiply(dt))
            # planet's position changes by momentum*dt/mass = v*dt
            planets[i].pos = planets[i].pos.add(planets[i].vel.s_multiply(dt))
            # Add each position component to the position lists for this planet
            X[i].append(planets[i].pos.x)
            Y[i].append(planets[i].pos.y)
    return X, Y


def main(nbodies, nsteps):
    # List of all the planets
    planets = []
    # Create n randomly generated planets
    for i in range(nbodies):
        # Create a list of 4 random numbers 0-1 for pos and vel components
        a = rand.random(4)/2
        p = Planet(10,
                   0.001,
                   Vector(a[0], a[1]),
                   Vector(a[2], a[3]),
                   str(i))
        planets.append(p)
    X, Y = simulate(planets, nsteps)
    fig1, ax = plt.subplots()
    ax.set_aspect('equal')
    # for each planet, plot the position components over time
    for i in range(len(planets)):
        ax.plot(X[i], Y[i])
        ax.scatter(X[i][-1], Y[i][-1], s=30)
    ax.set_title(f'N Body Problem (n = {nbodies})')
    plt.show()


if __name__ == '__main__':
    main(nbodies=2, nsteps=5000)
