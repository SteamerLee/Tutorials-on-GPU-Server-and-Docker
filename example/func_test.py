#！/usr/bin/python
# -*- coding: utf-8 -*-#

'''
---------------------------------
 Name:         func_test.py
 Description:  
 Author:       Samuel and Ray
 Date:         13/09/2021
---------------------------------
'''
import numpy as np
import pandas as pd
import time
import os
import gc
from graph_gen import convergence_graph
from sko.GA import GA
from sko.PSO import PSO
from problemSet import *
from jpype import *

startJVM(getDefaultJVMPath(), "-ea")
JClass = JClass("testfunc")
jc = JClass()

def run_process(process_no, selected_tasks):

    for kwargs in selected_tasks:
        algo_dicts = {'GA': GA, 'PSO': PSO}

        # Load args.
        run_times = kwargs['run_times']
        pop = kwargs['pop']
        iterations = kwargs['iterations']
        verbose = kwargs['verbose']

        problem_size = kwargs['problem_size']
        name = kwargs['algo']
        Algo = algo_dicts[kwargs['algo']]
        func = kwargs['func']['func']
        func_name = kwargs['func']['func_name']
        bound = kwargs['func']['bound']
        root_dir = kwargs['root_dir']
        version = kwargs['version']
        err_acc = kwargs['err_acc']
        optimal_value = kwargs['func']['optimal']

        cpu_times_list = []
        run_times_list = []
        best_fit_lst = []
        fitness_history_lst = []
        best_solution_lst = []
        success_run = 0
        fit_history = []

        iter_to_opt_lst = []
        iter_to_gbest_lst = []

        for time_no in range(run_times):

            start_processing_time = time.process_time() # CPU time
            start_pref_time = time.perf_counter()

            if name == 'GA':
                # Initialize the optimizer.
                algo = Algo(func=func, n_dim=problem_size, size_pop=pop, max_iter=iterations,
                            lb=(np.zeros(problem_size) + bound[0]).tolist(),
                            ub=(np.zeros(problem_size) + bound[1]).tolist(),
                            precision=1e-7)
                # Perform the search,
                best_solution, best_fit = algo.run()
                best_fit = best_fit[0]
                raw_fit_history = algo.all_history_Y
                raw_fit_history = np.array(raw_fit_history).min(axis=1) 
                cur_min = raw_fit_history[0]
                fit_history = []
                for cur_raw_fit in raw_fit_history:
                    if cur_raw_fit > cur_min:
                        fit_history.append(cur_min)
                    else:
                        cur_min = cur_raw_fit
                        fit_history.append(cur_raw_fit)
                fit_history = np.array(fit_history) # The history of the best fitness value. shape: (maxIterations, )

            elif name == 'PSO':
                algo = Algo(func=func, dim=problem_size, pop=pop, max_iter=iterations, lb= (np.zeros(problem_size) + bound[0]).tolist(), ub=(np.zeros(problem_size) + bound[1]).tolist(), w=0.8, c1=0.5, c2=0.5)
                best_solution, best_fit = algo.run()
                fit_history = np.array(algo.gbest_y_hist)  # The history of the best fitness value. shape: (maxIterations, )

            end_processing_time = time.process_time()
            end_pref_time = time.perf_counter()

            cpu_times_list.append(end_processing_time - start_processing_time)
            run_times_list.append(end_pref_time - start_pref_time)

            path = os.path.join(root_dir, 'history', name, 'func_{}'.format(func_name), 'dim_{}'.format(problem_size))
            os.makedirs(path, exist_ok=True)
           
            # Save fitness history
            pd.DataFrame(fit_history).to_csv(os.path.join(path, '{}.csv'.format(str(time_no + 1))), index=False)
            print("-----------------------------------")
            print("name {},fun {}, dim {}, time {}/{}, fit: {}, CPU Time: {}s".format(name,func_name, problem_size, time_no + 1, run_times, best_fit, round(end_processing_time - start_processing_time, 4)))

            best_fit_lst.append(best_fit)
            fit_history_norm = np.array(fit_history) - optimal_value
            fitness_history_lst.append(fit_history_norm) 
            best_solution_lst.append(best_solution) 

            is_success_flag = False
            if (best_fit - optimal_value) <= err_acc:
                success_run = success_run + 1
                is_success_flag = True
                d_x1 = np.where(fit_history_norm <= err_acc, 0, 1)
                d_x2 = np.sum(d_x1)
                if d_x2 >= len(d_x1):
                    # Non-convergence in the experiment
                    curIter_to_opt = len(d_x1)
                else:
                    # Convergence
                    curIter_to_opt = d_x2 + 1
                iter_to_opt_lst.append(curIter_to_opt) # the iteration where the optimal fitness is firstly generated. 

            std = np.std(best_fit_lst)
            mean = np.mean(best_fit_lst)
            best = np.min(best_fit_lst)
            worst = np.max(best_fit_lst)

            avg_cpu_time = np.mean(cpu_times_list)
            avg_run_time = np.mean(run_times_list)
            if len(iter_to_opt_lst) == 0:
                iter_to_opt = 0
            else:
                iter_to_opt = np.mean(iter_to_opt_lst)

            if len(iter_to_gbest_lst) == 0:
                iter_to_gbest = 0
            else:
                if is_success_flag:
                    iter_to_gbest_lst[-1] = curIter_to_opt
                    iter_to_gbest = np.mean(iter_to_gbest_lst)
                else:
                    iter_to_gbest = np.mean(iter_to_gbest_lst)  # the iteration where the best fitness is firstly generated. 

            out = {
            'function': str(func_name),
            'version': version,
            'dim': problem_size,
            'algo': name,
            'num_of_current_runtime': time_no + 1,
            'optimal': optimal_value,

            'mean': mean,
            'std': std,
            'best': best,
            'worst': worst,

            'avg_cpu_time': avg_cpu_time,
            'avg_run_time': avg_run_time,
            'best_fit_list': best_fit_lst,
            'success_run': success_run,
      
            'iterations_to_optimal': iter_to_opt,
            'iterations_to_gbest': iter_to_gbest,
            }
            path = root_dir + 'running/'
            os.makedirs(path, exist_ok=True)
            x_path = os.path.join(path, 'algo_{}_func_{}_dim_{}.csv'.format(name, func_name, problem_size))
            pd.DataFrame([out]).to_csv(x_path, index=False)

            # Save the best solution
            path = os.path.join(root_dir, 'solution')
            os.makedirs(path, exist_ok=True)
            pd.DataFrame(best_solution_lst).to_csv(os.path.join(path, 'algo_{}_func_{}_dim_{}_bestsolution.csv').format(name, func_name, problem_size), index=False)

            try:
                iter_lst = [iterations]
                convergence_graph(fitness_lst=fitness_history_lst, func_name=func_name, problem_size=problem_size,
                                    run_times=run_times, iter_lst=iter_lst, root_dir=root_dir, algo_name=name)

            except:
                print('Failed to output the convergence graph. {}_{}_{}'.format(func_name, problem_size, time_no))

            del algo
            gc.collect()

def main():

    problem_size = 30 
    cec2014 = CEC2014(jc=jc, dim=problem_size)
    F16_OptimalValue = {2: -1.8013, 5: -4.687658, 10: -9.66015, 30: -29.6308839, 50: -49.6248323}

    fun_list = [
        {'func_name': 'cec1-2014', 'func': cec2014.CEC1, 'bound': [-100,100], 'optimal': 100},
        # {'func_name': 'cec2-2014', 'func': cec2014.CEC2, 'bound': [-100,100], 'optimal': 200},
        # {'func_name': 'cec3-2014', 'func': cec2014.CEC3, 'bound': [-100,100], 'optimal': 300},
        # {'func_name': 'cec4-2014', 'func': cec2014.CEC4, 'bound': [-100,100], 'optimal': 400},
        # {'func_name': 'cec5-2014', 'func': cec2014.CEC5, 'bound': [-100,100], 'optimal': 500},
        # {'func_name': 'cec6-2014', 'func': cec2014.CEC6, 'bound': [-100,100], 'optimal': 600},
        # {'func_name': 'cec7-2014', 'func': cec2014.CEC7, 'bound': [-100,100], 'optimal': 700},
        # {'func_name': 'cec8-2014', 'func': cec2014.CEC8, 'bound': [-100,100], 'optimal': 800},
        # {'func_name': 'cec9-2014', 'func': cec2014.CEC9, 'bound': [-100,100], 'optimal': 900},
        # {'func_name': 'cec10-2014', 'func': cec2014.CEC10, 'bound': [-100,100], 'optimal': 1000},
        # {'func_name': 'cec11-2014', 'func': cec2014.CEC11, 'bound': [-100,100], 'optimal': 1100},
        # {'func_name': 'cec12-2014', 'func': cec2014.CEC12, 'bound': [-100,100], 'optimal': 1200},
        # {'func_name': 'cec13-2014', 'func': cec2014.CEC13, 'bound': [-100,100], 'optimal': 1300},
        # {'func_name': 'cec14-2014', 'func': cec2014.CEC14, 'bound': [-100,100], 'optimal': 1400},
        # {'func_name': 'cec15-2014', 'func': cec2014.CEC15, 'bound': [-100,100], 'optimal': 1500},
        # {'func_name': 'cec16-2014', 'func': cec2014.CEC16, 'bound': [-100,100], 'optimal': 1600},
        # {'func_name': 'cec17-2014', 'func': cec2014.CEC17, 'bound': [-100,100], 'optimal': 1700},
        # {'func_name': 'cec18-2014', 'func': cec2014.CEC18, 'bound': [-100,100], 'optimal': 1800},
        # {'func_name': 'cec19-2014', 'func': cec2014.CEC19, 'bound': [-100,100], 'optimal': 1900},
        # {'func_name': 'cec20-2014', 'func': cec2014.CEC20, 'bound': [-100,100], 'optimal': 2000},
        # {'func_name': 'cec21-2014', 'func': cec2014.CEC21, 'bound': [-100,100], 'optimal': 2100},
        # {'func_name': 'cec22-2014', 'func': cec2014.CEC22, 'bound': [-100,100], 'optimal': 2200},
        # {'func_name': 'cec23-2014', 'func': cec2014.CEC23, 'bound': [-100,100], 'optimal': 2300},
        # {'func_name': 'cec24-2014', 'func': cec2014.CEC24, 'bound': [-100,100], 'optimal': 2400},
        # {'func_name': 'cec25-2014', 'func': cec2014.CEC25, 'bound': [-100,100], 'optimal': 2500},
        # {'func_name': 'cec26-2014', 'func': cec2014.CEC26, 'bound': [-100,100], 'optimal': 2600},
        # {'func_name': 'cec27-2014', 'func': cec2014.CEC27, 'bound': [-100,100], 'optimal': 2700},
        # {'func_name': 'cec28-2014', 'func': cec2014.CEC28, 'bound': [-100,100], 'optimal': 2800},
        # {'func_name': 'cec29-2014', 'func': cec2014.CEC29, 'bound': [-100,100], 'optimal': 2900},
        # {'func_name': 'cec30-2014', 'func': cec2014.CEC30, 'bound': [-100,100], 'optimal': 3000},
    ]

    ### Parameter setting
    version = 'v0'
    err_acc = 1e-04 # 
    processes = 1

    run_times = 2 # usually set 10 or above for collecting the reliable results.
    pop = 50 # population size
    iterations = 10000 # Number of iterations in each runtime
    verbose = False

    tasks_list = []
    task_cnt = 0
    for func in fun_list:
        # GA, PSO
        for algo in ['PSO']:
            root_dir = 'res_{}_{}/'.format(version, algo)

            task_cnt = task_cnt + 1
            arg_lst = {
                'Task_ID': task_cnt,
                'func': func,
                'algo': algo,
                'problem_size': problem_size,
                'root_dir': root_dir,
                'version': version,
                'err_acc': err_acc,
                'run_times': run_times,
                'pop': pop,
                'iterations': iterations,
                'verbose': verbose
            }
            tasks_list.append(arg_lst)

    run_process(0, tasks_list)

    # pool = ProcessPool(processes)
    # _ = pool.map(run_process, tasks_list)
    #
    # pool.close()
    # pool.join()

   
    # tasks_list = np.array(tasks_list)
    # np.random.shuffle(tasks_list)
    # tasks_list = np.array_split(tasks_list, processes)
    # for i in range(processes):
    #     p = Process(target=run_process, args=(i, tasks_list[i]))
    #     p.start()



if __name__ == '__main__':
    main()
