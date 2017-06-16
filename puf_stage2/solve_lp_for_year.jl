using DataFrames
using JuMP
using Clp

A1 = readdlm("A1.csv", ',',header = true)[1]
A2 = readdlm("A2.csv", ',', header = true)[1]
b = readdlm("b.csv", ',', header = true)[1]

tol = 0.45

dim = size(A1)

m = Model(solver = ClpSolver())
@variable(m, r[1:dim[2]])
@variable(m, r >= 0)
@variable(m, s[1:dim[2]])
@variable(m, s >= 0)

c = ones(dim[2])
@objective(dot(r, c) + dot(s, c))
@constraint(m, r + s <= tol)
@constraint(m , dot(r, A1) + dot(s, A2) == b)


sol = solve(m)

print (sol)
