# parameter_updates.py

import math
from typing import Dict, Tuple, Any

class ParameterUpdates:
    """
    Class to manage updates to simulation parameter XML files.

    This class is used to specify changes to the default simulation parameters defined
    in template XML files. It maintains a dictionary (`parameter_updates`) that contains
    only the parameters that need to be changed relative to the templates.

    If no methods are called to populate `parameter_updates`, then when
    `SimulationSetup.prepare_simulation()` is called, the generated parameter files
    will be exact copies of the template files. If only a subset of parameters are
    updated, only those changes will be applied, and the rest will remain as in the
    template.

    **Usage:**

    - Create an instance of `ParameterUpdates`.
    - Use the provided methods to specify parameter changes.
    - Pass the `ParameterUpdates` instance to `SimulationSetup` to apply the changes.

    """

    def __init__(self, parameter_updates: Dict[str, Dict[Tuple[str, ...], Any]] = None):
        if parameter_updates is None:
            self.parameter_updates = {
                "parameters.xml": {},
                "parametersMeshes.xml": {},
                "parametersPositions.xml": {},
            }
        else:
            self.parameter_updates = parameter_updates

    def MPI(self, mpi: Tuple[int, int, int]) -> "ParameterUpdates":
        """
        Set the number of MPI cores in each direction.

        Args:
            mpi (Tuple[int, int, int]): Number of cores in x, y, z directions.

        Returns:
            ParameterUpdates: Self for method chaining.
        """
        self.parameter_updates["parameters.xml"].update({
            ('MPI', 'cores', 'x'): str(mpi[0]),
            ('MPI', 'cores', 'y'): str(mpi[1]),
            ('MPI', 'cores', 'z'): str(mpi[2]),
        })
        return self

    def lattice(self, NX: int, NY: int, NZ: int) -> "ParameterUpdates":
        """
        Set the lattice size.

        Args:
            NX (int): Lattice size in x-direction.
            NY (int): Lattice size in y-direction.
            NZ (int): Lattice size in z-direction.

        Returns:
            ParameterUpdates: Self for method chaining.
        """
        self.parameter_updates["parameters.xml"].update({
            ('lattice', 'size', 'NX'): str(NX),
            ('lattice', 'size', 'NY'): str(NY),
            ('lattice', 'size', 'NZ'): str(NZ),
        })
        return self

    def sim_time(self, t_end: int) -> "ParameterUpdates":
        """
        Set the simulation end time.

        Args:
            t_end (int): Simulation end time in lattice units.

        Returns:
            ParameterUpdates: Self for method chaining.
        """
        self.parameter_updates["parameters.xml"].update({
            ('lattice', 'times', 'end'): str(t_end),
        })
        return self

    def info_time(self, t_info):
        self.parameter_updates["parameters.xml"].update({
            ('lattice', 'times', 'info'): str(t_info),
        })

    def vtk_save(self, fluid_step=-1, particle_step=-1):
        self.parameter_updates["parameters.xml"].update({
            ('data', 'fluid', 'VTK', 'active'): str(1) if fluid_step > 0 else str(0),
            ('data', 'fluid', 'VTK', 'step'): str(fluid_step),
            ('data', 'particles', 'VTK', 'active'): str(1) if particle_step > 0 else str(0),
            ('data', 'particles', 'VTK', 'step'): str(particle_step),
        })

    def checkpoint(self, step, restartLBM, restartMEM):
        self.parameter_updates["parameters.xml"].update({
                    ('checkpoint','save', 'step'): str(step),
                    ('checkpoint','restart','timeLBM'): str(restartLBM),
                    ('checkpoint','restart','timeMEM'): str(restartMEM),
                    })

    def relaxation(self, tau):
        self.parameter_updates["parameters.xml"].update({
            ('LBM','relaxation', 'tau'): str(tau),
        })

    def MRT(self, tauBulk, magic):
        self.parameter_updates["parameters.xml"].update({
            ('LBM', 'MRT', 'active'): "1",
            ('LBM', 'MRT', 'tauBulk'): str(tauBulk),
            ('LBM', 'MRT', 'Lambda'): str(magic),
        })

    def cross_slot_geometry(self, inlet_width, outlet_width, stenosis_width, stenosis_length):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'CrossSlot', 'active'): "1",
            ('boundaries', 'CrossSlot', 'inletWidth'): str(inlet_width),
            ('boundaries', 'CrossSlot', 'outletWidth'): str(outlet_width),
            ('boundaries', 'CrossSlot', 'stenosisWidth'): str(stenosis_width),
            ('boundaries', 'CrossSlot', 'stenosisLength'): str(stenosis_length),
        })
    
    def duct_geometry(self):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'Duct', 'active'): "1",
        })

    def couette(self, velocity):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'Couette', 'active'): "1",
            ('boundaries', 'Couette', 'velocity'): str(velocity),
        })

    def forcing(self, force):
        self.parameter_updates["parameters.xml"].update({
            ('forces', 'gravity', 'x'): str(force[0]),
            ('forces', 'gravity', 'y'): str(force[1]),
            ('forces', 'gravity', 'z'): str(force[2]),
        })

    def cross_slot_velocity(self, inlet_velocity):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'CrossSlot', 'inletVelocity'): str(inlet_velocity),
        })

    def cross_slot_vortex(self, vortex_force_mag, vortex_time_begin, vortex_time_end):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'CrossSlot', 'ForceTriggerMagnitude'): str(vortex_force_mag),
            ('boundaries', 'CrossSlot', 'TimeBegin'): str(vortex_time_begin),
            ('boundaries', 'CrossSlot', 'TimeEnd'): str(vortex_time_end),
        })

    def convergence(self, time_ignore, convergence):
        self.parameter_updates["parameters.xml"].update({
            ('convergence', 'steady', 'active'): "1",
            ('convergence', 'steady', 'timeIgnore'): str(time_ignore),
            ('convergence', 'steady', 'timeInterval'): "1000",
            ('convergence', 'steady', 'threshold'): str(convergence),
        })

    def no_convergence(self):
        self.parameter_updates["parameters.xml"].update({
            ('convergence', 'steady', 'active'): "0",
        })

    def mesh_viscosity_contrast(self, viscosity_ratio):
        self.parameter_updates["parametersMeshes.xml"].update({
            ('viscosityContrast', 'indexField', 'active'): "1",
            ('viscosityContrast', 'viscosity', 'ratio'): str(viscosity_ratio),
        })

    def mesh(self, radius=0, kV=0, kA=0, kalpha=0, kS=0, kB=0, density=0, shearViscosity=0, dilationalViscosity=0, kmaxwell_dilation=0, kmaxwell_shear=0):
        self.parameter_updates["parametersMeshes.xml"].update({
            ('mesh', 'general', 'radius'): str(radius),
            ('mesh', 'general', 'file'): f"./MeshGenerator/sph_ico_{20*math.ceil(radius*1.2)**2}.msh",
            ('mesh', 'physics', 'kV'): str(kV),
            ('mesh', 'physics', 'kA'): str(kA),
            ('mesh', 'physics', 'kalpha'): str(kalpha),
            ('mesh', 'physics', 'kS'): str(kS),
            ('mesh', 'physics', 'kB'): str(kB),
            ('mesh', 'physics', 'density'): str(density),
            ('mesh', 'physics', 'ShearViscosity'): str(shearViscosity),
            ('mesh', 'physics', 'DilationalViscosity'): str(dilationalViscosity),
            ('mesh', 'physics', 'kMaxwell_dilation'): str(kmaxwell_dilation),
            ('mesh', 'physics', 'kMaxwell_shear'): str(kmaxwell_shear),
        })

    def mesh_positions(self, position, angle="0", axisX="1", axisY="1", axisZ="1"):
        self.parameter_updates["parametersPositions.xml"].update({
            ('particle', 'X'): str(position[0]),
            ('particle', 'Y'): str(position[1]),
            ('particle', 'Z'): str(position[2]),
            ('particle', 'angle'): str(angle),
            ('particle', 'axisX'): str(axisX),
            ('particle', 'axisY'): str(axisY),
            ('particle', 'axisZ'): str(axisZ),
        })

    def get_parameter_updates(self) -> Dict[str, Dict[Tuple[str, ...], Any]]:
        """
        Get the dictionary of parameter updates.

        Returns:
            Dict[str, Dict[Tuple[str, ...], Any]]: Parameter updates.
        """
        return self.parameter_updates