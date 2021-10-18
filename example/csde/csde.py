#！/usr/bin/python
# -*- coding: utf-8 -*-#

'''
---------------------------------
 Name:         csde
 Description:  
 Author:       Samuel
 Date:         28/09/2021
---------------------------------
'''

import numpy as np
import copy
import time
from .individual import Individual

class CSDE:

    def __init__(self, func=None, dim=None, bound=None, max_iters=1000, pop_size=50,
                 show_info=False, func_name=None):

        # Problem information
        self.func = func
        self.func_name = func_name
        self.dim = dim
        self.bound = bound
        self.pop_size = pop_size
        self.iterations = max_iters
        self.show_info = show_info

        self.FP = 200

        self.history = []
        self.gbest = {'individual': None, 'fitness': float('inf'), 'solution': None}
        self.gworst_y = -float('inf')
        self.convergence_iter = 0

        self.S_gc = 1
        self.R_gc = 1
        self.S_gr = 1
        self.R_gr = 1
        self.rec_S_gc_beatGbest = 0
        self.rec_S_gr_beatGbest = 0
        self.rec_SR = []
        self.rec_R = []
        self.rec_SRX_beatGbest = []
        self.rec_SRX_withoutExtraReward = []

    def run(self):
        self.history = []
        individuals = []

        # Initialization
        self.y_lst = []
        self.x_lst = []
        for _ in range(self.pop_size):
            ind = Individual(dim=self.dim, bound=self.bound, maxIterations=self.iterations, FP=self.FP)
            ind.fitness = self.func(ind.solution)
            individuals.append(ind)
            self.y_lst.append(ind.fitness)
            self.x_lst.append(copy.deepcopy(ind.solution))
            if ind.fitness < self.gbest['fitness']:
                self.gbest['fitness'] = ind.fitness
                self.gbest['solution'] = ind.solution
                self.gbest['individual'] = ind
        self.gworst_y = np.max(self.y_lst)

        order_lst = np.arange(self.pop_size)
        start_time = time.process_time()

        self.gbest_op = [""] * self.iterations
        self.op_stat = {'CurrentToPbest': np.zeros(self.iterations), 'PbestToRand': np.zeros(self.iterations)}

        for iteration in range(self.iterations):
            if iteration % 1000 == 0:
                end_time = time.process_time()
                log_time = end_time - start_time
                print('[{}]: {}/{}, Time: {}s, fitness: {}'.format(self.func_name, iteration, self.iterations,
                                                                   round(log_time, 2), self.gbest['fitness']))
                start_time = end_time
            # Update p of pbest, M_g and P_g
            M_g = (self.iterations - iteration) / self.iterations # -(cur_iteration + 1) + 1 as the iteration starts from 0.
            P_g = (self.FP - np.mod(iteration + 1, self.FP)) / self.FP
            p = int(np.floor((0.5 * M_g * P_g * P_g * self.pop_size) + 1))

            # Update SR_g
            SR_gc = (self.S_gc + self.rec_S_gc_beatGbest) / self.R_gc # CurrentToPbest
            SR_gr = (self.S_gr + self.rec_S_gr_beatGbest) / self.R_gr # PbestToRand
            SR_g = SR_gc / (SR_gc + SR_gr)

            # Reset every 200 iterations and log the data.
            reset_th = np.mod(iteration + 1, self.FP)
            if (reset_th == 0) or (iteration == 0):
                # Record the trend for visulaization.
                self.rec_SR.append(SR_g)
                totalRx = self.R_gc + self.R_gr
                self.rec_R.append([self.R_gc/totalRx, self.R_gr/totalRx])
                self.rec_SRX_withoutExtraReward.append([self.S_gc/self.R_gc, self.S_gr/self.R_gr])

                totalSx = self.rec_S_gc_beatGbest + self.rec_S_gr_beatGbest
                if totalSx == 0:
                    self.rec_SRX_beatGbest.append([0, 0])
                else:
                    self.rec_SRX_beatGbest.append([self.rec_S_gc_beatGbest/totalSx, self.rec_S_gr_beatGbest/totalSx])

                if reset_th == 0:
                    # Reset
                    self.S_gc = 1
                    self.R_gc = 1
                    self.S_gr = 1
                    self.R_gr = 1
                    self.rec_S_gc_beatGbest = 0
                    self.rec_S_gr_beatGbest = 0

            y_lst_new = []
            x_lst_new = []
            last_gbest_fitness = self.gbest['fitness']

            # Extract the index of the first p best individuals.
            pbest_sort = np.argsort(self.y_lst)
            pbest_sort = pbest_sort[:p]
            for idx, ind in enumerate(individuals):
                # Update CR
                ind.update_CR(M_g=M_g, gbest_y=last_gbest_fitness, gworst_y=self.gworst_y)
                
                # Randomly select pbest, x_r1g and x_r2g
                pbest_idx = np.random.choice(pbest_sort, size=1, replace=False)[0]
                pbest_x = self.x_lst[pbest_idx]

                rand_lst = np.delete(order_lst, [idx, pbest_idx])
                x1_idx, x2_idx = np.random.choice(rand_lst, size=2, replace=False)
                x_r1g = self.x_lst[x1_idx]
                x_r2g = self.x_lst[x2_idx]
                # Update and search
                rx = np.random.rand()
                if rx < SR_g:
                    # F_gc
                    op_x = 'CurrentToPbest'
                    ind.update_F(op_type=op_x, M_g=M_g, P_g=P_g)
                    u = ind.search(op_type=op_x, pbest_x=pbest_x, x_r1g=x_r1g, x_r2g=x_r2g)
                    self.R_gc = self.R_gc + 1
                    y_u = self.func(u)
                    if y_u < ind.fitness:
                        ind.solution = u
                        ind.fitness = y_u
                        self.S_gc = self.S_gc + 1
                        if y_u < last_gbest_fitness:
                            self.rec_S_gc_beatGbest = self.rec_S_gc_beatGbest + 1

                else:
                    # F_gr
                    op_x = 'PbestToRand'
                    ind.update_F(op_type=op_x, M_g=M_g, P_g=P_g)
                    u = ind.search(op_type=op_x, pbest_x=pbest_x, x_r1g=x_r1g, x_r2g=x_r2g)
                    self.R_gr = self.R_gr + 1
                    y_u = self.func(u)
                    if y_u < ind.fitness:
                        ind.solution = u
                        ind.fitness = y_u
                        self.S_gr = self.S_gr + 1
                        if y_u < last_gbest_fitness:
                            self.rec_S_gr_beatGbest = self.rec_S_gr_beatGbest + 1

                self.op_stat[op_x][iteration] = self.op_stat[op_x][iteration] + 1 # count the number of each operator being executed at each iteration.

                if ind.fitness < self.gbest['fitness']:
                    self.gbest_op[iteration] = op_x
                    self.gbest['fitness'] = ind.fitness
                    self.gbest['solution'] = ind.solution
                    self.gbest['individual'] = ind
                    self.convergence_iter = iteration + 1

                y_lst_new.append(ind.fitness)
                x_lst_new.append(copy.deepcopy(ind.solution))

            self.y_lst = y_lst_new
            self.x_lst = x_lst_new
            self.gworst_y = np.max(self.y_lst)
            if self.show_info:
                print("Iteration: {}, Fitness: {}".format(iteration, self.gbest['fitness']))
            self.history.append(self.gbest['fitness'])

        return self.gbest['solution'], self.gbest['fitness'], self.history

    def get_Rec(self):
        SR = np.array(self.rec_SR).transpose()
        R = np.array(self.rec_R).transpose()
        SRX_withoutExtraReward = np.array(self.rec_SRX_withoutExtraReward).transpose()
        SRX_beatGbest = np.array(self.rec_SRX_beatGbest).transpose()
        SR_stat = {'SR': SR, 'R': R, 'SRX_enhancement': SRX_withoutExtraReward, 'SRX_beatGbest': SRX_beatGbest}

        return SR_stat

    def get_convergenceIter(self):
        return self.convergence_iter
