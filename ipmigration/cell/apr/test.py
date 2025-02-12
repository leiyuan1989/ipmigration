from ortools.sat.python import cp_model





model = cp_model.CpModel()

# Creates the variables.
num_vals = 3
x = model.new_int_var(0, 10 - 1, "x")
y = model.new_int_var(0, 8 - 1, "y")
z = model.new_int_var(0, 5 - 1, "z")



model.add(x != y)
model.add(x != z)
model.add(x != z)

# model.add_bool_or([x==3,y==4])

solver = cp_model.CpSolver()

solution_printer = VarArraySolutionPrinter([x, y, z])
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True
# Solve.
status = solver.solve(model, solution_printer)



class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count


def search_for_all_solutions_sample_sat():
    """Showcases calling the solver to search for all solutions."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    num_vals = 3
    x = model.new_int_var(0, num_vals - 1, "x")
    y = model.new_int_var(0, num_vals - 1, "y")
    z = model.new_int_var(0, num_vals - 1, "z")

    # Create the constraints.
    model.add(x != y)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([x, y, z])
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.solve(model, solution_printer)

    print(f"Status = {solver.status_name(status)}")
    print(f"Number of solutions found: {solution_printer.solution_count}")


search_for_all_solutions_sample_sat()



"""Simple solve."""
from ortools.sat.python import cp_model


def main() -> None:
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    var_upper_bound = max(50, 45, 37)
    x = model.new_int_var(0, var_upper_bound, "x")
    y = model.new_int_var(0, var_upper_bound, "y")
    z = model.new_int_var(0, var_upper_bound, "z")

    # Creates the constraints.
    model.add(2 * x + 7 * y + 3 * z <= 50)
    model.add(3 * x - 5 * y + 7 * z <= 45)
    model.add(5 * x + 2 * y - 6 * z <= 37)

    model.maximize(2 * x + 2 * y + 3 * z)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Maximum of objective function: {solver.objective_value}\n")
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("No solution found.")

    # Statistics.
    print("\nStatistics")
    print(f"  status   : {solver.status_name(status)}")
    print(f"  conflicts: {solver.num_conflicts}")
    print(f"  branches : {solver.num_branches}")
    print(f"  wall time: {solver.wall_time} s")


if __name__ == "__main__":
    main()
    
"""OR-Tools solution to the N-queens problem."""
import sys
from ortools.constraint_solver import pywrapcp


def main(board_size):
    # Creates the solver.
    solver = pywrapcp.Solver("n-queens")

    # Creates the variables.
    # The array index is the column, and the value is the row.
    queens = [solver.IntVar(0, board_size - 1, f"x{i}") for i in range(board_size)]

    # Creates the constraints.
    # All rows must be different.
    solver.Add(solver.AllDifferent(queens))

    # No two queens can be on the same diagonal.
    solver.Add(solver.AllDifferent([queens[i] + i for i in range(board_size)]))
    solver.Add(solver.AllDifferent([queens[i] - i for i in range(board_size)]))

    db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

    # Iterates through the solutions, displaying each.
    num_solutions = 0
    solver.NewSearch(db)
    while solver.NextSolution():
        # Displays the solution just computed.
        for i in range(board_size):
            for j in range(board_size):
                if queens[j].Value() == i:
                    # There is a queen in column j, row i.
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()
        num_solutions += 1
    solver.EndSearch()

    # Statistics.
    print("\nStatistics")
    print(f"  failures: {solver.Failures()}")
    print(f"  branches: {solver.Branches()}")
    print(f"  wall time: {solver.WallTime()} ms")
    print(f"  Solutions found: {num_solutions}")


if __name__ == "__main__":
    # By default, solve the 8x8 problem.
    size = 8
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    main(size)
    
    




#!/usr/bin/env python3
# Copyright 2010-2024 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Link integer constraints together."""


from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables

    def on_solution_callback(self) -> None:
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()


def channeling_sample_sat():
    """Demonstrates how to link integer constraints together."""

    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Declare our two primary variables.
    x = model.new_int_var(0, 10, "x")
    y = model.new_int_var(0, 10, "y")

    # Declare our intermediate boolean variable.
    b = model.new_bool_var("b")

    # Implement b == (x >= 5).
    model.add(x >= 5).only_enforce_if(b)
    model.add(x < 5).only_enforce_if(~b)

    # Create our two half-reified constraints.
    # First, b implies (y == 10 - x).
    model.add(y == 10 - x).only_enforce_if(b)
    # Second, not(b) implies y == 0.
    model.add(y == 0).only_enforce_if(~b)

    # Search for x values in increasing order.
    model.add_decision_strategy([x], cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)

    # Create a solver and solve with a fixed search.
    solver = cp_model.CpSolver()

    # Force the solver to follow the decision strategy exactly.
    solver.parameters.search_branching = cp_model.FIXED_SEARCH
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True

    # Search and print out all solutions.
    solution_printer = VarArraySolutionPrinter([x, y, b])
    solver.solve(model, solution_printer)


channeling_sample_sat()





#!/usr/bin/env python3
# Copyright 2010-2024 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Solves a binpacking problem using the CP-SAT solver."""


from ortools.sat.python import cp_model


def binpacking_problem_sat():
    """Solves a bin-packing problem using the CP-SAT solver."""
    # Data.
    bin_capacity = 100
    slack_capacity = 20
    num_bins = 5
    all_bins = range(num_bins)

    items = [(20, 6), (15, 6), (30, 4), (45, 3)]
    num_items = len(items)
    all_items = range(num_items)

    # Model.
    model = cp_model.CpModel()

    # Main variables.
    x = {}
    for i in all_items:
        num_copies = items[i][1]
        for b in all_bins:
            x[(i, b)] = model.new_int_var(0, num_copies, f"x[{i},{b}]")

    # Load variables.
    load = [model.new_int_var(0, bin_capacity, f"load[{b}]") for b in all_bins]

    # Slack variables.
    slacks = [model.new_bool_var(f"slack[{b}]") for b in all_bins]

    # Links load and x.
    for b in all_bins:
        model.add(load[b] == sum(x[(i, b)] * items[i][0] for i in all_items))

    # Place all items.
    for i in all_items:
        model.add(sum(x[(i, b)] for b in all_bins) == items[i][1])

    # Links load and slack through an equivalence relation.
    safe_capacity = bin_capacity - slack_capacity
    for b in all_bins:
        # slack[b] => load[b] <= safe_capacity.
        model.add(load[b] <= safe_capacity).only_enforce_if(slacks[b])
        # not(slack[b]) => load[b] > safe_capacity.
        model.add(load[b] > safe_capacity).only_enforce_if(~slacks[b])

    # Maximize sum of slacks.
    model.maximize(sum(slacks))

    # Solves and prints out the solution.
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    print(f"solve status: {solver.status_name(status)}")
    if status == cp_model.OPTIMAL:
        print(f"Optimal objective value: {solver.objective_value}")
    print("Statistics")
    print(f"  - conflicts : {solver.num_conflicts}")
    print(f"  - branches  : {solver.num_branches}")
    print(f"  - wall time : {solver.wall_time}s")


binpacking_problem_sat()