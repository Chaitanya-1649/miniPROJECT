import random

def create_graph():
    A = (16.3067, 80.4365)
    B = (16.3100, 80.4400)
    C = (16.3150, 80.4450)
    D = (16.3200, 80.4500)

    traffic_data = {
        (A, B): random.randint(10, 60),
        (A, C): random.randint(10, 80),
        (B, D): random.randint(20, 90),
        (C, D): random.randint(5, 70)
    }

    graph = {
        A: [(B, 2), (C, 4)],
        B: [(A, 2), (D, 7)],
        C: [(A, 4), (D, 3)],
        D: [(B, 7), (C, 3)]
    }

    return graph, traffic_data
