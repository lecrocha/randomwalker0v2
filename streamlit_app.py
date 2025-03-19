#=========================================================================================================================================================
# Author: Luis E C Rocha - Ghent University, Belgium  - 26.09.2022
#
# Description:  This file contains the implementation of multiple Random Walkers on a grid
#               On the left panel, the movement of all RWs simultaneously
#               On the right panel, it shows the historical trajectory of a single walker
#               1. first install streamlit using "pip install streamlit" 
#               2. when you run streamlit, it will open a tab in your default browser with the streamlit application *it works as a webpage hosted at the following URL:  Local URL: http://localhost:8501
#
#=========================================================================================================================================================

# Import essential modules/libraries
import numpy as np
import pandas as pd
import random as rg
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from time import sleep  # this is used to add a delay for each time step

#===============================================================================================================
# THIS IS THE DEFINITION OF THE CLASS FOR THE MODEL
class RandomWalker:

    #===================================================================
    # This method initialises the system
    def __init__(self, N, no_walkers, boundary):

        # These are the parameters of the model, input by the user
        self.N = N
        self.no_walkers = no_walkers
        self.boundary = boundary

        # This is the size of the system - Ps: this little trick just makes sure the system (grid) will have integer length for a square grid
        NN = int(np.sqrt(self.N))**2
        self.grid_size = int(np.sqrt(NN))

        self.grid = np.zeros([self.grid_size, self.grid_size])

        # Set an empty list to store the position of all RWs
        self.pos_walkers = []
        
        #---------------------------------------------------------------
        # INITIAL POSITION OF THE RANDOM WALKERS
        for i in range(self.no_walkers):
            pos_x = rg.randint(0, self.grid_size-1)
            pos_y = rg.randint(0, self.grid_size-1)
            self.grid[pos_x, pos_y] = 1
            self.pos_walkers.append([pos_x, pos_y])


    #====================================================================
    # MODEL: This method updates the position of the walkers in the grid
    def run(self):

        #-----------------------------------------------------
        # This loop checks if the walker can move to one of the neighbours empty cells
        # The loop is repeated to check every RW
        for i in range(self.no_walkers):

            pos_x = self.pos_walkers[i][0]
            pos_y = self.pos_walkers[i][1]

            next_position_direction = rg.randint(0, 3)

            pos_xx, pos_yy = self.next_position(next_position_direction, pos_x, pos_y)

            # if the cell is free, move the RW there
            if self.grid[pos_xx, pos_yy] == 0:
                self.grid[pos_xx, pos_yy] = 1
                self.grid[pos_x, pos_y] = 0
                self.pos_walkers[i][0] = pos_xx
                self.pos_walkers[i][1] = pos_yy
            # else, keep the RW in the original position
            
            # ALTERNATIVE IMPLEMENTATION: one can also have multiple walkers on the same cell

    #====================================================================
    # This method calculates the next x,y position of the walker - periodic boundaries
    def next_position(self, direction, pos_x, pos_y):

        pos_xx = pos_x
        pos_yy = pos_y

        # For periodic boundary conditions
        if self.boundary == "Periodic":
            if direction == 0:
                if pos_x == 0:
                    pos_xx = self.grid_size-1
                else:
                    pos_xx = pos_x - 1

            elif direction == 1:
                if pos_y == 0:
                    pos_yy = self.grid_size-1
                else:
                    pos_yy = pos_y - 1

            elif direction == 2:	
                if pos_x == self.grid_size-1:
                    pos_xx = 0
                else:
                    pos_xx = pos_x + 1
                    
            elif direction == 3:
                if pos_y == self.grid_size-1:
                    pos_yy = 0
                else:
                    pos_yy = pos_y + 1

        # For mirror boundary conditions
        elif self.boundary == "Mirror":
            if direction == 0:
                if pos_x == 0:
                    pos_xx = 1
                else:
                    pos_xx = pos_x - 1

            elif direction == 1:
                if pos_y == 0:
                    pos_yy = 1
                else:
                    pos_yy = pos_y - 1

            elif direction == 2:
                if pos_x == self.grid_size-1:
                    pos_xx = self.grid_size-2
                else:
                    pos_xx = pos_x + 1

            elif direction == 3:
                if pos_y == self.grid_size-1:
                    pos_yy = self.grid_size-2
                else:
                    pos_yy = pos_y + 1

            # For absorbing boundary conditions
            # Can you code such boundary conditions? i.e. the walker disappears once it hits the border
            # see solution in the first exercise

        return(pos_xx, pos_yy)

    #====================================================================
    # Returns the x,y position of the first walker
    def position_firstwalker(self):

#        print(self.pos_walkers[0][0], self.pos_walkers[0][1])
        return([self.pos_walkers[0][0], self.pos_walkers[0][1]])

    #====================================================================
    # EXERCISES: Can you measure the distance - in terms of cells - from the start position over time?


#===============================================================================================================
# VISUALISATION OF THE MODEL DYNAMICS USING THE streamlit FRAMEWORK (see more on https://streamlit.io/)

#--------------------------------------------------------------------------------------------------
# Title of the visualisation - shows on screen

st.title("Random Walk model")

# This method is used to fix the random number generator. Use it for testing. Remove it to make analysis
#np.random.seed(0)

#--------------------------------------------------------------------------------------------------
# Methods to interactively collect input variables

N = st.sidebar.slider("Population Size", 5, 10000, 4900)
no_walkers = st.sidebar.number_input("Number of Walkers", 1)
boundary = st.sidebar.radio("Boundary Conditions", ('Periodic', 'Mirror'))
no_iter = st.sidebar.number_input("Number of Iterations", 10)
speed = st.sidebar.number_input("Speed Simulation", 0.0, 1.0, 1.0)


#--------------------------------------------------------------------------------------------------
# Initialise the object   - Note that when one runs the code, the selected parameters will be passed here during the initialisation of the object via "self" method

randomwalker= RandomWalker(N, no_walkers, boundary)

#--------------------------------------------------------------------------------------------------
# Initialise a list trajectory to store the position over time

trajectory = []
trajectory.append(randomwalker.position_firstwalker())

#--------------------------------------------------------------------------------------------------
# Create placeholders for the plot and progress indicators
plot_placeholder = st.empty()
iteration_text = st.empty()

# Display the initial state: an empty grid and setup for the trajectory plot
fig = plt.figure(figsize=(8, 4))

# Left grid - lattice that will show the positions of the random walkers at the current time step
ax1 = plt.subplot(121)
ax1.axis('off')
cmap = ListedColormap(['white', 'red']) # Define the colormap for visualization
ax1.pcolormesh(0*randomwalker.grid, cmap=cmap, edgecolors='k', linewidths=0.01)

# Right grid - lattice that will show the historical positions of the first random walker (only the first, otherwise, too much information on the screen)
ax2 = plt.subplot(122)
ax2.set_title("Trajectory first walker", fontsize=15)
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_xlim([0, randomwalker.grid_size])
ax2.set_ylim([0, randomwalker.grid_size])

# This function draw the figure (in object) fig on the screen
plot_placeholder.pyplot(fig)
plt.close(fig)

# This part shows a progress bar
iteration_text.text("Step 0")
progress_bar = st.progress(0)
progress_bar.progress(0)

#===============================================================================================================
# RUN THE DYNAMICS (IF THE USER CLICKS ON "Run") FOLLOWING THE RULES DEFINED ABOVE IN "RUN"

if st.sidebar.button('Run'):

    # Run the simulation for no_iter iterations, i.e. total time of the simulation
    # Repeat routines below for each time step i
    for i in range(no_iter):

        # Add a little time delay otherwise the patterns update too fast on the screen
        sleep(1.0-speed)

        # Call the method "Run" with the interaction rules
        # Here you can test the other algorithms to update the state and then visualise what happens
        randomwalker.run()

        #-----------------------------------------------------
        # CONTAGION DYNAMICS
        # Once all RWs update their position at the current time step, you can check who is in the neighbourhood 
        # (i.e. "touching") the RW (or the RWs) with "the piece of information" (or "the infection")
        # For example, you can scan all RWs and if the RW is infected, check who is in its neighbourhood
        # Attention: Remember to keep two lists of states (e.g. infected or not), one for the current time step and one for the updated time step, otherwise, the states at different times will mix up

        #-----------------------------------------------------
        # Measure position and append the results on the list "trajectory" - Ps: By the end of the simulation, this list contains all positions of the first random walker, for all time steps
        trajectory.append(randomwalker.position_firstwalker())

        #--------------------------------------------------------------------
        # Visualisation of the evolution - Ps: This part has to be the same as above
        fig = plt.figure(figsize=(8, 4))
    
        # left grid - lattice with the positions of all random walkers
        ax1 = plt.subplot(121)
        ax1.axis('off')
        ax1.pcolormesh(randomwalker.grid, cmap=cmap, edgecolors='k', linewidths=0.01)

        # right grid - lattice with the positions of the first random walker
        ax2 = plt.subplot(122)       
        ax2.set_title("Trajectory first walker", fontsize=15)
        ax2.set_xlabel("x")
        ax2.set_ylabel("y")
        ax2.set_xlim([0, randomwalker.grid_size])
        ax2.set_ylim([0, randomwalker.grid_size])

        # Draw the initial value of measure 1 on top of the plot
        ax2.text(1, 0.95, "x,y: %.f,%.f" % (randomwalker.position_firstwalker()[1], randomwalker.position_firstwalker()[0]), fontsize=8)

        # Plot the entire list with the values of measure_2 (from time 0 to current time) on the graph
#        plt.scatter(*zip(*trajectory), s = 0.1*randomwalker.grid_size, marker="s", alpha = 0.3)

        # Extract x and y coordinates for plotting (note: using column for x, row for y)
        xs = [pos[1] for pos in trajectory]
        ys = [pos[0] for pos in trajectory]
        ax2.scatter(xs, ys, s=0.1 * randomwalker.grid_size, marker="s", alpha=0.3, color='blue', edgecolors='none')


 #       df1 = pd.DataFrame(trajectory)
 #       ax2.scatter(df1.iloc[:,1], df1.iloc[:,0], s = 0.1*randomwalker.grid_size, marker="s", alpha = 0.3)
        
        # Draws the figure (in the object) fig on the screen
        plot_placeholder.pyplot(fig)

        # Closes the figure instance (to replot them in the next time step)
        plt.close(fig)

        # Updates the progress bar
        iteration_text.text(f'Step {i+1}')
        progress_bar.progress( (i+1.0)/no_iter )
    
        #--------------------------------------------------------------------
