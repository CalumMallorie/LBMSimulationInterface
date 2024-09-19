# lbm_utils.py

"""
This module provides utility functions specific to lattice-Boltzmann 
simulations, such as calculating the viscosity from the relaxation time,
or checking that the grid Reynolds number is sufficiently low. It is 
expected that the user will add their own functions to this module.
"""


import math

def calculate_viscosity(tau: float) -> float:
    """
    Calculate the lattice viscosity based on the relaxation time tau.

    Formula:
        viscosity = (1/3) * (tau - 0.5)

    Args:
        tau (float): Relaxation time.

    Returns:
        float: Calculated viscosity.
    """
    return (1 / 3) * (tau - 0.5)

def check_grid_reynolds_number(tau: float, velocity: float) -> bool:
    """
    Check whether the grid Reynolds number is sufficiently small.

    According to equation 7.18 in the LBM book:
        tau >= 0.5 + 0.125 * velocity

    Args:
        tau (float): Relaxation time.
        velocity (float): Lattice velocity.

    Returns:
        bool: True if the grid Reynolds number is acceptable, False otherwise.
    """
    test_parameter = 0.5 + 0.125 * velocity
    return tau >= test_parameter

def biofm_num_faces(radius: float) -> int:
    """
    Calculates the number of faces which a mesh should have for a given
    radius to ensure that the approximate average side length of a face is 
    close to 1. 
    """

    number_of_faces = 20*math.ceil(radius)**2

    return number_of_faces