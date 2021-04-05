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
    - Open PuTTY and connect to Host name `raspberrypi.local` or IP Address (find by typing `arp -a` in laptop's terminal ) with SSH connection
    - Login with the following details:
        ```
        Username: pi
        Password: mechfly23
        ```
    - Find Pi's IP address with by typing `ifconfig` in terminal
    - Run the following commands
        ```
        $ cd Desktop
        $ sudo python3 startup_script.py $PI'S_IP_ADDRESS
        ```
    - To run server code directly without the looping through network function of `startup_script.py`
        ```
        $ sudo python3 netgear_server.py $PC'S_IP_ADDRESS 8080
        ```
2. PC
    - Open terminal
    - Run `ipconfig` and look for the PC's ip address
    - Run the following command to run tic tac toe helper
        ```
        $ python netgear_client.py $PC'S IP_ADDRESS 8080
        ```
    - Run the following command to run HSV slider to calibrate HSV values. Note that there are three color options available: `red`, `green`, and `white`
        ```
        $ python HSVforRPi.py $PC'S_IP_ADDRESS 8080 $COLOR
        ```

# To-Do List
Prep:
- [X] Convert Kieren's HSV slider code to be compatible with VidGear
- [X] Backup code to github
- [ ] Bind laptop's IP address to router (Optional)

D-Day:
- [ ] Use the hsv slider code to adjust the values in `netgear_client.py`