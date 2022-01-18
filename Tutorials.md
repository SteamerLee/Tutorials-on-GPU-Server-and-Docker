# The Use of GPU Server
The repo aims to provide some useful suggestions and guidance for better understanding the use of our machines on your projects. The servers run on Ubuntu 16.04 with 1080Ti graphic card unit. The content of repo contains:
- [How to login user account](#topic1)
- [How to run your project in a docker container](#topic2)
- [Kindly reminder](#topic3)
- [Useful tools](#topic4)
- [Useful links](#topic5)

## <span id="topic1">How to login user account</span>
Usually, we remotely login the GPU server via [SSH](https://www.ssh.com/ssh/) protocol.

**For Windows User:** 

Step 1: Check that your computer has turned on SSH service. 

- Open CMD Command Prompt, type `ssh` and run. The SSH service has been turned on if it shows the usage help, then you can try to login the server remotely on your computer [[See Step2]](#Step2). Otherwise, you have to turn on SSH service before login.
- Turn on SSH Client Service: System Settings -> Apps -> Apps & features -> Optional features -> Add a feature -> Tick `OpenSSH Client` and install. After installing, restart system and run `ssh` on CMD Command Prompt to check if successfully turning on.
- Alternatively, [PuTTY](https://www.ssh.com/ssh/putty/) can be used to login remote server, which is a versatile terminal program for Windows.

<span id="Step2">Step 2:</span> Login your account remotely. Type below command on CMD and click `Enter`:
```
ssh [username]@[ip_address] -p [port_number]
```
Command example:
```
ssh jack@148.7.189.53 -p 22 
```
Then type your password and click `Enter`. The password will not be visible when typing. After that, you can run your program on remote GPU server.

**For Linux/Ubuntu/macOS User**

Open the terminal, type below command on CMD and click `Enter`:
```
ssh [username]@[ip_address] -p [port_number]
```
Command example:
```
ssh jack@148.7.189.53 -p 22 
```
Then type your password and click `Enter`. The password will not be visible when typing. After that, you can run your program on remote GPU server.

For better visualizing remote folder on your computer, I'd suggest you download a manager client called WinSCP (for Windows) or cyberduck (for macOS).


## <span id="topic2">How to run your project in a docker container</span>
Since different programs may depend on various development environments, a version control system is necessary. [Docker](https://www.docker.com/) is an open-source and free platform for developing/running/packing the program and its dependencies into a virtual container, which is separated from the server environment and can be treated as a virtual machine. Hence, We'd suggest you run your programs in your own docker container.

**Check the existing docker images**

Type and run `docker images` on terminal, the existing docker images will be listed. Then, select the appropriate one to build the container. If you cannot find the docker images you wanted, please try to run below command to achieve.
```
docker pull [image_name]
``` 
Most of docker images can be found from [Docker hub](https://hub.docker.com/).

**Build a docker container for your project**

```
docker run [options] [image_name] [command] [arg]
```

Usual optional parameters:
- **-i**: Run container with interactive mode.
- **-t**: Allocate a pseudo terminal.
- **-d**: Run container in background.
- **-p**：Publish a container's port(s) to the host. [Host port:Container port]
- **--name**:  Assign a name to the container.
- **-v**: Bind mount to volume, that is folder on server mapped to a folder on container. [Host path:Container path]
- **-gpus**: Enable GPU devices in your container. (E.g., --gpus all) for all GPUs.

Example 1:
```
docker run -p 51000:22 -v /program/mnist:/code/mnist --name MNIST_CONTAINER -d mxnet/python:latest
```
A container will be created and run in background. Use `docker exec` command if you want to enter interactive mode.

Example 2:
```
docker run -p 51000:22 -v program:/program --name MNIST_CONTAINER -it mxnet/python:latest
```
A container will be created and run in interactive mode, and will be stopped after you exit the container.

**More useful docker commands**

`docker images`: Check all existing docker images.

`docker ps -a`: Check all existing docker containers.

`docker start [CONTAINER_ID/NAME]`: Restart a stopped container.

`docker stop [CONTAINER_ID/NAME]`: Stop a running container.

`docker exec -it [CONTAINER_ID/NAME] /bin/bash`: Enter the interactive mode in a running container.

`docker rm [CONTAINER_ID/NAME]`: Remove containers.

`docker rmi [CONTAINER_ID/NAME]`: Delete docker images.

**Docker Tutorials**

For more information on Docker use, please access below websites:

English version: <https://docs.docker.com/get-started/overview/>

Chinese version: <https://www.runoob.com/docker/docker-tutorial.html>

For executing your code in container, please refer tutorials about running program on Linux/Ubuntu.

## <span id="topic3">Kindly reminder</span>
- Please change your password after login at the first time. Execute `passwd` on your terminal when login server remotely, then type the old and new passwords.
- As the SSD (Solid-state Dive) space is limit, please place large dataset to HDD (Hard Disk Drive). The location path of HDD can be found below:
    - `/opt/Disk2` For "New AI OPT Group"
    - `/storage1` For "Deep Learning Group"
- Please keep your account for your own use and don't distribute them to public.
- As the computational resource is very limit, please stop running meaningless programs and don't occupy all GPU/CPU resource for a long time. Alternatively, you may run your program on cloud server provided by Amazon, Ali Cloud, Microsoft Azure, etc.

## <span id="topic4">Useful tools</span>
- [WinSCP](https://winscp.net/eng/download.php)
- [VS Code](https://code.visualstudio.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/): Register student account for better using remotely debugging function.
- [PuTTY](https://www.ssh.com/ssh/putty/)
- [Anaconda](https://www.anaconda.com/)
- [Github](https://github.com/): Manage your code and find the source code of popular algorithms.

## <span id="topic5">Useful links</span>

- [Coursera](https://www.coursera.org/learn/machine-learning): Provide a series of machine learning/deep learning online courses. 
- [Book: Deep Learning](https://www.deeplearningbook.org/): A popular deep learning textbook written by Ian Goodfellow and Yoshua Bengio.
- Book (Chinese version): Machine Learning (机器学习，周志华)
- Book (Chinese version): 统计学习方法（李航）
- [w3schools](https://www.w3schools.com/default.asp)
- [菜鸟教程](https://www.runoob.com/)
- SSH for Linux and Windows user: <https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows>
- SSH for macOS user: <https://osxtips.net/how-to-connect-to-macos-via-ssh/> or <https://www.servermania.com/kb/articles/ssh-mac/>
- [PuTTY Tutorial](https://www.siteground.com/tutorials/ssh/putty/)


Please feel free to let me know if you have any questions or advice, thanks!

Samuel
