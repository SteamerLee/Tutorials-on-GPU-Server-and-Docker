#！/usr/bin/python
# -*- coding: utf-8 -*-#

'''
---------------------------------
 Name:         graph_gen.py
 Description:  
 Author:       Samuel
 Date:         03/06/2020
---------------------------------
'''

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os

def convergence_graph(fitness_lst, func_name, problem_size, run_times, iter_lst, root_dir, algo_name):

    pic_dir = os.path.join(root_dir, 'convergence')
    os.makedirs(pic_dir, exist_ok=True)

    for ir in iter_lst:
        fig = plt.figure()
        for xd in fitness_lst:
            xx = np.arange(ir)
            xy = xd[:ir]
            plt.plot(xx, xy)

        plt.xlabel("Iterations")
        plt.ylabel("f(x) - f_opt")
        pic_name = 'dim_{}_func_{}_algo_{}_times_{}_iter_{}.png'.format(problem_size, func_name, algo_name, run_times, ir)
        pic = 'Function: {}'.format(func_name)

        plt.title(pic)
        plt.savefig(os.path.join(pic_dir, pic_name))  
        # plt.show()
        plt.close(0)
