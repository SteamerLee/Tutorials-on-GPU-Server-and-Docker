# CEC 2014 Benchmark in Python
The repo shows how to call the IEEE Congress on Evolutionary Computation (CEC) 2014 competition benchmark functions in Python. There are 30 functions provided here.

## Requirements
Python library:
```
Python 3.x, numpy, pandas, scikit-opt, matplotlib, JPype1
Command: pip install <library name> 
```
Java SE Development Kit:
```
- Download from [Here](https://www.oracle.com/java/technologies/downloads/) (Say select "x64 Compressed Archive" in Linux for the server.)
- Unzip the file: tar -xvf jdk-xxx.tar.gz
- Edit the below information (environment variables) at the end of the file '~/.bashrc':
    export JAVA_HOME=/home/farryniu/Install/JDK/jdk-11  ## jdk所在目录
    export CLASSPATH=.:${JAVA_HOME}/lib
    export PATH=${JAVA_HOME}/bin:$PATH 
- Activate the file: source ~/.bashrc
```

## Introduction
- func_test.py: Program entrance
- graph_gen.py: Draw the convergence graph.
- problemSet.py: Define the benchmark functions.
- input_data: Save the parameters of the benchmark functions.