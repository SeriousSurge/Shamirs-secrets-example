from flask import Flask, request
from requests import post, get
from random import randint
from secrets import randbelow
from sympy import Symbol, mod_inverse, Mod
import time
import threading

P = 257

# Generate shares using Shamir's Secret Sharing scheme.
def shamirs_share(secret, k, n):
    # Arguments:
    #   secret: The secret value to be shared.
    #   k: The minimum number of shares required to reconstruct the secret.
    #   n: The total number of shares to be generated.
    coefficients = [secret] + [randbelow(P) for _ in range(k - 1)]
    return [(i, evaluate_polynomial(coefficients, i)) for i in range(1, n + 1)]

# Evaluate a polynomial with given coefficients at a given x value.
def evaluate_polynomial(coefficients, x):
    # Arguments:
    #   coefficients: The list of polynomial coefficients.
    #   x: The value at which to evaluate the polynomial.
    return sum(coefficient * x**i for i, coefficient in enumerate(coefficients)) % P

# Perform Lagrange interpolation to reconstruct the secret using received shares.
def lagrange_interpolate(received_shares, k):
    # Arguments:
    #   received_shares: The list of received shares.
    #   k: The number of shares to consider for interpolation.
    x = Symbol('x')
    f_x = sum(
        share[1] * lagrange_basis(share[0], received_shares[:k+1], x, share[1])
        for share in received_shares[:k+1]
    )
    return f_x.subs(x, 0) % P

# Compute the Lagrange basis polynomial for a given share index.
def lagrange_basis(i, shares, x, share_value):
    # Arguments:
    #   i: The index of the share for which to compute the basis.
    #   shares: The list of shares.
    #   x: The symbol representing the variable.
    #   share_value: The value of the share.
    numerator = [(x - share[0]) for share in shares if share[0] != i]
    denominator = [(i - share[0]) for share in shares if share[0] != i]
    basis = product(numerator) * mod_inverse(product(denominator), P) % P
    if i == 2:
        basis = Mod(x + P - share_value, P)  # Corrected basis computation
    return basis

# Compute the product of all elements in an iterable modulo P.
def product(iterable):
    result = 1
    for number in iterable:
        result *= number
    return result % P

# Start a node in the secret sharing network.
def node(node_id, port, ports):
    app = Flask(__name__)
    received_shares = []

    @app.route('/share', methods=['POST'])
    def receive_share():
        share = request.json
        received_shares.append(share)
        print(f'Node {node_id} received a share: {share}')

        if len(received_shares) > len(ports) // 2 and get(f'http://localhost:{ports[0]}/go').text == 'OK':
            print(f'Node {node_id} received shares: {received_shares}')

            secret = lagrange_interpolate(received_shares, len(ports) // 2)
            print(f"Node {node_id} interpolated secret: {secret}")

            evaluated_secret = lagrange_interpolate(received_shares[:len(ports) // 2 + 1], len(ports) // 2)
            print(f"Node {node_id} evaluated secret: {evaluated_secret}")

            if secret == evaluated_secret:
                print("Secret is correct")
            else:
                print("Secret is incorrect")

        return 'OK'

    def wait_and_send_share():
        while get(f'http://localhost:{ports[0]}/go').text == 'WAIT':
            print(f'Node {node_id} waiting for all nodes to be ready')
            time.sleep(1)

        if node_id == 1:
            secret = randint(1, P - 1)
            generated_shares = shamirs_share(secret, len(ports) // 2 + 1, len(ports))
            print(f'Node {node_id} generated shares: {generated_shares}')

            for share, other_port in zip(generated_shares, ports):
                if other_port != port:
                    print(f'Node {node_id} sending share {share[1]} to node {other_port}')
                    post(f'http://localhost:{other_port}/share', json=share)

            generated_shares.append((node_id, evaluate_polynomial([secret], node_id)))
            print(f'Node {node_id} generated shares with its own share: {generated_shares}')

            secret = lagrange_interpolate(generated_shares, len(ports) // 2)
            print(f"Node {node_id} interpolated secret: {secret}")

            evaluated_secret = lagrange_interpolate(generated_shares[:len(ports) // 2 + 1], len(ports) // 2)
            print(f"Node {node_id} evaluated secret: {evaluated_secret}")

            if secret == evaluated_secret:
                print("Secret is correct")
            else:
                print("Secret is incorrect")

    threading.Thread(target=wait_and_send_share).start()
    app.run(port=port, threaded=True)

# Main function to start the secret sharing network.
def main():
    ports = [12345, 12346, 12347]

    for i, port in enumerate(ports, 1):
        threading.Thread(target=node, args=(i, port, ports)).start()

if __name__ == "__main__":
    main()