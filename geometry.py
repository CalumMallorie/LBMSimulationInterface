import simulation_parameters
import math

class CrossSlot():
    '''
    A class to store all the parameters relating to cross-slot simulations.
    
    The class is initialised using default values, which will be entered into the
    parameter files unless otherwise specified. As the flag default value is zero, 
    simulations will not be given this geometry by default.
    '''
    
    def __init__(self):
        # Flag to switch on cross slot simulations
        self.active = False
        
        # Cross slot geometry
        self.inlet_width = None
        self.outlet_width = None
        self.height = None
        self.inlet_length = None
        self.outlet_length = None
        self.inlet_hydraulic_diameter = None
        self.outlet_hydraulic_diameter = None
        
        # Cross slot inlet velocity
        self.velocity_in = None

        # Force trigger for vortex
        self.force_trigger_magnitude = None
        self.force_trigger_time_begin = None
        self.force_trigger_time_end = None

    def set_widths_aspect_ratio(self,inlet_aspect_ratio,outlet_aspect_ratio):
        '''set inlet and outlet widths based on w/h aspect ratio'''
        self.inlet_width = round(inlet_aspect_ratio * self.height)
        self.outlet_width = round(outlet_aspect_ratio * self.height)

    def calculate_hydraulic_diameters(self):
        self.inlet_hydraulic_diameter = 2 * (self.inlet_width*self.height)/(self.inlet_width + self.height)
        self.outlet_hydraulic_diameter = 2 * (self.outlet_width*self.height)/(self.outlet_width + self.height)

    

    def set_velocity_reynolds(self,Re,viscosity):
        self.velocity_in = Re*viscosity / self.inlet_width


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
