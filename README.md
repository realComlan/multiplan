# Multi-agent planning for Treasure Hunting


## 1. Introduction
To solve the posed treasure collection problem, we propose a Python program based on basic data classes and equipped with a graphical interface that facilitates the experimentation of our solution approach on a large number of problem instances. It is possible to speed up or slow down the execution, restart, generate new instances, and pause the execution at any time to examine the behaviors of the different elements more closely.
The code of the Environment.py file has not been modified and is located in the main directory of the project.
This report briefly presents the algorithms used and indicates the parts of the code (well-documented) that implement them.
### 2. The Code
#### 2.1 Prerequisites
The code requires the installation of version 2.5.2 of the pygame module used to develop the graphical interface.
This can be done automatically by executing the install-requirements.sh script from the main directory of the project.

```bash
bash install-requirements.sh
```
## 2.2 Execution
The simplest way to execute the program is through the following command, to be launched from the main directory of the project:
```bash
python main.py
```
Running this command launches the program by automatically generating an environment file (in the ./environments/ directory) and then launching the graphical interface of the program, which will display the initial state of the environment.

To specify a customized environment file, simply launch the program with the following command:
```bash
python main.py env=path/to/env###.txt
```
Then, press the yellow "go" button located at the bottom left of the program window.
