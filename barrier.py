from flask import Flask, request

def barrier(port, total):
    # Initialize the Flask application
    app = Flask(__name__)

    # Keep track of how many nodes have reached the barrier
    count = 0

    @app.route('/ready', methods=['POST'])
    def ready():
        # Increment the count when a node reports readiness
        nonlocal count
        count += 1
        print(f'Node reported readiness. Total ready nodes: {count}')
        return 'OK'

    @app.route('/go', methods=['GET'])
    def go():
        # Check if the number of ready nodes has reached the total
        if count >= total:
            return 'OK'
        else:
            return 'WAIT'

    # Run the Flask server
    app.run(port=port)

if __name__ == "__main__":
    barrier(12344, 3)  # you should adjust the number of nodes accordingly
