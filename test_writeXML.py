import xml.etree.ElementTree as ET

# Define simulation parameters
nx = 128
ny = 128
nt = 100
dt = 0.01
tau = 0.5
omega = 1.0
youngs_modulus = 1.0
poissons_ratio = 0.3

# Create XML tree structure
root = ET.Element("simulation")

# Fluid simulation
fluid_simulation = ET.SubElement(root, "fluid_simulation")
grid = ET.SubElement(fluid_simulation, "grid", {"nx": str(nx), "ny": str(ny), "nt": str(nt), "dt": str(dt)})
params = ET.SubElement(fluid_simulation, "parameters")
ET.SubElement(params, "tau").text = str(tau)
ET.SubElement(params, "omega").text = str(omega)

# Hyperelastic capsule simulation
capsule_simulation = ET.SubElement(root, "capsule_simulation")
params = ET.SubElement(capsule_simulation, "parameters")
ET.SubElement(params, "youngs_modulus").text = str(youngs_modulus)
ET.SubElement(params, "poissons_ratio").text = str(poissons_ratio)

# Immersed boundary method
immersed_boundary = ET.SubElement(root, "immersed_boundary")
ET.SubElement(immersed_boundary, "coupling_type").text = "force_coupling"

# Write XML tree to file
tree = ET.ElementTree(root)
tree.write("simulation.xml")