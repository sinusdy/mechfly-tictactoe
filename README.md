# mechfly-tictactoe
Code for computer vision to play tic tac toe for Mechfly

# Code Installation
1. Raspberry Pi
    - Install required libraries
    ```
    $ sudo python3 -m pip install --pre scapy[basic]
    $ sudo apt-get install tcpdump
    $ sudo python3 -m pip install vidgear
    ```
    - Download files `netgear_server.py`, and `startup_script.py` to folder Desktop
    - Or checkout to branch **pi** and pull the files
    ```
    $ git clone https://github.com/sinusdy/mechfly-tictactoe.git
    $ git checkout -b pi
    $ git pull
    ```  
2. PC
    - Install required lilbraries
    ```
    $ sudo pip install vidgear
    $ sudo pip install opencv-python
    ```
    - Download file `netgear_client.py`, `minimax.py`, `TicTacToeModified.py`, and `HSVforRPi.py`
   - Or checkout to branch **pc** and pull the files
    ```
    $ git clone https://github.com/sinusdy/mechfly-tictactoe.git
    $ git checkout -b pc
    $ git pull
    ```   

# How to run code
1. Raspberry Pi
    - Open PuTTY and connect to Host name `raspberrypi.local` or `192.168.0.101` with SSH connection
    - Login with the following details:
        ```
        Username: pi
        Password: mechfly23
        ```
    - Run the following commands
        ```
        $ cd Desktop
        $ sudo python3 startup_script.py
        ```
2. PC
    - Open terminal
    - Run `ipconfig` and look for the PC's ip address
    - Run the following command
        ```
        python netgear_client.py $IP_ADDRESS 8080
        ```

# To-Do List
Prep:
- [X] Convert Kieren's HSV slider code to be compatible with VidGear
- [ ] Bind Pi's IP address to router to be `192.168.0.101`
- [ ] Backup code to github
- [ ] Bind laptop's IP address to router (Optional)

D-Day:
- [ ] Use the hsv slider code to adjust the values in `netgear_client.py`