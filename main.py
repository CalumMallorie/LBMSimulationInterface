#!/bin/python
'''
A Python script to take physical parameters and generate 
matching parameter files for BioFM simulations
'''

# import external modules
import numpy as np


# import local modules
import parameter_files
import input
    

def main():

    Lattice = input.setup_lattice()
    Geometry = input.setup_geometry(Lattice)
    Particle = input.setup_particle(Lattice,Geometry)

    

    return
     # Set the input arguments from the command line
    args = _parse_args()

    # Generate parameter files for Couette flow simulations
    if args.Couetteflow == "ON":
        couette_flow(args) 
        
    # Generate parameter files for DLD simulation
    if args.DLD == "ON":
        DLD_sim(args) 

    # Generate parameter files for DLD DoubleCylinder
    if args.DLD_DoubleCylinder == "ON":
        DLD_DoubleCylinder(args)     

    # Generate parameter files for Cross Slot simuilations
    if args.CrossSlotSim == "ON":
        CrossSlotSim(args) 

if __name__ == '__main__':
   main()  