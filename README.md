# Shamir's Secret Sharing - Local Python impl with simulated nodes

Shamir's Secret Sharing is a cryptographic algorithm that allows a secret to be divided into shares and distributed among a group of participants. Only a specified threshold number of shares is required to reconstruct the original secret. This implementation demonstrates the usage of Shamir's Secret Sharing algorithm using Flask, Python, and Sympy.

## Features

- Generation of shares for a secret using Shamir's Secret Sharing algorithm
- Distribution of shares among multiple nodes using Flask API
- Reconstruction of the secret using Lagrange interpolation
- Support for different secret sizes (up to 256)
- Simple and extensible implementation

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Flask
- Sympy

### Installation

1. Clone the repository:

```shell
git clone https://github.com/SeriousSurge/shamirs-secret-sharing-dist.git
```

2. Install the required dependencies:

```shell
pip install -r requirements.txt
```

### Usage

1. Start the barrier server:
```shell
python barrier.py
```
2. Start the nodes:
```shell
python nodes.py
```
### How it Works
The barrier server is responsible for coordinating the nodes. It listens for each node to report its readiness and determines when all nodes are ready to proceed.

Each node generates shares of the secret using Shamir's Secret Sharing algorithm. The secret is split into polynomial coefficients, and each node evaluates the polynomial at its unique ID to generate a share.

The nodes use Flask API to distribute their shares to other nodes.

Once a node receives enough shares (threshold: total nodes / 2), it can interpolate the secret using Lagrange interpolation.

The reconstructed secret is compared to the evaluated secret (interpolation using a subset of shares). If they match, the secret is considered correct.
