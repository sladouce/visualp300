## Standard Visual P3 Experiment, utilising LSL for streaming events markers.
## Visual P300 ERP paradigm presenting blue rectangles (non-targets) and red circles (targets).
## Make sure you look over the libraries and make them available.
## This version will only work on Windows OS, change time, and keypress items if needing on other platforms.
## This was written in PsychoPy 2, compatibilities may arise with earlier versions. None known at moment of writing.
##----------------------------------------------------------------
## Make Sure you have Edited the file output to avoid overwriting.
##----------------------------------------------------------------
# Importing of Libraries.
import psychopy
from psychopy import visual, core, logging, event  # Import PsychoPy Presentation and Data Logging Libraries.
from psychopy.visual import ShapeStim, Circle, Rect # Import PsychoPy objects from PsychoPy.
import random
import numpy
import pylab
import csv
from datetime import datetime # Allows use of internal clock, in Windows.
from win32api import GetSystemMetrics # Allows you to detect the screen information. This only works with using 1 screen, in Windows.
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_byprop, local_clock

# Looks for the file name mentioned below and if there is none creates it. This txt file will be formated to allow for a CSV file format later, done for ease of formating.
file = open("visualTask-sl13nores.csv", "w+") # Change name as wanted. -1-1 is in reference to participant and session number, for differentiation.
print ("Name of the file:" , file.name) # Will write name of file in the command line for you.
dataVariableNames = "trialNumber,setNumber,shape,responseTime,triggerOutput\n"
file.write(dataVariableNames)

# Initializations, Constants and Counters.
nTarget = 1 # Number of Targets.
nNonTarget = 3 # Number of non Targets minus one.
shapes = [0]*nTarget + [1]*nNonTarget # Populate list with 1 and 0 based on constants above.
nSets = 10# Number of desired sets of targets and non targets you want to present.
nTrials = nSets * len(shapes) # Setting trial number by number multiplying number of sets by the length of the set.
REFRESH_RATE = 60 # Declaring of refresh rate, use GetSystemMetrics if you want to get screen actual refresh rate.
RR = 1/REFRESH_RATE # Milliseconds for 1 Hz.
random.seed(datetime.now())

# Marker stream
info = StreamInfo(name='MyMarkerStream', type='Markers', channel_count=1,
                  nominal_srate=0, channel_format='string', source_id='myuidw43536')
outlet = StreamOutlet(info)


# Size of monitor, detects the resolution and will always present on monitor 1. Need to specify if have multiple screens.
WINWIDTH = GetSystemMetrics (0)
WINHEIGHT = GetSystemMetrics (1)

# Main Window Settings.
main_win = visual.Window(size=(WINWIDTH, WINHEIGHT), units='height', fullscr = True)
main_win.color = 'white' # Colour for window Popup, if using non specified Black and White then define colour beforehand and call upon.


# Establishing data logging warnings.
logging.console.setLevel(logging.WARNING)

# Parameters for fixation cross, rectangle, and circle.
circle = Circle(main_win, units="pix", radius=150, fillColor='red', lineColor=[-1, -1, -1], edges=128)
rect = Rect(main_win, units="pix", width=300, height=300, fillColor='blue', lineColor=[-1, -1, -1])
button = visual.Rect(main_win, name='button', width=(0.4, 0.4)[0], height=(0.1, 0.1)[1], ori=0, pos=(0,-0.2),
        lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb', fillColor=[0,0,0], fillColorSpace='rgb', opacity=1, depth=-1.0, interpolate=True)
fixation = visual.GratingStim(win=main_win, size=0.2, pos=[0,0], sf=0, rgb=-1, mask='cross')
fixation.color = 'black'

# Instructions for study.
instructions = "Please count the number of circles. \n \
                \nDo not count the squares. \n \
                \nTap the button below to start." 
                

# Goodbye Message.
goodbye = " Thank you for taking part in the study."

# Need to allow for touchscreen options and moving things along.
mouse = event.Mouse(visible = True, win = main_win) # Mouse can visible or invisible.
expClock = core.Clock() # Start clock for study.

## -----------------------Main Study Body.----------------------------------------
# Present the Introduction.
imessage = visual.TextStim(main_win, contrast = 0, text = instructions, height = 0.03, font = 'Arial', pos = (0, 0))
mouse.clickReset()
clicked = False

# Move on from introduction if the mouse is clicked on box.
while clicked is False:
    if button.contains(mouse):
        clicked = True
    else:
        imessage.draw()
        button.draw()
        main_win.flip()
    
# Setup for fixation cross at the beginning of study.
for frameN in range(2 * REFRESH_RATE): # Display Fixation cross for (n x Refresh_Rate), so will present for n seconds.
    fixation.draw()
    main_win.flip()

main_win.setRecordFrameIntervals(True)
main_win.refreshThreshold = RR + 0.004 # RR Correction.

# Setup for a blank screen seperating cross from main study.
for frameN in range(1 * REFRESH_RATE): # Blank screen presentation for (n x REFRESH_RATE), so will present for n seconds.
    main_win.flip()

# As we count cicle and rectangles, we delcare them here.
number_of_circle = 0
number_of_rect = 0
numberTrial = 0

for set in range(nSets):
    
    # Shuffle the order of the shapes list.
    random.shuffle(shapes)
    trials = (shapes) # Not really needed, but good for structure recall later.
    print("Trial List: 1 ", trials) # Prints the set order in Output, to make sure that the object presentation is same order as the randomised sets.
    
    # first non target stim for pseudo randomized presentation order
    stimStart = core.getTime()
    numberTrial = numberTrial + 1
    number_of_rect += 1
    shape = rect
    cShape = 'rectangle'
    marker_info = ["non-target"]
    outlet.push_sample(marker_info)
    for frameN in range(1 * REFRESH_RATE): # For (n * refresh rate) present rectangle.
        if frameN < 0.2 * REFRESH_RATE: # Draw this for (n * refresh rate)...
            rect.draw()
            main_win.flip()
            response = stimStart # To account for no button press, given stimStart time, so RT = 0.
        else:
            main_win.flip() # Then present a blank screen.
    nTrial = str(numberTrial)
    numberSet = str(set)
    nShape = str(cShape)
    responseTime = str(response - stimStart)
        
    trialOutput = nTrial + ',' + numberSet + ',' + nShape + ',' + responseTime + ',' + '\n'
    file.write(trialOutput)
    
    
    # Run the set based on parameters below.
    for trial in range(len(trials)): # Set will run for the length of the trials list.
            # Add 1 per trial.
            numberTrial = numberTrial + 1
            mouse.setPos(newPos=(100,100))
            # Find the time for each trial.
            stimStart = core.getTime()
      
            # If Trial is a 0, then make shapeArray value a circle, and count.
            if shapes[trial] == 0:
                number_of_circle += 1
                shape = circle
                cShape = 'circle'
                marker_info = ["target"]
                outlet.push_sample(marker_info)
                mouse.clickReset() # Reset clicks on mouse between trials.
                clicked = False # Reset clicked status between trials.
                for frameN in range(1 * REFRESH_RATE): # For (n * refresh rate) present circle.
                    if frameN < 0.2 * REFRESH_RATE: # Draw this for (n * refresh rate)...
                        circle.draw()
                        main_win.flip()
                        response = stimStart # To account for no button press, given stimStart time, so RT = 0.
                    else:
                        main_win.flip() # Then present a blank screen.
            
            # If Trial is a 1, then make shapeArray value a rectangle, and count.
            else:
                number_of_rect += 1
                shape = rect
                cShape = 'rectangle'
                marker_info = ["non-target"]
                outlet.push_sample(marker_info)                
                for frameN in range(1 * REFRESH_RATE): # For (n * refresh rate) present rectangle.
                    if frameN < 0.2 * REFRESH_RATE: # Draw this for (n * refresh rate)...
                        rect.draw()
                        main_win.flip()
                        response = stimStart # To account for no button press, given stimStart time, so RT = 0.
                    else:
                        main_win.flip() # Then present a blank screen.
            
            # Data Output Setup.
            nTrial = str(numberTrial)
            numberSet = str(set)
            nShape = str(cShape)
            responseTime = str(response - stimStart)
            
            trialOutput = nTrial + ',' + numberSet + ',' + nShape + ',' + responseTime + '\n'
            file.write(trialOutput)
            
    #Fixation cross is added between each set, used to test whether blocks are coming out as sets.
    #for frameN in range(1 * REFRESH_RATE): # Display Fixation cross for (n x Refresh_Rate), so will present for n seconds.
        #fixation.draw() 
        #main_win.flip()
            

# Present the Goodbye Message.
gmessage = visual.TextStim(main_win, contrast = 0, text = goodbye, height = 0.03, font = 'Arial', pos = (0, 0))
mouse.clickReset()
clicked = False

# Move on from introduction if the mouse is clicked on box.
while clicked is False:
    if button.contains(mouse):
        clicked = True
    else:
        gmessage.draw()
        button.draw()
        main_win.flip()
    
# Save information on frame intervals.
main_win.saveFrameIntervals(fileName=None, clear=True)

# Close Data File.
file.close()

# Close the Window.
main_win.close()
