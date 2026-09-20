import numpy as np
import matplotlib.pyplot as plt
from math import comb

# Parameters
n = 30
p = 0.4
N = 10000000

# --------------------------------------------------
# Convolution method
# X = X1 + X2 + ... + X30
# Each Xi ~ Bernoulli(p)
# --------------------------------------------------

samples = []

for _ in range(N):

    # Generate 30 Bernoulli random variables
    bernoulli_variables = np.random.binomial(1, p, n)

    # Add them (convolution)
    X = np.sum(bernoulli_variables)

    samples.append(X)

samples = np.array(samples)

# --------------------------------------------------
# Empirical PMF from generated samples
# --------------------------------------------------

x = np.arange(n + 1)

empirical_pmf = np.bincount(
    samples,
    minlength=n + 1
) / N

# --------------------------------------------------
# Theoretical Binomial PMF
#
# P(X=x) = C(n,x) p^x (1-p)^(n-x)
# --------------------------------------------------

theoretical_pmf = np.array([
    comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    for k in x
])

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(10, 6))

# Generated PMF
plt.bar(
    x,
    empirical_pmf,
    alpha=0.6,
    label="Generated samples"
)

# Theoretical PMF
plt.plot(
    x,
    theoretical_pmf,
    'o-',
    linewidth=2,
    label="Theoretical Binomial PMF"
)

plt.xlabel("x")
plt.ylabel("P(X = x)")
plt.title("Verification of Binomial(30, 0.4) using Convolution")

plt.xticks(x)
plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.savefig("Q1_b_plot.png", dpi=300, bbox_inches="tight")
plt.show()
