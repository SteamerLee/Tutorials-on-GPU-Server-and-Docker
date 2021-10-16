import numpy as np

def ray_f1(variables=None, problem_size=None):
  # Sphere
  return np.sum(variables**2)

def ray_f1(variables=None, problem_size=None):
  # Sphere
  return np.sum(variables**2)

def ray_f2(variables=None, problem_size=None):
    problem_size = len(variables)
    t1 = 0.0
    for i in range(problem_size - 1):
        t1 = t1 + np.power(variables[i] ** 2, variables[i + 1] ** 2 + 1) + np.power(variables[i+1] ** 2, variables[i] ** 2 + 1)
    return t1

def ray_f3(variables=None, problem_size=None):
    # Ellipsoid
    tmp = 0
    problem_size = len(variables)
    for i in range(problem_size):
        tmp += np.power(np.power(1000,i/(problem_size-1))*variables[i],2)
    return tmp

def ray_f4(variables=None, problem_size=None):
    # Schwefel 2.21 Function
    problem_size = len(variables)
    return np.max(np.abs(variables))


def ray_f5(variables=None, problem_size=None):
   # Weighted Sphere function
   tmp = 0
   problem_size = len(variables)
   for i in range(problem_size):
       tmp += (i+1)*np.power(variables[i],2)
   return tmp

def ray_f6(variables=None, problem_size=None):
    # Sum of Power
    tmp = 0
    problem_size = len(variables)
    for i in range(problem_size):
        tmp += np.power(np.absolute(variables[i]),i+2)
    return tmp

def ray_f7(variables=None, problem_size=None):
    # ZAKHAROV
    tmp1 = 0
    tmp2 = 0
    problem_size = len(variables)
    for i in range(problem_size):
        tmp1 += np.power(variables[i],2)
        tmp2 += (i+1)*variables[i]

    return tmp1+np.power(1/2*tmp2,2)+np.power(1/2*tmp2,4)

def ray_f8(variables=None, problem_size=None):
    problem_size = len(variables)
    return np.sum([np.power(np.sum([variables[j] for j in range(0, i)]), 2) for i in range(0, problem_size)])

def ray_f9(variables=None, problem_size=None):
    problem_size = len(variables)
    return np.sum(np.abs(variables**2 - 10*np.cos(2*np.pi*variables) + 10))

def ray_f10(variables=None, problem_size=None):
    problem_size = len(variables)
    return -20*np.exp(-0.2*np.sqrt(np.sum(variables**2)/problem_size))-np.exp(np.sum(np.cos(2*np.pi*variables))/problem_size)+20+np.exp(1)

def ray_f11(variables=None, problem_size=None):
   # Griewank function
    problem_size = len(variables)
    w=[i for i in range(problem_size)]
    w=[i+1 for i in w]
    return np.sum(variables**2)/4000-np.prod(np.cos(variables/np.sqrt(w)))+1

def ray_f12(variables=None, problem_size=None):
   # tyblinski-Tang
   tmp1 = 0
   problem_size = len(variables)
   for i in range(problem_size):
     tmp1 += np.power(variables[i],4)-16*np.power(variables[i],2)+5*variables[i]
   return tmp1/2

def ray_f13(variables=None, problem_size=None):
    #Csendes Function
    return (np.power(variables,6) * (2 + np.sin(1/variables))).sum()

def ray_f14(variables=None, problem_size=None):
    # Xin-She Yang function 3 (should be 2)
    problem_size = len(variables)
    tmp1 = 0
    tmp2 = 0
    for i in range(problem_size):
        tmp1 += np.absolute(variables[i])
        tmp2 += np.sin(np.power(variables[i],2))
    return tmp1*np.exp(-tmp2)

def ray_f15(variables=None, problem_size=None):
    #Alpine Function No.01
    problem_size = len(variables)
    return np.sum(np.abs(variables[i] * np.sin(variables[i]) + 0.1 * variables[i]) for i in range(problem_size))

def ray_f16(variables=None, problem_size=None):
   # Michalewicz
   problem_size = len(variables)
   m = 10
   tmp1 = 0
   for i in range(problem_size):
     tmp1 += np.sin(variables[i])*np.power(np.sin((i+1)*np.power(variables[i],2)/np.pi),2*m)
   return -tmp1


def rray_f1(variables):
  return ray_f1(variables)

def rray_f2(variables):
    return ray_f2(variables)

def rray_f3(variables):
  return ray_f3(variables)

def rray_f4(variables):
  return ray_f1(variables)

def rray_f5(variables):
  return ray_f5(variables)

def rray_f6(variables):
  return ray_f6(variables)

def rray_f7(variables):
  return ray_f7(variables)

def rray_f8(variables):
  return ray_f8(variables)

def rray_f9(variables):
  return ray_f9(variables)

def rray_f10(variables):
  return ray_f10(variables)

def rray_f11(variables):
  return ray_f11(variables)

def rray_f12(variables):
  return ray_f12(variables)

def rray_f13(variables):
  return ray_f13(variables)

def rray_f14(variables):
  return ray_f14(variables)

def rray_f15(variables):
  return ray_f15(variables)

def rray_f16(variables):
  return ray_f16(variables)

class CEC2014:
  def __init__(self, jc, dim):
    self.jc = jc
    self.dim = dim

  def CEC1(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,1)
  
  def CEC2(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,2)
  
  def CEC3(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,3)
  
  def CEC4(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,4)
  
  def CEC5(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,5)
  
  def CEC6(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,6)
  
  def CEC7(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,7)
  
  def CEC8(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,8)
  
  def CEC9(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,9)
  
  def CEC10(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,10)
  
  def CEC11(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,11)
  
  def CEC12(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,12)

  def CEC13(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,13)
  
  def CEC14(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,14)
  
  def CEC15(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,15)
  
  def CEC16(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,16)
  
  def CEC17(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,17)
  
  def CEC18(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,18)
  
  def CEC19(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,19)
  
  def CEC20(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,20)
  
  def CEC21(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,21)
  
  def CEC22(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,22)
  
  def CEC23(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,23)
  
  def CEC24(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,24)
  
  def CEC25(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,25)
  
  def CEC26(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,26)
  
  def CEC27(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,27)
  
  def CEC28(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,28)
  
  def CEC29(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,29)
  
  def CEC30(self, solution):
      return self.jc.test_func(solution.tolist(),[0],self.dim,1,30)
