# Import Statements
from Common_Libraries.p2_sim_lib import *
from time import sleep
from random import choice

# Documented Autoclave Bin Locations:
# Red Small: (-0.599, 0.239, 0.391)
# Green Small: (-0.0, -0.645, 0.391)
# Blue Small: (0.0, 0.645, 0.391)
# Red Large: (-0.4, 0.16, 0.18)
# Green Large: (0.006, -0.431, 0.18)
# Blue Large: (0.006, 0.431, 0.18)
# Start Position: (0.534, 0.0, 0.044)
# Home Position: (0.406, 0.0, 0.483)

# Chosen EMG Sensor Activation Combo: #3
# Chosen Threshold: 0.4
# Move End Effector: Left Sensor is zero & Right Sensor > 0.4
# Open Autoclave Drawer: Left Sensor > 0.4 & Right Sensor is zero
# Control Gripper: Left Sensor > 0.4 & Right Sensor > 0.4

# Assign Contstants
# List of autoclave locations determined through experimentation
LOCS = [[-0.599, 0.239, 0.391], [-0.0, -0.645, 0.391], [0.0, 0.645, 0.391], [-0.4, 0.16, 0.18], [0.006, -0.431, 0.18], [0.006, 0.431, 0.18]]

# Container spawn point coordinates as a list
CONTAINER_POS = [0.534, 0.0, 0.044]

# Arm home position coordinates as a list
HOME = [0.406, 0.0, 0.483]

# Instantiate qarm object
arm = qarm()

# Assign Functions
def id_autoclave_location(container_id):
    '''
    Function: id_autoclave_location()
    
    Purpose: This function takes a given containter id, identifies its corresponding autoclave, and finds its XYZ coordinates.
    
    Inputs: container_id (int) - id of the container to be sterilized
    Outpus: (list) - the XYZ coordinates of the corresponding autoclave as a list

    Author: Shyavan Sridhar
    '''
    # Checks which id was given as input, return respective locations from inside if statements for efficiency
    if container_id == 1:
        return LOCS[0]
    elif container_id == 2:
        return LOCS[1]
    elif container_id == 3:
        return LOCS[2]
    elif container_id == 4:
        return LOCS[3]
    elif container_id == 5:
        return LOCS[4]
    elif container_id == 6:
        return LOCS[5]

def move_end_effector(coords):
    '''
    Function: move_end_effector()
    
    Purpose: This function takes a given set of coordinates and moves the arm to that location if the emg sensors are at the correct threshold.
    
    Inputs: coords (list) - coordinates of the desired location
    Outpus: (bool) - returns True for ease of debugging when sucessfully completed

    Author: Haotian Sun
    '''
    # Assign Variables
    done = False

    # Loops until action is complete
    while not done:
        # Get emg sensor values to check if they are at the correct values for the required action
        right_sensor = arm.emg_right()
        left_sensor = arm.emg_left()
        if right_sensor > 0.4 and left_sensor == 0:
            # Move arm to specified location if emg sensor values are correct
            arm.move_arm(coords[0], coords[1], coords[2])
            
            # Give time for the action to complete
            sleep(3)
            done = True
    
    # Return True by default to signal successful completion
    return True

def open_autoclave_drawer(container_id, opened):
    '''
    Function: open_autoclave_drawer()
    
    Purpose: This function takes a given container id and opens or closes the corresponding autoclave drawer if required and if the emg sensors are at the correct threshold.
    
    Inputs: container_id (int) - id of the container to be sterilized,
            opened (bool) - whether the autoclave drawer should be opened or closed on this run of the function
    Outpus: (bool) - returns True for ease of debugging when sucessfully completed

    Author: Haotian Sun & Madhav Narang
    '''
    # Check if the container id is 1, 2, or 3 in which case the autoclave drawer need not be opened
    if container_id == 1 or container_id == 2 or container_id == 3:
        # Return False to signal no autoclave drawers opened
        return False

    # Assign Variables
    done = False

    # Loops until action is complete
    while not done:
        # Get emg sensor values to check if they are at the correct values for the required action
        right_sensor = arm.emg_right()
        left_sensor = arm.emg_left()
        if right_sensor == 0 and left_sensor > 0.4:
            # Open or close autoclave drawer corresponding to container id and boolean variable: opened
            if container_id == 4:
                arm.open_red_autoclave(opened)
            elif container_id == 5:
                arm.open_green_autoclave(opened)
            elif container_id == 6:
                arm.open_blue_autoclave(opened)
            
            # Give time for the action to complete
            sleep(3)
            done = True

    # Return True by default to signal successful completion
    return True

def control_gripper(angle):
    '''
    Function: control_gripper()
    
    Purpose: This function takes a given angle and closes or opens the gripper by that much accordingly if the emg sensors are at the correct threshold.
    
    Inputs: angle (int) - the angle that the gripper should be opened or closed to
    Outpus: (bool) - returns True for ease of debugging when sucessfully completed

    Author: Madhav Narang
    '''
    # Assign Variables
    done = False

    # Loops until action is complete
    while not done:
        # Get emg sensor values to check if they are at the correct values for the required action
        right_sensor = arm.emg_right()
        left_sensor = arm.emg_left()
        if right_sensor > 0.4 and left_sensor > 0.4:
            # Open or close gripper corresponding to the set angle
            arm.control_gripper(angle)

            # Give time for the action to complete
            sleep(3)
            done = True

    # Return True by default to signal successful completion
    return True

def main():
    '''
    Function: main()
    
    Purpose: This function is the main function to be run when not imported as a module.
    
    Inputs: None
    Outpus: None

    Author: Shyavan Sridhar
    '''
    # Generate list of 6 container ids (1-6)
    unsterilized_containers = list(range(1, 7))

    # Loop until list is empty, no remaining containers to sterilize
    while unsterilized_containers:
        # Randomly select one id from the list
        container_id = choice(unsterilized_containers)

        # Remove selected id from the list
        unsterilized_containers.remove(container_id)

        # Spawn in container with the selected id
        arm.spawn_cage(container_id)

        # Cycle arm movement to pick up container and drop it off at its determined autoclave location and return home for the next loop iteration
        autoclave_location = id_autoclave_location(container_id)
        move_end_effector(CONTAINER_POS)
        control_gripper(40)
        open_autoclave_drawer(container_id, True)
        move_end_effector(autoclave_location)
        control_gripper(-40)
        move_end_effector(HOME)
        open_autoclave_drawer(container_id, False)

# Call to main function
if __name__ == "__main__":
    main()
