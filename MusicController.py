"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from StateModel import *
from Button import *
from Counters import *
from Log import *
from Buzzer import *
from Instrument import *
from LightStrip import *
from Displays import *


"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class MusicController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._button1 = Button(12, "white", buttonhandler=None)
        self._button2 = Button(13, "red", buttonhandler=None)
        self._button3 = Button(14, "yellow", buttonhandler=None)
        self._button4 = Button(15, "blue", buttonhandler=None)
        self._button5 = Button(11, "black", buttonhandler=None)


        self._mydisplay = LCDDisplay(sda=0, scl=1, i2cid=0)
        self._lightstrip = LightStrip(name='Neo', pin=2, numleds=16)
        self._buzzer = PassiveBuzzer(16)
        self._instrument = Organ()
        self._instrumentno = 0
 


        # self._timer = SoftwareTimer(None)
        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = StateModel(10, self, debug=True)
        
        # Up to 5 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)
        self._model.addButton(self._button5)
        

    

        # add other buttons (up to 3 more) if needed
        
        # Add any timer you have.
        # self._model.addTimer(self._timer)
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # some examples:
        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [BTN1_RELEASE], 0)

        self._model.addTransition(0, [BTN5_PRESS], 9)
        self._model.addTransition(9, [NO_EVENT], 0)

        self._model.addTransition(0, [BTN2_PRESS], 2)
        self._model.addTransition(2, [BTN2_RELEASE], 0)

        self._model.addTransition(0, [BTN3_PRESS], 3)
        self._model.addTransition(3, [BTN3_RELEASE], 0)

        self._model.addTransition(0, [BTN4_PRESS], 4)
        self._model.addTransition(4, [BTN4_RELEASE], 0)

        self._model.addTransition(1, [BTN2_PRESS], 5)
        self._model.addTransition(5, [BTN2_RELEASE], 1)

        self._model.addTransition(2, [BTN1_PRESS], 5)
        self._model.addTransition(5, [BTN1_RELEASE], 2)

        # etc.
    
    def changeInstrument(self):
        if self._instrumentno == 0:
            self._instrument = Violin()
            self._instrumentno = 1
        else:
            self._instrument = Organ()
            self._instrumentno = 0
    
    def testDisplay(self):
        self._mydisplay.showText("start the Music")
        self._mydisplay.addShape(0,[ 0x00,0x11,0x0A,0x04,0x1F,0x04,0x0A,0x11])
        self._mydisplay.showText(f"   {chr(0)}  {chr(0)}", row=1, col=0)
    

    
    def testLightstrip(self):
        # Turn on the lights in order 
        for lightno in range(0,16):
            # Turn the specific light on
            self._lightstrip.setPixel(lightno, RED)
            time.sleep(0.25)
            self._lightstrip.setPixel(lightno, BLUE)
            time.sleep(0.25)
            




    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
        # Now if you want to do different things for each state you can do it:
            # State 0 do/actions
            
            # State1 do/actions
            # You can check your sensors here and perform transitions manually if needed
            # For example, if you want to go from state 1 to state 2 when the motion sensor
            # is tripped you can do something like this
            # if self.motionsensor.tripped():
            # 	gotoState(2)
        pass

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        Log.d(f'State {state} entered')
        if state == 0:
            # entry actions for state 0
            pass
        
        elif state == 1:
            # entry actions for state 1
            self._buzzer.play(self._instrument.getNote(0))
            self._lightstrip.setPixel(1, RED)
            self._mydisplay.showText("DO")
            self._mydisplay.addShape(0,[ 0x18, 0x14, 0x12, 0x11, 0x11, 0x12, 0x14, 0x18])
            self._mydisplay.showText(f"   {chr(0)}  {chr(0)}", row=1, col=0)

        elif state == 2:
            # entry actions for state 2
            self._buzzer.play(self._instrument.getNote(1))
            self._lightstrip.setPixel(2, BLUE)
            self._mydisplay.showText("RE")
            self._mydisplay.addShape(0,[ 0x1C,0x12,0x11,0x12,0x14,0x18,0x14,0x13])
            self._mydisplay.showText(f"   {chr(0)}  {chr(0)}", row=1, col=0)

        elif state == 3:
            # entry actions for state 3
            self._buzzer.play(self._instrument.getNote(2))
            self._lightstrip.setPixel(3, YELLOW)
            self._mydisplay.showText("MI")
            self._mydisplay.addShape(0,[ 0x11,0x1B,0x1B,0x15,0x11,0x11,0x11,0x11])
            self._mydisplay.showText(f"   {chr(0)}  {chr(0)}", row=1, col=0)

        elif state == 4:
            # entry actions for state 4
            self._buzzer.play(self._instrument.getNote(3))
            self._lightstrip.setPixel(4, WHITE)
            self._mydisplay.showText("FA")
            self._mydisplay.addShape(0,[ 0x1F,0x10,0x10,0x1E,0x10,0x10,0x10,0x10])
            self._mydisplay.showText(f"   {chr(0)}  {chr(0)}", row=1, col=0)

        elif state == 5:
            # entry actions for state 5
            self._buzzer.play(self._instrument.getNote(4))
            self._lightstrip.setPixel(5, RED)
        
        elif state == 9:
            self.changeInstrument()    

            
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state, event):
        Log.d(f'State {state} exited')
        if state in range(1,9):
            # exit actions for state 0
            self._buzzer.stop()
        # etc.
    

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
# if __name__ == '__main__':
# MyControllerTemplate().run()