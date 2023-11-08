from pysat.solvers import Glucose3

# Exemplo de uso glucose
# g = Glucose3()

# g.add_clause([1, 2])
# g.add_clause([-1, 2])
# g.add_clause([1, -2])
# g.add_clause([-1, -2])

g = Glucose3()

# Mapear os símbolos proposicionais (átomos)
N = 30
counter = 1
mapping_to_int = {}
mapping_to_int_inv = {}
positions = [[i,j] for i in range(1,N+1) for j in range(1,N+1)]
for position in positions:
    key = f"Q_{position[0]}_{position[1]}"
    mapping_to_int[key] = counter
    mapping_to_int_inv[counter] = key
    counter += 1

# Cada linha possui pelo menos uma rainha
for i in range(1,N+1):
    line = []
    for j in range(1, N+1):
        line.append(mapping_to_int[f"Q_{i}_{j}"])
    g.add_clause(line)

# Cada coluna possui no máximo uma rainha
for j in range(1, N+1):
    for i in range(1, N+1):
        other_indexes = list(range(1, N+1))
        other_indexes.remove(i)
        for other in other_indexes:
            # Q_i_j -> ~Q_k_j === ~Q_i_j v ~Q_k_j
            clause = [-mapping_to_int[f"Q_{i}_{j}"], -mapping_to_int[f"Q_{other}_{j}"]]
            g.add_clause(clause)

# Cada diagonal principal possui no máximo uma rainha
for d in range(1 - N, N):
    for i in range(1, N+1):
        if 1 <= i + d <= N:
            other_indexes = list(range(1, N+1))
            other_indexes.remove(i)
            for other in other_indexes:
                if 1 <= other + d <= N:
                    clause = [-mapping_to_int[f"Q_{i}_{i+d}"], -mapping_to_int[f"Q_{other}_{other+d}"]]
                    g.add_clause(clause)

# Cada diagonal secundária possui no máximo uma rainha
for d in range(2, 2*N+1):
    for i in range(1, N+1):
        if 1 <= d - i <= N:
            other_indexes = list(range(1, N+1))
            other_indexes.remove(i)
            for other in other_indexes:
                if 1 <= d - other <= N:
                    clause = [-mapping_to_int[f"Q_{i}_{d-i}"], -mapping_to_int[f"Q_{other}_{d-other}"]]
                    g.add_clause(clause)

print(g.solve())
print(g.get_model())