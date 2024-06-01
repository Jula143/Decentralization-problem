from docplex.mp.model import Model

mdl = Model(name='decentralization')

CITIES = 3
DEPARTMENTS = 5
id_city = range(0, CITIES)
id_dep = range(0, DEPARTMENTS)

#defining decision variables
delta = mdl.binary_var_dict((i, j)
                       for i in id_dep
                       for j in id_city)
gamma = mdl.binary_var_dict((i, j, k, l)
                       for i in id_dep
                       for j in id_city
                       for k in id_dep
                       for l in id_city)

#Defining parameters
#B -> benefits of relocation (in thousands of pounds)
#C -> quantity of communication between departments per year
#D -> cost per unit of communication between cities
B = [[10, 15, 10, 20, 5],
     [10, 20, 15, 15, 15],
     [0, 0, 0, 0, 0]]

C = [[0.0, 0.0, 1.0, 1.5, 0.0],
     [0.0, 0.0, 1.4, 1.2, 0.0],
     [0.0, 0.0, 0.0, 0.0, 2.0],
     [0.0, 0.0, 0.0, 0.0, 0.7],
     [0.0, 0.0, 0.0, 0.0, 0.0]]

D = [[5, 14, 13],
     [14, 5, 9],
     [13, 9, 10]]


constraints = []

#defining objective function
obj = mdl.sum(-B[j][i] * delta[i, j] for i in id_dep for j in id_city) + \
                mdl.sum(C[k][i] * D[l][j] * gamma[i, j, k, l] for i in id_dep 
                        for j in id_city for k in id_dep for l in id_city)
mdl.minimize(obj)



#defining constraints

#one department in only one city
for i in id_dep:
    con = mdl.add_constraint(mdl.sum(delta[i, j] for j in id_city) == 1)
    constraints.append(con)

#no more than three deps in one city
for j in id_city:
    con = mdl.add_constraint(mdl.sum(delta[i, j] for i in id_dep) <= 3)
    constraints.append(con)

#relating delta to gamma
for i in id_dep:
    for j in id_city:
        for k in id_dep:
            for l in id_city:
                con1 = mdl.add_constraint(gamma[i, j, k, l] - delta[i, j] <= 0) #gamma ijkl = 1 -> delta ij = 1
                con2 = mdl.add_constraint(gamma[i, j, k, l] - delta[k, l] <= 0) #gamma ijkl = 1 -> delta kl = 1
                con3 = mdl.add_constraint(delta[i, j] + delta[k, l] - gamma[i, j, k, l] <= 1) #delta ij = 1, delta kl = 1 -> gamma ijkl= 1
                constraints.append(con1)
                constraints.append(con2)
                constraints.append(con3)
                
#solving the model
mdl.print_information()
model = mdl.solve(log_output=True)

print("Solution status:", mdl.solve_details.status)
print("Objective value:", mdl.objective_value)

deps = ["A","B","C","D","E"]
cities = ["Briston", "Brighton", "London"]
print("Values of delta:")
for i in id_dep:
    for j in id_city:
        if delta[i, j].solution_value==1:
            print(f'{deps[i]} was moved to {cities[j]}')
        
print("Slack values:")        
for constraint in constraints:
    print(f"{constraint}: {constraint.slack_value}") 
    

print("\nConstraints:")
for constraint in mdl.iter_constraints():
    print(constraint)



#gerarating other feasible solutions
mdl.parameters.mip.pool.capacity = 20 
mdl.parameters.mip.limits.populate = 20  

mdl.print_information()
solution = mdl.solve(log_output=True)

solution_pool = mdl.populate_solution_pool()
print(f"Number of solutions in pool: {len(solution_pool)}")

deps = ["A", "B", "C", "D", "E"]
cities = ["Bristol", "Brighton", "London"]

for sol_num, sol in enumerate(solution_pool):
    print(f"Solution #{sol_num + 1}:")
    for i in id_dep:
        for j in id_city:
            if sol[delta[i, j]] == 1:
                print(f'  {deps[i]} was moved to {cities[j]}')
    print(f"Objective value: {sol.objective_value}")
    print("\n")
