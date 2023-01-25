def get_parameters_xml(lattice_parameters,CrossSlot_parameters,CouetteFlow,DLD_parameters):
    '''Generates a string that can be used to generate the parameters.xml file'''
    file = f'<?xml version="1.0" ?> \n\
    \n\
    <MPI>\n\
        <cores x="{lattice_parameters.nx}" y="{lattice_parameters.ny}" z="{lattice_parameters.nz}" />\n\
    </MPI>\n\
    \n\
    <lattice>\n\
        <size NX="{lattice_parameters.Lx}" NY="{lattice_parameters.Ly}" NZ="{lattice_parameters.Lz}" />\n\
        <times start="0" end="{lattice_parameters.t_end}" info="{lattice_parameters.t_info}" sanity="{lattice_parameters.t_sanity}" />\n\
    </lattice>\n\
    \n\
    <checkpoint>\n\
        <save step="{lattice_parameters.checkpoint_saveStep}" />\n\
        <restart timeLBM="{lattice_parameters.checkpoint_timeLBM}" timeMEM="{lattice_parameters.checkpoint_timeMEM}" />\n\
    </checkpoint>\n\
    \n\
    <LBM>\n\
        <relaxation tau="{lattice_parameters.tau}" />\n\
    </LBM>\n\
    \n\
    <IBM>\n\
        <stencil range="3" />\n\
        <displacement disp="0.5" />\n\
        <start time="{lattice_parameters.timeIBMon}" />\n\
    </IBM>\n\
    \n\
    <init>\n\
        <constant active="1" density="1." velX="0." velY="0." velZ="0." />\n\
    </init>\n\
    \n\
    <forces>\n\
        <gravity x="{lattice_parameters.force_x}" y="{lattice_parameters.force_y}" z="{lattice_parameters.force_z}" tOn="1" tOff="-1" flowAlignment="{DLD_parameters.flowAlignment}"/>\n\
    </forces>\n\
    \n\
    <data>\n\
        <fluid>\n\
            <VTK active="{lattice_parameters.fluidVTK_flag}" step="{lattice_parameters.fluidVTK_step}" />\n\
            <statistics active="{lattice_parameters.fluidStats_flag}" step="{lattice_parameters.fluidStats_step}" />\n\
        </fluid>\n\
        <particles>\n\
            <VTK active="{lattice_parameters.particleVTK_flag}" step="{lattice_parameters.particleVTK_step}" />\n\
            <statistics active="{lattice_parameters.particleStats_flag}" step="{lattice_parameters.particleStats_step}" />\n\
        </particles>\n\
    </data>\n\
    \n\
    <boundaries>\n\
        <Couette active="{CouetteFlow.flag}" velBotX="{CouetteFlow.velBotX}" velBotY="{CouetteFlow.velBotY}" velTopX="{CouetteFlow.velTopX}" velTopY="{CouetteFlow.velTopY}" />\n\
        <Duct active="0" />\n\
        <Pipe active="0" />\n\
        <Constriction active="0" />\n\
        <CrossSlot active="{CrossSlot_parameters.flag}" inletWidth="{CrossSlot_parameters.inletWidth}" outletWidth="{CrossSlot_parameters.outletWidth}" inletVelocity="{CrossSlot_parameters.vel_in}" asymmetry="0" ForceTriggerMagnitude = "{CrossSlot_parameters.ForceTriggerMagnitude}" TimeBegin= "{CrossSlot_parameters.ForceTriggerTimeBegin}" TimeEnd="{CrossSlot_parameters.ForceTriggerTimeEnd}"/>\n\
        <DLD active="{DLD_parameters.flag}" numPostsX="{DLD_parameters.numPostsX}" numPostsY="{DLD_parameters.numPostsY}" radius="{DLD_parameters.p_radius}" />\n\
        <DoubleCylinder active="{DLD_parameters.DoubleCylinder}" numPosts="{DLD_parameters.numPosts}" radius="{DLD_parameters.p_radius}" post1X="{DLD_parameters.post1X}" post1Y="{DLD_parameters.post1Y}" post2X="{DLD_parameters.post2X}" post2Y="{DLD_parameters.post2Y}" /> \n\
    </boundaries>\n\
    \n\
    <convergence>\n\
        <steady active="{lattice_parameters.convergence_flag}" timeIgnore="{lattice_parameters.convergence_t_ignore}" timeInterval="1000" threshold="{lattice_parameters.convergence_tolerance}" />\n\
    </convergence>'
    return file

def get_parametersMeshes_xml(mesh,nuc,numParticles):
    '''Generates a string that can be used to generate the parameters.xml file'''
    if numParticles == 0:
        file = f'<?xml version="1.0" ?>\n\
        \n\
        <init>\n\
            <autoPosition active="0" randomSeed="0" />\n\
            <overlapCheck particleParticle="0" particleObstacle="1" />\n\
            <growth active="0" relativeRadius="4" growthMass="20" numSteps="1000" infoStep="100" />\n\
            <normalisation method="0" />\n\
        </init>\n\
        \n\
        <interaction>\n\
            <particleParticle strength="0.01" range="1" />\n\
            <particleObstacle strength="0.1" range="1.5" />\n\
        </interaction>\n\
        \n\
        <mesh>\n\
            <general numParticles="0" />\n\
        </mesh>'
    if numParticles == 1:
        file = f'<?xml version="1.0" ?>\n\
        \n\
        <init>\n\
            <autoPosition active="0" randomSeed="0" />\n\
            <overlapCheck particleParticle="0" particleObstacle="1" />\n\
            <growth active="0" relativeRadius="4" growthMass="20" numSteps="1000" infoStep="100" />\n\
            <normalisation method="0" />\n\
        </init>\n\
        \n\
        <interaction>\n\
            <particleParticle strength="0.01" range="1" />\n\
            <particleObstacle strength="0.1" range="1.5" />\n\
        </interaction>\n\
        \n\
        <mesh>\n\
            <general numParticles="1" file="./MeshGenerator/sph_ico_{mesh.numFaces}.msh" radius="{mesh.radius}" />\n\
            <physics kV="{mesh.kV}" kA="{mesh.kA}" kalpha="{mesh.kalpha}" kS="{mesh.kS}" kB="{mesh.kB}" density="1.00" ShearViscosity="{mesh.shearViscosity}" DilationalViscosity="{mesh.dilationalViscosity}" kMaxwell_dilation="{mesh.kMaxwell_dilation}" kMaxwell_shear="{mesh.kMaxwell_shear}"/>\n\
        </mesh>'
    if numParticles == 2:
        file = f'<?xml version="1.0" ?>\n\
        \n\
        <init>\n\
            <autoPosition active="0" randomSeed="0" />\n\
            <overlapCheck particleParticle="0" particleObstacle="1" />\n\
            <growth active="0" relativeRadius="4" growthMass="20" numSteps="1000" infoStep="100" />\n\
            <normalisation method="0" />\n\
        </init>\n\
        \n\
        <interaction>\n\
            <particleParticle strength="0.01" range="1" />\n\
            <particleObstacle strength="0.1" range="1.5" />\n\
        </interaction>\n\
        \n\
        <mesh>\n\
            <general numParticles="1" file="./MeshGenerator/sph_ico_{mesh.numFaces}.msh" radius="{mesh.radius}" />\n\
            <physics kV="{mesh.kV}" kA="{mesh.kA}" kalpha="{mesh.kalpha}" kS="{mesh.kS}" kB="{mesh.kB}" density="1.00" ShearViscosity="{mesh.shearViscosity}" DilationalViscosity="{mesh.dilationalViscosity}" kMaxwell_dilation="{mesh.kMaxwell_dilation}" kMaxwell_shear="{mesh.kMaxwell_shear}"/>\n\
        </mesh>\n\
        \n\
        <mesh>\n\
            <general numParticles="1" file="./MeshGenerator/sph_ico_{nuc.numFaces}.msh" radius="{nuc.radius}" />\n\
            <physics kV="{nuc.kV}" kA="{nuc.kA}" kalpha="{nuc.kalpha}" kS="{nuc.kS}" kB="{nuc.kB}" density="1.00" ShearViscosity="{nuc.shearViscosity}" DilationalViscosity="{nuc.dilationalViscosity}" kMaxwell_dilation="{nuc.kMaxwell_dilation}" kMaxwell_shear="{nuc.kMaxwell_shear}"/>\n\
        </mesh>'
    return file

def get_parametersPositions_xml(mesh,nuc,numParticles):
    '''Generates a string that can be used to generate the parameters.xml file'''
    if numParticles == 0:
        file = f'<?xml version="1.0" ?> \n\
        \n\
        <particle X="0" Y="0" Z="0" angle="0" axisX="1" axisY="2" axisZ="3"/>'
    if numParticles == 1:
        file = f'<?xml version="1.0" ?> \n\
        \n\
        <particle X="{mesh.X}" Y="{mesh.Y}" Z="{mesh.Z}" angle="0" axisX="1" axisY="2" axisZ="3"/>'
    if numParticles == 2:
        file = f'<?xml version="1.0" ?> \n\
        \n\
        <particle X="{mesh.X}" Y="{mesh.Y}" Z="{mesh.Z}" angle="0" axisX="1" axisY="2" axisZ="3"/> \n\
        \n\
        <particle X="{nuc.X}" Y="{nuc.Y}" Z="{nuc.Z}" angle="0" axisX="1" axisY="2" axisZ="3"/>'
    return file




