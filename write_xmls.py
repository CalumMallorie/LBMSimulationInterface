def generate_parameter_xmls(Lattice,Mesh,nucMesh,numParticles,CrossSlot,CouetteFlow,DLD):
    '''Takes the data classes and uses get_parameters_xml to generate and write the parameter files'''
    # Generate xml strings
    parameters = parameter_files.get_parameters_xml(Lattice,CrossSlot,CouetteFlow,DLD)
    parametersMeshes = parameter_files.get_parametersMeshes_xml(Mesh,nucMesh,numParticles)
    parametersPositions = parameter_files.get_parametersPositions_xml(Mesh,nucMesh,numParticles)

    # write strings to files
    with open('parameters.xml', 'w') as f:
        f.write(parameters)
    with open('parametersMeshes.xml', 'w') as f:
        f.write(parametersMeshes)
    with open('parametersPositions.xml', 'w') as f:
        f.write(parametersPositions)
