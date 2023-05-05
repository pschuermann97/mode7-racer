# mode7-racer
Prototype F-Zero-style racing game made with Python/pygame.

<p float="left">
  <img width="448" alt="0" src="https://user-images.githubusercontent.com/28012017/235456613-3b90fb13-49b9-4e57-9858-cec4e5bd37cd.png">
  <img width="448" alt="1" src="https://user-images.githubusercontent.com/28012017/235456656-672e1c48-5d49-4b36-acf8-dbaac1d18623.png">
</p>

<p float="left">
  <img width="448" alt="2" src="https://user-images.githubusercontent.com/28012017/235456666-2fbcc8e8-52da-46f9-be8d-3eae1fcce96b.png">
  <img width="449" alt="3" src="https://user-images.githubusercontent.com/28012017/235456683-48ec5b33-b2ac-4ee9-9655-f82cf4b70983.png">
</p>

The Mode7 rendering module used in this implementation is based on the Mode7 tutorial by Coder Space (https://www.youtube.com/watch?v=D0MPYZYe40E).

If you want to experiment with the code of the game prototype, see paragraph "Installation instructions" below.
If you want to just try out the prototype and do not want to install the required dependencies on your machine, see "Test build".

## Installation instructions

1. Install Python version 3.10 on your machine (https://www.python.org/downloads/release/python-31011/). In this project, Python 3.10.10 was used. Note that the project's scripts will NOT run with the Python 3.11 interpreter since not all dependencies work with Python 3.11.
2. Install pygame 2.2.0. If you are using pip to manage your Python packages, this can be done by running the command `pip install pygame==2.2.0`.
3. For performance optimization and to be able to run the Mode7 renderer in real time, this implementation uses the Python just-in-time compiler numba (https://numba.pydata.org/) which compiles numerical functions to machine code at runtime to greatly accelerate their execution.
For this implementation, numba version 0.56.4 was used which you can install via pip by running the command `pip install numba==0.56.4`.
Note: numba does not work with Python 3.11 yet (May 1, 2023).
4. Clone this repository to your machine using `git clone`.
5. Navigate to the root folder of this repository and run the script `main.py` using the Python interpreter.

## Test build

You can find a test build under https://pschuermann97.itch.io/mode7-racer which features 4 consecutive races.
The controls for the game are as follows:

- A/D: steer
- K: accelerate
- J: break
- L: use booster (unlocked after finishing one lap)
- R: restart race

Every race requires 3 laps to complete.
After finishing a race, press K to skip to the next one.
