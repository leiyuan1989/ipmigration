#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:03:52 2024

@author: shunqidai
modified MyProblem and class Optimizer:
    MyProblem:
        modified _evaluate: 
            add simulation result check
            total_area_index
        
    Optimizer:
        self.num_design_variables=len(self.bounds)
        self.population_size
        self.num_offsprings
        
        use homemade sbx and pm:
            from operator_cust.sbx_homemade import SBX
            operator_cust.pm_homemade
            convert float to int
29/08/2024

self.simulationFun_dict in Optimizer will be a two level dict
self.simulationFun in Optimizer will be a dict
simulation in MyProblem will be a dict


each circuit simulates all corners
add _get_history() method in Optimizer class
from operator_cust.sampling.lhs_integer import LHS
30/08/2024

modified evaluate:
    sum the loss of all corners for each metric as the result
13/09/2024

modified setup_and_update_prediction_models:
    corners
    path_state_dict
    import ml_predictor

13/11/2024
modified calculate_result:
    #result[result>=0.99]=10 #let unsaticied item be large
    ----->
    result_new_tmp=result.copy()
    for i in range(len(result_new_tmp)):
        item=result_new_tmp[i]
        if item>=0.99:
            #item=10*item*np.exp(item-1)
            item=item+10
            result_new_tmp[i]=item
    result=result_new_tmp
    
Dec 06
add DEHomemadeOptimizer
"""
import numpy as np
import time
import os

from pymoo.core.problem import Problem
from pymoo.problems.static import StaticProblem
from pymoo.core.evaluator import Evaluator
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.rvea import RVEA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM

from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.core.termination import NoTermination
from pymoo.util.ref_dirs import get_reference_directions
#from pymoo.termination import get_termination
#from pymoo.optimize import minimize
#from pymoo.visualization.scatter import Scatter
import matplotlib.pyplot as plt
import torch

from src import ml_predictor
#from src.operator_cust.sampling import lhs_integer
from src.operator_cust.sampling.lhs_integer import LHS


class MyProblem(Problem):
    # Define Problem
    def __init__(self, n_var, n_obj, n_ieq_constr, xl, xu,\
                 simulation, spec, objective_index, targets_type, vtype=int):
        super().__init__(n_var=n_var,
                         n_obj=n_obj,
                         n_ieq_constr=n_ieq_constr,
                         xl=xl,
                         xu=xu)
        
        self.simulation=simulation
        self.spec=spec
        self.obj_index=objective_index
        self.tgts_type=targets_type
            

class Optimizer:
    def __init__(self, simulationFun_dict, targets, \
                 boundary, population_size, num_offsprings, \
                 seed=None, objective_index=[]):
        self.boundary=boundary
        self.targets=targets
        self.bounds=boundary.get_normalized_variables_range()
        self.num_design_variables=len(self.bounds)
        self.spec=targets['all targets value']
        self.targets_type=targets['min_max_type']
        self.simulationFun_dict=simulationFun_dict
        self.simulationFun=simulationFun_dict["all"]
        self.population_size=min(population_size, 5*self.num_design_variables)
        self.num_offsprings=min(num_offsprings, population_size) # used in nsga2
        self.seed=seed
        self.objective_index=objective_index #list
        self.n_obj=None
        self.n_ieq_constr=None
        self.n_var=None 
        self.xl=None #1-d array
        self.xu=None #1-d array
        self.problem=None
        self.run_time=None
        self.all_sim_result_dict=None #all_sim_result
        self.all_solution=None
        self.predictor_dict=None
    
    
    def plot(self):
        xl=self.xl
        xu=self.xu
        problem=self.problem
        #Scatter().add(res.F).show()
        xl, xu = problem.bounds()
        ####Design Space
        '''
        plt.figure(figsize=(7, 5))
        plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
        plt.xlim(xl[0], xu[0])
        plt.ylim(xl[1], xu[1])
        plt.title("Design Space")
        plt.show()
        '''
        ###Objective Space
        #plt.figure(figsize=(7, 5))
        #plt.scatter(F[:, 0], F[:, 0], s=30, facecolors='none', edgecolors='blue')
        #plt.title("Objective Space")
        #plt.show()
    
    def _generate_problem(self):
        objective_index = self.objective_index
        spec = self.spec
        targets_type = self.targets_type
        simulationFun = self.simulationFun
        
        n_var, n_obj, n_ieq_constr, xl, xu = self._generate_variables_number_and_uppers_lowers()
        problem = MyProblem(n_var, n_obj, n_ieq_constr, xl, xu, simulationFun, spec, objective_index, targets_type)      
        self.problem=problem
        return problem
    
    def _generate_variables_number_and_uppers_lowers(self):
        #Define variable
        boundary = self.boundary
        objective_index = self.objective_index
        spec = self.spec
        bounds = boundary.get_normalized_variables_range()
        print("bounds:", bounds)
        
        xl=np.array(boundary.get_normalized_variables_lower())
        xu=np.array(boundary.get_normalized_variables_upper())
        print("xl:", xl)
        print("xu:", xu)
        sample_points=1
        for j in range(len(xu)):
            points_tmp=xu[j]-xl[j]+1
            sample_points=float(sample_points)*float(points_tmp)
        print("sample points: {0:.3e}".format( sample_points))
        n_var=len(bounds)
        if len(objective_index)>0:
            n_obj=len(objective_index)
            n_ieq_constr=len(spec)-n_obj
        else:
            n_obj=1
            n_ieq_constr=len(spec)
        print("n_var: {0}, n_obj: {1}, n_ieq_constr: {2}".format(n_var, n_obj, n_ieq_constr))
        self.xl=xl
        self.xu=xu
        self.n_var=n_var
        self.n_obj=n_obj
        self.n_ieq_constr=n_ieq_constr
        return n_var, n_obj, n_ieq_constr, xl, xu
    
    
    def _get_history(self, history):
        n_evals = []             # corresponding number of function evaluations\
        hist_F = []              # the objective space values in each generation
        hist_cv = []             # constraint violation in each generation
        hist_cv_avg = []         # average constraint violation in the whole population

        for algo in history:
        # store the number of function evaluations
            n_evals.append(algo.evaluator.n_eval)
        # retrieve the optimum from the algorithm
            opt = algo.opt
        # store the least contraint violation and the average in each population
            hist_cv.append(opt.get("CV").min())
            hist_cv_avg.append(algo.pop.get("CV").mean())
        # filter out only the feasible and append and objective space values
            feas = np.where(opt.get("feasible"))[0]
            hist_F.append(opt.get("F")[feas])
        
        print("#####history####")
        print("n_evals:", n_evals)
        print("hist_F:", hist_F)
        print("hist_cv:", hist_cv)
        print("hist_cv_avg:", hist_cv_avg)
        # plot convergence
        # replace this line by `hist_cv` if you like to analyze the least feasible optimal solution and not the population
        vals = hist_cv_avg
        num_evals=np.array(list(range(1, len(vals)+1)))
        #k = np.where(np.array(vals) <= 0.0)[0].min()
        #print(f"Whole population feasible in Generation {k} after {n_evals[k]} evaluations.")

        plt.figure(figsize=(7, 5))
        plt.plot(num_evals, vals,  color='blue', lw=2, label="Avg CV of Pop")
        plt.scatter(num_evals, vals,  facecolor="none", edgecolor='blue', marker="p")
        #plt.axvline(num_evals[k], color="red", label="All Feasible", linestyle="--")
        plt.title("Convergence")
        plt.xlabel("Number of Generations")
        #plt.ylabel("Convergence Loss")
        plt.ylabel("Hypervolume")
        plt.legend()
        plt.show()
        
        return n_evals, hist_F, hist_cv, hist_cv_avg
    
    def _create_algorithm(self):
        pass
    
    def _generate_all_corner_predictor_dict(self, corner_list):
        boundary, targets = self.bounds, self.targets
        predictor_dict={}
        for i in range(len(corner_list)):
            corner=corner_list[i]
            predictor_dict[corner]=predictor(boundary, targets, corner) # setup predictor class instance
        self.predictor_dict=predictor_dict
        return predictor_dict
    
    
    def optimize_run(self, max_generation, DNN_mode=None, gen_th=10, gen_period=3):
        # check corner num to determine DNN model:
        #num_corners=len(list(self.simulationFun.keys()))
        #if (num_corners!=1) or (DNN_mode==None):
        if not DNN_mode:
            DNN_mode=0 # deactivate DNN
        ######################
        num_generation=max_generation
        problem=self._generate_problem()
        seed=self.seed #66
        # Define a Termination Criterion
        #termination = get_termination("n_gen", num_generation)
        termination = NoTermination()
        # create algorithm
        algorithm=self._create_algorithm()
        # setup an algorithm object that never terminates
        ## prepare the algorithm to solve the specific problem (same arguments as for the minimize function)
        algorithm.setup(problem, termination=termination, 
                        seed=seed, save_history=True,
                        return_least_infeasible=True,
                        verbose=True)
        # fix the random seed manually
        np.random.seed(seed)
        # Optimization loop
        start_time = time.time()
        n_gen=1
        n_eval=0
        #model_cfg_list, target_bounds_list=None, None
        simulation_flag=1 # 1: SPICE simulation, 0: DNN
        # until the algorithm has no terminated
        while (algorithm.has_next() and n_gen<=num_generation):
            print("##### No.{0} #####".format(n_gen))
            # check simulation flag
            #if DNN_mode and (n_gen>gen_th):
            if DNN_mode:
                if n_gen<=gen_th:
                    simulation_flag=1
                elif ((n_gen-gen_th)%(2*gen_period))>gen_period or (n_gen-gen_th)%(2*gen_period)==0:
                    simulation_flag=0
                else:
                    simulation_flag=1
                print("simulation_flag:", simulation_flag)
            # ask the algorithm for the next solution to be evaluated
            pop = algorithm.ask()
            # get the design space values of the algorithm
            X = pop.get("X")
            #print("X_real:", X)
            #X=(np.rint(X)).astype(int)
            #print("X_int:", X)
            # implement your evaluation
            generation_sim_result_dict=None
            generation_solution=None
            for i in range(len(X)):
                x=X[i]
                if simulation_flag:
                    f, g, sim_result_dict = evaluate(x, problem)
                    n_eval+=1
                else:
                    #bounds=self.bounds
                    predictor_dict=self.predictor_dict
                    f, g=prediction(x, problem, predictor_dict)
                if i==0:
                    F, G =f, g
                else:
                    F = np.row_stack([F, f])
                    G = np.row_stack([G, g])
                    
                # save this generation's simulation result
                if simulation_flag:
                    if i==0:
                        generation_solution=x
                        generation_sim_result_dict=sim_result_dict
                    else:
                        generation_solution=np.row_stack([generation_solution, x])
                        corner_list=generation_sim_result_dict.keys()
                        for corner in corner_list:
                            array1=generation_sim_result_dict[corner]
                            array2=sim_result_dict[corner]
                            generation_sim_result_dict[corner]=np.row_stack([array1, array2])
                        
            
            algorithm.n_eval=n_eval
            static = StaticProblem(problem, F=F, G=G)
            #print("F:", F)
            #print("G:", G)
            Evaluator().eval(static, pop)
            # save generation's simulation result
            if simulation_flag:
                if self.all_sim_result_dict is None:
                    self.all_sim_result_dict=generation_sim_result_dict
                else:
                    corner_list=list(generation_sim_result_dict.keys())
                    for corner in corner_list:
                        array1=self.all_sim_result_dict[corner]
                        array2=generation_sim_result_dict[corner]
                        self.all_sim_result_dict[corner]=np.row_stack([array1, array2])
                if self.all_solution is None:
                    self.all_solution=generation_solution
                else:
                    self.all_solution=np.row_stack([self.all_solution, generation_solution])
            # returned the evaluated individuals which have been evaluated or even modified
            algorithm.tell(infills=pop)
            
            # setup and train DNN
            #bounds, targets=self.bounds, self.targets
            if DNN_mode and simulation_flag:
                if n_gen==1:
                    train_solutions = torch.Tensor(self.all_solution)
                    train_sim_results_dict={}
                    corner_list=list(self.all_sim_result_dict.keys())
                    for corner in corner_list:
                        train_sim_results_dict[corner] = torch.Tensor(self.all_sim_result_dict[corner])
                    setup_mode="setup"
                    predict_mode="all"
                else:
                    train_solutions = torch.Tensor(generation_solution)
                    corner_list=list(train_sim_results_dict.keys())
                    for corner in corner_list:
                        train_sim_results_dict[corner] = torch.Tensor(generation_sim_result_dict[corner])
                    setup_mode="update"
                    predict_mode="all"
                    #pass
                print("DNN setup and training!")
                if setup_mode=="setup":
                    self._generate_all_corner_predictor_dict(corner_list) #setup predictor instance dict
                
                predictor_dict=self.predictor_dict
                for i in range(len(corner_list)):
                    corner=corner_list[i]
                    train_sim_results=train_sim_results_dict[corner]
                    predictor=predictor_dict[corner]
                    predictor.setup_and_update(train_solutions, train_sim_results, predict_mode=predict_mode, mode=setup_mode)
                
            
            # do same more things, printing, logging, storing or even modifying the algorithm object
            print("n_eval:", algorithm.n_eval)
            n_gen=algorithm.n_gen
            
        # obtain the result objective from the algorithm
        res = algorithm.result()
        # Optimization loop end
        end_time = time.time()
        self.run_time=end_time-start_time
        X, F, CV = res.X, res.F, res.CV # F is objective_loss, CV is constrain_loss
        pareto_set = [X]
        
        final_pop = res.pop
        final_pop_X = final_pop.get("X")
        
        hist = res.history
        self._get_history(hist)
        print("pareto set:", pareto_set)
        print("final population:", final_pop_X)
        print("run_time:", self.run_time)
        print("####### End ###########")
        return pareto_set, F, CV


class USGA3Optimizer(Optimizer):
    def _create_algorithm(self):
        population_size=self.population_size
        #num_offsprings=self.num_offsprings
        n_obj=self.n_obj
        # create the reference directions to be used for the optimization
        #ref_dirs = get_reference_directions("uniform", n_obj, n_partitions=int(population_size*0.6))
        ref_dirs = get_reference_directions("energy", n_obj, population_size)  #seed=1
        # create the algorithm object, NSGA3 UNSGA3 
        algorithm = UNSGA3(pop_size=population_size,
                          ref_dirs=ref_dirs,
                          sampling=LHS(),
                          crossover=SBX(prob=0.9, eta=30, vtype=float, repair=RoundingRepair()),
                          mutation=PM(eta=20, vtype=float, repair=RoundingRepair()),
                          save_history=True,
                          eliminate_duplicates=True)
        return algorithm
    
class NSGA2Optimizer(Optimizer):
    def __init__():
        pass
        

    def _create_algorithm(self):
        population_size=self.population_size
        num_offsprings=self.num_offsprings
        #n_obj=self.n_obj
        # create the algorithm object, NSGA2 
        algorithm = NSGA2(
                pop_size=population_size,
                n_offsprings=num_offsprings,
                sampling=LHS(),
                crossover=SBX(prob=0.9, eta=30, vtype=float, repair=RoundingRepair()),
                mutation=PM(eta=20, vtype=float, repair=RoundingRepair()),
                save_history=True,
                eliminate_duplicates=True,
                )
        return algorithm    

class RVEAOptimizer(Optimizer):
    def _create_algorithm(self):
        population_size=self.population_size
        #num_offsprings=self.num_offsprings
        n_obj=self.n_obj
        # create the reference directions to be used for the optimization
        n_partitions=int(population_size*0.6)
        ref_dirs = get_reference_directions("das-dennis", n_obj, n_partitions)
        # create the algorithm object, RVEA
        algorithm = RVEA(pop_size=population_size,
                          ref_dirs=ref_dirs,
                          sampling=LHS(),
                          crossover=SBX(prob=0.9, eta=30, vtype=float, repair=RoundingRepair()),
                          mutation=PM(eta=20, vtype=float, repair=RoundingRepair()),
                          save_history=True,
                          eliminate_duplicates=True)
        return algorithm



#################################################################
def evaluate(x, problem):
    simulation=problem.simulation
    spec=np.array(problem.spec)
    #print("values:", x)
    total_area_index=sum(x)
    tgts_type=np.array(problem.tgts_type)
    #print("tgts_type",tgts_type)
    
    #result=np.zeros(len(spec))
    #corner_list =["tt", "ff", "ss", "fnsp", "snfp"]
    corner_list=list(simulation.keys())
    #print("simulation:", simulation)
    #print("corner_list:", corner_list)
    sim_result_dict={} #dict key is corner in corner_list, value is array
    for i in range(len(corner_list)):
        corner=corner_list[i]
        #print("corner:", corner)
        simulation_fun=simulation[corner]
        result_tmp, sim_result_tmp=calculate_result(x, simulation_fun, tgts_type, spec)
        #print("result_tmp:", result_tmp)
        #print("sim_result_tmp:", sim_result)
        sim_result_dict[corner]=sim_result_tmp
        if i==0:
            result=result_tmp
            sim_result=sim_result_tmp
        else:
            result=np.row_stack((result, result_tmp))
            sim_result=np.row_stack((sim_result, sim_result_tmp))
    
    sum_result=np.zeros(len(spec))
    if len(corner_list)>1:
        for item in result:
            sum_result=sum_result+item
    else:
        sum_result=result
    #print("sim_result_dict:", sim_result_dict)
    #print("sim_result:", sim_result) #2D matrix
    #print("result:", result) #2D matrix
    #print("sum result:", sum_result)
    #print("sum loss:", sum(sum_result))
    
    obj_index = problem.obj_index
    all_index = list(range(len(sum_result)))
    if len(obj_index)>0:
        constr_index = [i for i in all_index if i not in obj_index]
    
        F = np.array(sum_result[obj_index])
        G = np.array(sum_result[constr_index])
    else:
        #out["F"] = sum(result)
        F = total_area_index
        #F = np.sum(sum_result)
        G = sum_result
    return F, G, sim_result_dict

def calculate_result(x, simulation_fun, tgts_type, spec):
    sim_result=np.array(simulation_fun.run(x))
    #print("sim_result:", sim_result)
    # check whether simulation result is normal or not
    contain_nan= (True in np.isnan(sim_result))
    if contain_nan:
        result=100*np.ones(len(sim_result)) #100
    else:
        spec=np.array(spec)
        #print("specification:", spec)
        result = ((spec-sim_result)*tgts_type)/spec #normalize
        result[result<0]=0 #let negative item be 0
        #result[result>=0.99]=10 #let unsaticied item be large
        result_new_tmp=result.copy()
        for i in range(len(result_new_tmp)):
            item=result_new_tmp[i]
            if item>=0.99:
                #item=10*item*np.exp(item-1)
                item=item+10
                result_new_tmp[i]=item
        result=result_new_tmp
    return result, sim_result

#################### setup DNN ####################
def setup_and_update_prediction_models(all_solutions, all_sim_results, bounds, targets, corner="tt", predict_mode='all', mode='setup'):
    print("set up prediction models")
    if predict_mode=='all':
        target_mode='all targets value'
    else:
        target_mode=predict_mode
    used_targets=targets[target_mode]
    model_cfg_list=[]
    target_bounds_list=[]
    corner=corner
    # check DNN models folder dir
    cwd=os.getcwd()
    models_dir=os.path.join(cwd,"DNN_models")
    existance=os.path.exists(models_dir)
    #print("current dir:", cwd)
    #print("models dir:", models_dir)
    #print("existance:", existance)
    if not existance:
        os.mkdir(models_dir)
    # setup DNN model or update DNN model
    for target_index in range(len(used_targets)):
        model_name="model_state_dict_{0}_{1}_target_{2}.pkl".format(corner, predict_mode, target_index)
        path_state_dict = os.path.join(models_dir, model_name)
        #print("model_path_state_dict:", path_state_dict)
        model_cfg, target_bounds=ml_predictor.setup_and_update_DNN_for_single_target(all_solutions,\
                                         all_sim_results,\
                                         bounds, targets, target_index,\
                                         sim_mode=predict_mode,\
                                         BATCH_SIZE=1, EPOCH=100,\
                                         n_hidden=None, mode=mode, path_state_dict=path_state_dict )
        model_cfg_list.append(model_cfg)
        target_bounds_list.append(target_bounds)
    return model_cfg_list, target_bounds_list

def use_mode_predict(x_test, model_cfg_list, bounds, target_bounds_list):
    #print("use_mode_predict")
    predict_results=[]
    for idx in range(len(model_cfg_list)):
        model_cfg = model_cfg_list[idx]
        target_bounds = target_bounds_list[idx]
        x_test = np.array(x_test)
        #print("x_test:", x_test)
        y_predict=ml_predictor.run_DNN(model_cfg, target_bounds, bounds, x_test)
        #print("y_predict:", y_predict)
        predict_results.append(y_predict)
    return predict_results



class predictor:
    def __init__(self, bounds, targets, corner="tt"):     
        self.boundary=bounds
        self.targets=targets
        self.corner=corner
        self.target_bounds_list=None
        self.model_cfg_list=None
    def setup_and_update(self, train_solutions, train_sim_results, predict_mode='all', mode='setup'):
        corner=self.corner
        boundary=self.boundary
        targets=self.targets
        model_cfg_list, target_bounds_list = setup_and_update_prediction_models(train_solutions, train_sim_results, boundary, targets, corner, predict_mode='all', mode='setup')
        self.model_cfg_list, self.target_bounds_list =model_cfg_list, target_bounds_list
    def run(self, x):
        predict_result=use_mode_predict(x, self.model_cfg_list, self.boundary, self.target_bounds_list)
        return predict_result
    

def prediction(x, problem, predictor_dict):
    spec=np.array(problem.spec)
    #print("values:", x)
    total_area_index=sum(x)
    tgts_type=np.array(problem.tgts_type)
    #print("tgts_type",tgts_type)
    corner_list=list(predictor_dict.keys())
    for i in range(len(corner_list)):
        corner=corner_list[i]
        predictor=predictor_dict[corner]
        result_tmp, predict_result_tmp=calculate_result(x, predictor, tgts_type, spec)
        if i==0:
            result=result_tmp
        else:
            result=np.row_stack((result, result_tmp))
        #print("{0} result:{1}".format(corner, result_tmp))
        #print("{0} predict_result:{1}".format(corner, predict_result_tmp))
    
    sum_result=np.zeros(len(spec))
    for item in result:
        sum_result=sum_result+item
    #print("prediction sum result:", sum_result)
    
    obj_index = problem.obj_index
    all_index = list(range(len(sum_result)))
    if len(obj_index)>0:
        constr_index = [i for i in all_index if i not in obj_index]
    
        F = np.array(sum_result[obj_index])
        G = np.array(sum_result[constr_index])
    else:
        #out["F"] = sum(result)
        F = total_area_index
        G = sum_result
    return F, G


