from docplex.mp.model import Model

mdl = Model(name='decentralization')

CITIES = 3
DEPARTMENTS = 5
id_city = range(0, CITIES)
id_dep = range(0, DEPARTMENTS)

#Defining decision variables
delta = mdl.binary_var_dict((i, j)
                       for i in id_dep
                       for j in id_city)
omega = mdl.binary_var_dict((i, j, k, l)
                       for i in id_dep
                       for j in id_city
                       for k in id_dep
                       for l in id_city)

#Defining parameters
#B -> benefits of relocation  
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

#Defining objective function
obj = mdl.sum(-B[j][i] * delta[i, j] for i in id_dep for j in id_city) + mdl.sum(C[k][i] * D[l][j] * omega[i, j, k, l] for i in id_dep for j in id_city for k in id_dep for l in id_city)
mdl.minimize(obj)

#Defining constraints
for i in id_dep:
    con = mdl.add_constraint(mdl.sum(delta[i, j] for j in id_city) == 1)
    constraints.append(con)

for j in id_city:
    con = mdl.add_constraint(mdl.sum(delta[i, j] for i in id_dep) <= 3)
    constraints.append(con)

for i in id_dep:
    for j in id_city:
        for k in id_dep:
            for l in id_city:
                con1 = mdl.add_constraint(omega[i, j, k, l] - delta[i, j] <= 0)
                con2 = mdl.add_constraint(omega[i, j, k, l] - delta[k, l] <= 0)
                con3 = mdl.add_constraint(delta[i, j] + delta[k, l] - omega[i, j, k, l] <= 1)
                constraints.append(con1)
                constraints.append(con2)
                constraints.append(con3)
                
#Solving the model
#mdl.print_information()
model = mdl.solve(log_output=False)
#s = model.display()

print("Solution status:", mdl.solve_details.status)
print("Objective value:", mdl.objective_value)

print("Values of delta:")
for i in id_dep:
    for j in id_city:
        print(f"delta[{i},{j}]: {delta[i, j].solution_value}")
        
print("Slack values:")        
for constraint in constraints:
    print(f"{constraint}: {constraint.slack_value}") 
    
#not working for binary, continuous give results    
# print("Dual values:")        
# for constraint in constraints:
#     print(f"{constraint}: {constraint.dual_value}") 
        
print(model.get_reduced_costs(delta))
print(model.get_reduced_costs(omega))
#not available for mixed integer programming   
#for continuous gives vector of 0's    
        
  