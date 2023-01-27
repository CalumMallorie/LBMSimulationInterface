import simulation_parameters
import geometry

def simulation_setup():

    # input parameters
    height = 50
    inlet_aspect_ratio = 1.2
    outlet_aspect_ratio = 1.1
    inlet_length_hydraulic_diameters = 4
    outlet_length_hydraulic_diameters = 4
    Re = 150
    tau = 1

    # Initilaise CrossSlot class:
    CrossSlot = geometry.CrossSlot()

    # Set widths based on height and aspect ratios
    CrossSlot.active = True
    CrossSlot.height = height
    print(CrossSlot.height)
    CrossSlot.set_widths_aspect_ratio(inlet_aspect_ratio,outlet_aspect_ratio)

    # Set inlet and outlet lengths based on number of hydraulic diameters
    CrossSlot.calculate_hydraulic_diameters()
    CrossSlot.inlet_length = inlet_length_hydraulic_diameters * CrossSlot.inlet_hydraulic_diameter 
    CrossSlot.outlet_length = outlet_length_hydraulic_diameters * CrossSlot.outlet_hydraulic_diameter 

    # create lattice
    Lattice = CrossSlot.set_lattice()
    Lattice.tau = tau

    # Set inlet velocity
    CrossSlot.set_velocity_reynolds(Re,Lattice.viscosity())
    
# # Set outer mesh properties
#     if args.nuc_confinement == 0:
#         numParticles = 1
#     shear_rate = 2*velocity/height
#     outer_mesh.radius = 0.5*args.cell_confinement*height # radius set by confinement
#     outer_mesh.numFaces = 20*math.ceil(outer_mesh.radius)**2 # keep the node-to-node distance close to 1
#     outer_mesh.X = 2*outer_mesh.radius # particle is 1 diameter into the inlet
#     outer_mesh.Y = lattice_parameters.Ly/2 + CrossSlot_parameters.inletWidth*args.CrossSlot_ydeviation # particle is offset by percent deviation from centreline
#     outer_mesh.Z = lattice_parameters.Lz/2
#     outer_mesh.kS = LBM_viscosity(args)*shear_rate*outer_mesh.radius/args.outer_Ca # set kappa_s by Ca=visc*gammadot*radius/kS
#     outer_mesh.kB = outer_mesh.kS*outer_mesh.radius**2/400 # set kB based on red blood cell relation
#     outer_mesh.kalpha = 2*outer_mesh.kS # using kB = 2*kS for now
#     outer_mesh.shearViscosity = args.outer_Bq_s*outer_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)
#     outer_mesh.dilationalViscosity = args.outer_Bq_d*outer_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)

#     # Set innter mesh properties 
#     if args.nuc_confinement != 0:
#         numParticles = 2
#     nuc_mesh = Mesh(args)
#     nuc_mesh.radius = args.nuc_confinement*outer_mesh.radius # radius set by confinement
#     nuc_mesh.numFaces = 20*math.ceil(nuc_mesh.radius)**2 # keep the node-to-node distance close to 1
#     nuc_mesh.X = outer_mesh.X
#     nuc_mesh.Y = outer_mesh.Y
#     nuc_mesh.Z = outer_mesh.Z
#     nuc_mesh.kS = LBM_viscosity(args)*shear_rate*nuc_mesh.radius/args.nuc_Ca # set kappa_s by Ca=visc*gammadot*radius/kS
#     nuc_mesh.kB = nuc_mesh.kS*nuc_mesh.radius**2/400 # set kB based on red blood cell relation
#     nuc_mesh.kalpha = 2*nuc_mesh.kS # using kB = 2*kS for now
#     nuc_mesh.shearViscosity = args.nuc_Bq_s*nuc_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)
#     nuc_mesh.dilationalViscosity = args.nuc_Bq_d*nuc_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)






def _parse_args():
    '''Takes input arguments from the command line'''
    parser = argparse.ArgumentParser()
    # Setup
    parser.add_argument("--Couetteflow", type=str)
    parser.add_argument("--DLD", type=str)
    parser.add_argument("--CrossSlot_GridIndependence", type=str)
    parser.add_argument("--CrossSlotSim", type=str)
    parser.add_argument("--DLD_DoubleCylinder", type=str)

    # General
    parser.add_argument("--numCores", nargs="+", type=int, default=[1,1,1])
    parser.add_argument("--tau", type=float)
    parser.add_argument("--convergence_tolerance", type=float)
    parser.add_argument("--convergence_t_ignore", type=int)
    parser.add_argument("--t_end", type=int)
    parser.add_argument("--timeIBMon", type=int)
    parser.add_argument("--Re", type = int)

    # Viscoelastic model numerical parameters
    parser.add_argument("--k_s", type=float)
    parser.add_argument("--k_d", type=float)

    # Outer mesh
    parser.add_argument("--cell_confinement", type=float)
    parser.add_argument("--outer_Bq_s", type=float)
    parser.add_argument("--outer_Bq_d", type=float)
    parser.add_argument("--outer_Ca", type=float)

    # Nucleus mesh
    parser.add_argument("--nuc_confinement", type=float)
    parser.add_argument("--nuc_Bq_s", type=float)
    parser.add_argument("--nuc_Bq_d", type=float)
    parser.add_argument("--nuc_Ca", type=float)

    # Data
    parser.add_argument("--fluidVTK_step", type=int)
    parser.add_argument("--particleVTK_step", type=int)

    # DLD arguments
    parser.add_argument("--DLD_len", type=int)
    parser.add_argument("--DLD_forceMag", type=float)
    parser.add_argument("--DLD_forceDir", type=float)
    parser.add_argument("--DLD_normGapSize", type=float)
    parser.add_argument("--DLD_flowAlignment", type=int)
    parser.add_argument("--DLD_postRadius", type=int)
    parser.add_argument("--post1_coords", nargs="+", type=int)
    parser.add_argument("--post2_coords", nargs="+", type=int)
    parser.add_argument("--DLD_aspectratio", type=float)

    # Couette flow arguments
    parser.add_argument("--CouetteFlow_h", type=int)

    # Cross slot flow arguments
    parser.add_argument("--CrossSlot_size", type=int)
    parser.add_argument("--CrossSlot_inletAspectRatio", type=float)
    parser.add_argument("--CrossSlot_outletAspectRatio", type=float)
    parser.add_argument("--CrossSlot_inletLength", type=float)
    parser.add_argument("--CrossSlot_outletLength", type=float)
    parser.add_argument("--CrossSlot_ydeviation", type=float)
    parser.add_argument("--CrossSlot_ForceTriggerMagnitude", type=float)
    parser.add_argument("--CrossSlot_ForceTriggerTimeBegin", type=int)
    parser.add_argument("--CrossSlot_ForceTriggerTimeEnd", type=int)

    
    args = parser.parse_args()
    return args

    
def couette_flow(args):
    '''Function used to generate Couette flow simulations'''
    # Initalise classes:
    lattice_parameters, CrossSlot_parameters, particle_mesh, CouetteFlow_parameters, DLD_parameters = initialise_classes(args)
    

    # Set couette flow to ON:
    CouetteFlow_parameters.flag = 1

    # no convergence:
    lattice_parameters.convergence_flag = 0

    # Set particle simulation details:
    numParticles = 1 # Always one particle for Couette
    particle_mesh.radius = 0.5*args.confinement*float(args.CouetteFlow_h) # radius set by confinement
    particle_mesh.numFaces = 20*math.ceil(particle_mesh.radius)**2 # keep the node-to-node distance close to 1
    particle_mesh.X = particle_mesh.Y = particle_mesh.Z = 0.5*args.CouetteFlow_h # particle in centre of box

    # Set Couette geometry, cubic:
    lattice_parameters.Lx = lattice_parameters.Ly = lattice_parameters.Lz = args.CouetteFlow_h

    # Set velocity based on Re, assuming opposing x-velocities at top and bottom walls:
    velocity = args.Re*LBM_viscosity(args)/args.CouetteFlow_h
    CouetteFlow_parameters.velTopX = 0.5*velocity
    CouetteFlow_parameters.velBotX = -0.5*velocity

    # Set particle properties based on Ca and Bq values:
    shear_rate = 2*velocity/args.CouetteFlow_h 
    particle_mesh.kS = LBM_viscosity(args)*shear_rate*particle_mesh.radius/args.Ca # set kappa_s by Ca=visc*gammadot*radius/kS
    particle_mesh.kB = particle_mesh.kS*particle_mesh.radius**2/400 # set kB based on red blood cell relation
    particle_mesh.kalpha = 2*particle_mesh.kS # using kB = 2*kS for now
    particle_mesh.shearViscosity = args.Bq_s*particle_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)
    particle_mesh.dilationalViscosity = args.Bq_d*particle_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)
    if args.Bq_d > 0 or args.Bq_s>0: 
        particle_mesh.kMaxwell = 1 # need to make sure this is sufficiently high so as to be independent
    
    # generate the parameter files:
    generate_parameter_xmls(lattice_parameters,particle_mesh,numParticles,CrossSlot_parameters,CouetteFlow_parameters,DLD_parameters)

def DLD_sim(args):
    # Initalise classes:
    lattice_parameters, CrossSlot_parameters, outer_mesh, CouetteFlow_parameters, DLD_parameters = initialise_classes(args)
    nuc_mesh = Mesh(args)

    # Set DLD flow to ON:
    DLD_parameters.flag = 1

    # DLD has no particles:
    numParticles = 0

    # Set simulation bounds:
    lattice_parameters.Lx = lattice_parameters.Ly = args.DLD_len 
    lattice_parameters.Lz = 1

    # Set convergence tolerance:
    lattice_parameters.convergence_tolerance = args.convergence_tolerance

    # Set geometry:
    DLD_parameters.p_radius = 0.5 * args.DLD_len * (1-args.DLD_normGapSize)
    DLD_parameters.numPostsX = DLD_parameters.numPostsY = 1

    # Set forcing:
    lattice_parameters.force_x =  args.DLD_forceMag*np.cos((np.pi/180)*args.DLD_forceDir)
    lattice_parameters.force_y = -args.DLD_forceMag*np.sin((np.pi/180)*args.DLD_forceDir)

    # Set force alignment model:
    DLD_parameters.flowAlignment = args.DLD_flowAlignment

    generate_parameter_xmls(lattice_parameters,outer_mesh,nuc_mesh,numParticles,CrossSlot_parameters,CouetteFlow_parameters,DLD_parameters)

def CrossSlot_GridIndependence(args):
    # Initalise classes:
    lattice_parameters, CrossSlot_parameters, particle_mesh, CouetteFlow_parameters, DLD_parameters = initialise_classes(args)

    # Set CrossSlot flow to ON:
    CrossSlot_parameters.flag = 1

    # Set CrossSlot geometry based on lattice side length:
    lattice_parameters.Lx = lattice_parameters.Ly = args.CrossSlot_size
    CrossSlot_parameters.inletWidth = CrossSlot_parameters.outletWidth = math.floor(args.CrossSlot_size / 6) # ebsure the inlets and outlets have at least 4*D_hydraulic 
    CrossSlot_parameters.Lz = math.floor(CrossSlot_parameters.inletWidth / CrossSlot_parameters.CrossSlot_aspectRatio)
    height = CrossSlot_parameters.Lz - 2
    inlet_hydraulic_diameter = 2 * (CrossSlot_parameters.inletWidth*height)/(CrossSlot_parameters.inletWidth + height)
    inlet_length = (lattice_parameters.Lx - CrossSlot_parameters.outletWidth)/2
    print('The inlet legth is ', inlet_length/inlet_hydraulic_diameter, ' times the hydraulic diameter')



    # Set particle size and position:
    numParticles = 1 
    particle_mesh.radius = 0.5*args.confinement*float(args.CouetteFlow_h) # radius set by confinement
    particle_mesh.numFaces = 20*math.ceil(particle_mesh.radius)**2 # keep the node-to-node distance close to 1
    particle_mesh.X = 2*particle_mesh.radius # particle is 1 diameter into the inlet
    particle_mesh.Y = lattice_parameters.Ly/2 + CrossSlot_parameters.inletWidth*args.CrossSlot_ydeviation # particle is offset by 2% from centreline
    particle_mesh.Z = lattice_parameters.Lz/2

    # Set membrane physics:
    # Set particle properties based on Ca and Bq values:
    shear_rate = 2*velocity/args.CouetteFlow_h 
    particle_mesh.kS = LBM_viscosity(args)*shear_rate*particle_mesh.radius/args.Ca # set kappa_s by Ca=visc*gammadot*radius/kS
    particle_mesh.kB = particle_mesh.kS*particle_mesh.radius**2/400 # set kB based on red blood cell relation
    particle_mesh.kalpha = 2*particle_mesh.kS # using kB = 2*kS for now
    particle_mesh.shearViscosity = args.Bq_s*particle_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)
    particle_mesh.dilationalViscosity = args.Bq_d*particle_mesh.radius*LBM_viscosity(args)# membrane viscosities set by Bq=memvisc/(radius*fluidvisc)
    if args.Bq_d > 0 or args.Bq_s>0: 
        particle_mesh.kMaxwell = 1 # need to make sure this is sufficiently high so as to be independent

    # Generate xmls:
    generate_parameter_xmls(lattice_parameters,particle_mesh,nuc_mesh,numParticles,CrossSlot_parameters,CouetteFlow_parameters,DLD_parameters)


def DLD_DoubleCylinder(args):
    lattice_parameters, CrossSlot_parameters, outer_mesh, CouetteFlow_parameters, DLD_parameters = initialise_classes(args)
    nuc_mesh = Mesh(args)
    numParticles = 1

    DLD_parameters.DoubleCylinder = 1

    # Set simulation bounds:
    lattice_parameters.Lx = 2*args.DLD_len 
    lattice_parameters.Ly = args.DLD_len * args.DLD_aspectratio
    lattice_parameters.Lz = 1

    # Set convergence tolerance:
    lattice_parameters.convergence_tolerance = args.convergence_tolerance

    # Set geometry:
    DLD_parameters.p_radius = DLD_parameters.p_radius = 0.5 * args.DLD_len * (1-args.DLD_normGapSize)
    DLD_parameters.numPosts = 2
    DLD_parameters.post1X = lattice_parameters.Lx/4
    DLD_parameters.post1Y = lattice_parameters.Ly/2
    DLD_parameters.post2X = 3*lattice_parameters.Lx/4
    DLD_parameters.post2Y = lattice_parameters.Ly/2

    # Set forcing:
    lattice_parameters.force_x =  args.DLD_forceMag*np.cos((np.pi/180)*args.DLD_forceDir)
    lattice_parameters.force_y = -args.DLD_forceMag*np.sin((np.pi/180)*args.DLD_forceDir)

    # Set force alignment model:
    DLD_parameters.flowAlignment = args.DLD_flowAlignment

    generate_parameter_xmls(lattice_parameters,outer_mesh,nuc_mesh,numParticles,CrossSlot_parameters,CouetteFlow_parameters,DLD_parameters)