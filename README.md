
# Elevator System

An app that controls the movement of elevators in a building. The algorithm is written in Python, and the app itself in HTML, CSS and JavaScript, thanks to the awesome [Eel](https://github.com/ChrisKnott/Eel) library.

## Features:
- Pickup - specify a pickup and dropoff floor
- Status - show status of all elevators
- Update - show update about the status status of a specified elevator
- Step - go one step further in the simulation


## Requirements:
- [Python](https://www.python.org/downloads/)
- [Eel](https://github.com/ChrisKnott/Eel)

## Running the app:
1. Download and install [Python](https://www.python.org/downloads/).
2. Install [Eel](https://github.com/ChrisKnott/Eel) with pip: ```pip install eel```
3. Clone this repository: ```git clone <link_to_the_repository>```
4. Open command line in the root folder of the cloned repository, and type ```python main.py```
5. If the GUI doesn't open automatically, type ```http://localhost:8000``` in your web browser.

## Troubleshooting:
- I get an error ```OSError: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions: ('localhost', 8000)```

That error occurs when port 8000 is occupied by something else and cannot be used to run the app. To fix that, open ```main.py``` in a text editor, scroll down to the last line of code, and add option ```port=xxxx``` where ```xxxx``` is a random number of your choice. The line should now look like that:
```eel.start('index.html', size=(1500, 900), port=764)```.
Repeat the steps until you encounter a port number that is not occupied.

## Explanation of the algorithm:

An elevator control system which supports up to 16 elevators.

It's able to provide status updates for all elevators, update on a specific elevator, time step forward or accept a pickup requests. The algorithm tries to minimize the waiting time and maximize the number of working elevators.

When a pickup request comes in, the first thing the app does is try to find an elevator that is currently not in use. Once it finds an idle elevator, it searches for the closest one and assigns it the task.

If the pickup and dropoff locations are in the same direction the elevator is going, it simply adds both to the goal and moves forward.

If the elevator is required to change a direction at some point (for example, the elevator is currently on the 5th floor, a request is received to go from 1st to 2nd floor), the elevator will start going down towards the 1st floor, and will be able to process other requests along the way, such as  5th to 4th, or 4th to 2nd or even 1st to 0th, as it behaves like a normal elevator. As soon as it's done moving downwards, floor 1 and 2 are readded as goal floors and the elevator starts moving upwards.

If all the elevators are busy, the algorithm checks if there's an elevator that is moving in the same direction as our pickup location and is expected to reach it along the way, and assigns the task to that elevator. Should there be no such elevators, it holds off on this request until one of the elevators becomes free.