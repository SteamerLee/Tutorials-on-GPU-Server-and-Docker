#！/usr/bin/python
# -*- coding: utf-8 -*-#

'''
---------------------------------
 Name:         individual
 Description:  
 Author:       Samuel
 Date:         28/09/2021
---------------------------------
'''

import numpy as np
import copy

class Individual:

    def __init__(self, dim, bound, maxIterations, FP):

        self.dim = dim
        self.bound = bound
        self.maxIterations = maxIterations

        self.solution = self.bound[0] + np.random.rand(self.dim) * (self.bound[1] - self.bound[0])
        self.fitness = None

        self.FP = FP # Cyclic frequency of p parameter
        self.CR = None
        self.I_ig = None
        self.F_igC = None
        self.F_igR = None

    def update_CR(self, M_g, gbest_y, gworst_y):
        N_ig = np.random.normal(0.5, 0.1)
        N_ig = np.clip(N_ig, 0, 1)
        self.I_ig = (self.fitness - gbest_y) / (gworst_y - gbest_y + 1e-99)
        self.CR = (M_g * N_ig) + ((1 - M_g) * self.I_ig)

    def search(self, op_type, pbest_x, x_r1g, x_r2g):

        if op_type == 'CurrentToPbest':
            # Current to pbest
            v_ig = self.solution + self.F_igC * (pbest_x - self.solution) + self.F_igC * (x_r1g - x_r2g)

        elif op_type == 'PbestToRand':
            # Pbest to rand
            v_ig = pbest_x + self.F_igR * (x_r1g - self.solution) + self.F_igR * (x_r2g - self.solution)

        else:
            print('Invalid operators in search [{}]'.format(op_type))
            raise

        # Handle the bound constraints
        v_ig = np.clip(v_ig, *self.bound)
        # Crossover
        c = np.random.rand(self.dim)
        c_jrand = np.random.randint(low=0, high=self.dim, size=1)[0]
        c[c_jrand] = 0
        mask = c <= self.CR
        u = np.where(mask, v_ig, self.solution)
        return u

    def update_F(self, op_type, M_g, P_g):
        # Update hyper-parameter
        if op_type == 'CurrentToPbest':
            # Current to pbest
            self.F_igC = M_g * M_g + (1 - M_g) * self.I_ig

        elif op_type == 'PbestToRand':
            # Pbest to rand
            self.F_igR = M_g * M_g + (1 - M_g) * P_g

        else:
            print('Invalid operators in search [{}]'.format(op_type))
            raise