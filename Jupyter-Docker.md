# Guidance on Remotely Connecting Jupyter Notebook in Docker
The tutorial shows how to remotely connect the jupyter notebook running in the docker from your desktop step by step.

To explain the steps clearly, an example will be used here. We assume that:
- Host: your desktop
- Host port for connecting jupyter notebook: 9999
- IP address in remote server: 148.1.32.96
- Port for ssh in remote server: 22
- Username in remote server: hello
- Port for communication between remote server and container: 50000 (server-side) and 8888 (container-side)

**Reminder**: As the range of available ports number is between 0 and 65535, and most registered ports for services are distributed between 0 and 49151, it could be better to check the port number status first and set the port number larger than 49151 to avoid the collision. 

## Step 1: Prepare the docker and Jupyter notebook
- Login to the remote server with your account via ssh.
- Download a docker image.
- Build a docker container for your project. Please carefully set the port number for communication here.
```
docker run -itd -p <remote server port>:<container port> -name <container name> -v <file path in remote server>:<file path in container> <docker image repository>:<docker image tag>

Example:
docker run -itd -p 50000:8888 --name jupyter -v /home/hello/mnist:/program  pytorch/pytorch:latest
```
- Enter the interactive mode in the container:
```
docker exec -it <container name> bash
```
- Install jupyter notebook in the container:
```
pip install Jupyter
```
- Generate the configuration file for Jupyter notebook:
```
jupyter notebook --generate-config
```
- Set the password for entering the jupyter notebook:
```
jupyter notebook password
```
- Modify the configuration file. Open the file:
```
vim ~/.jupyter/jupyter_notebook_config.py
```
``` 
Common commands in 'vim' editor.
- click 'i' to enter the insert mode.
- click 'Esc' to exit the insert mode.
- click 'Shift' + ':' to enter the command mode.
- click 'w' + 'q' to save file and exit the editor.
- click 'q' to exit the editor without save.
```
Add the information at the end of the file:
```
c.NotebookApp.allow_remote_access = True
c.NotebookApp.open_browser = False
c.NotebookApp.ip = '*'
c.NotebookApp.allow_root = True
c.NotebookApp.port = 8888
```
- Start the jupyter notebook engine in the container.
```
jupyter notebook --no-browser --port=<container port> --ip=0.0.0.0 --allow-root

Example:
jupyter notebook --no-browser --port=8888 --ip=0.0.0.0 --allow-root
```
If you want to keep the jupyter notebook engine running after exiting the interactive window, please use 'nohup' command to run the engine in the background, and also keep your container running at the same time.

## Step 2: Build the connection between your desktop and jupyter notebook
- Open another terminal and type:
```
ssh -N -L <IP address for opening jupyter notebook in host>:<Port in host>:<>

Example:
ssh -N -L localhost:9999:localhost:50000 -p 22 hello@148.1.32.96
```
- Open your browser and type:
```
http://127.0.0.1:9999
```
- The jupyter notebook will be opened after keying the password.

## Kindly reminder
- Please use 'docker rm \<container name\>' to remove the unnecessary container, otherwise, it may occupy the resource all the time.
- Jupyter notebook is a convenient tool for visualizing the middle steps. But for the program that needs to run a long time, I'd suggest running the program in the background with **nohup** and use 'kill -9 \<process ID\>' if you would stop the program.
