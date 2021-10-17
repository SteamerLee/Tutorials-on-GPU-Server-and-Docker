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


def paraTrend_graph(dataLst, para, func_name, problem_size, iter_lst, root_dir, algo_name, time_no, FP=None):
    # Display the trend of some adjusted parameters.
    pic_dir = os.path.join(root_dir, 'parameter', 'func_{}'.format(func_name))
    os.makedirs(pic_dir, exist_ok=True)

    ir = iter_lst[0]

    fig = plt.figure()

    if para == 'SR':
        data_key = ['SR', 'R', 'SRX_enhancement', 'SRX_beatGbest']
        ylabel_lst = ["Selection Prob.", "Utilization Prob.", "Enhancement Prob.", "Enhancement Prob.(Gbest)"]
        title_lst = ['Selection', 'Utilization', 'Enhancement', 'Enhancement(Gbest)']
        for idx in range(4):
            plt.subplot(2, 2, idx + 1)
            x = np.arange(0, ir + 1, FP)
            data = dataLst[data_key[idx]]
            if idx == 0:
                # SR
                y1 = data[:len(x)] # Current to pebst
                y2 = 1 - y1 # Pbest to rand
            else:
                y1 = data[0][:len(x)]
                y2 = data[1][:len(x)]
            plt.stackplot(x, y1, y2, colors=['m', 'b'], labels=['Current_to_pbest', 'Pbest_to_rand'])
            plt.legend(prop={'size': 6})
            plt.xlabel("Iterations")
            plt.ylabel(ylabel_lst[idx])
            plt.title(title_lst[idx])

    plt.tight_layout()
    pic_name = 'func_{}_algo_{}_dim_{}_times_{}_para_{}.png'.format(func_name, algo_name, problem_size, time_no, para)
    pic = "Function: {} [{}]".format(func_name, algo_name)
    plt.suptitle(pic)
    plt.savefig(os.path.join(pic_dir, pic_name))  
    # plt.show()
    plt.close(0)