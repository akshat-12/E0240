import random
import numpy as np
import matplotlib.pyplot as plt

def generate_x():
    u1 = random.random()
    u2 = random.random()

    if u1 < 0.25:
        # Component 1: f1(x) = 3x^2
        return u2 ** (1/3)
    else:
        # Component 2: f2(x) = 2x
        return u2 ** (1/2)


# Generate 10000000 samples
N = 10000000
samples = [generate_x() for _ in range(N)]

# Histogram
plt.hist(samples, bins=50, density=True, alpha=0.7, label="Generated samples")

# Theoretical PDF
x = np.linspace(0, 1, 1000)
pdf = 3 * x * (x + 2) / 4

plt.plot(x, pdf, label="Theoretical PDF")

plt.xlabel("x")
plt.ylabel("Density")
plt.title("Composition Method: f(x) = 3x(x+2)/4")
plt.legend()
plt.savefig("Q1_a_plot.png", dpi=300, bbox_inches="tight")
plt.show()