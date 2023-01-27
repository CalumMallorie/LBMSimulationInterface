
class CrossSlot():
    '''
    A class to store all the parameters relating to cross-slot simulations.
    
    The class is initialised using default values, which will be entered into the
    parameter files unless otherwise specified. As the flag default value is zero, 
    simulations will not be given this geometry by default.
    '''
    def __init__(self,args):
        # flag to switch on cross slot simulations
        self.flag = 0
        
        # cross slot geometry
        self.inletWidth = 50; self.outletWidth = 50
        
        # cross slot inlet velocity
        self.vel_in = 0.08

        # Force trigger
        self.ForceTriggerMagnitude = args.CrossSlot_ForceTriggerMagnitude
        self.ForceTriggerTimeBegin = args.CrossSlot_ForceTriggerTimeBegin
        self.ForceTriggerTimeEnd = args.CrossSlot_ForceTriggerTimeEnd

class CouetteFlow():
    '''
    A class to store all the parameters relating to Couette flow simulations.
    
    The class is initialised using default values, which will be entered into the
    parameter files unless otherwise specified. As the flag default value is zero, 
    simulations will not be given this geometry by default.
    '''
    def __init__(self,args):
        # flag to switch on Couette flow
        self.flag = 0
        
        # wall velocities
        self.velBotX = 0; self.velBotY = 0
        self.velTopX = 0; self.velTopY = 0

class DLD():
    '''
    A class to store all the parameters relating to DLD simulations.
    
    The class is initialised using default values, which will be entered into the
    parameter files unless otherwise specified. As the flag default value is zero, 
    simulations will not be given this geometry by default.
    '''
    def __init__(self,args):
        # flag to switch on DLD
        self.flag = 0
        
        # DLD geometry
        self.numPostsX = 1; self.numPostsY = 1; self.p_radius = 10
        
        # force model flag
        self.flowAlignment = 0

        # double cylinder experiments
        self.DoubleCylinder = 0
        self.numPosts = 0
        self.post1X = 0; self.post1Y = 0; self.post2X = 0; self.post2Y = 0
