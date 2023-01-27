# Set up cross-slot flow simulation

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