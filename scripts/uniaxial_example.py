import matplotlib.pyplot as plt
import numpy as np

from panelyze.analysis import plot_results
from panelyze.analysis.geometry import CircularCutout, PanelGeometry
from panelyze.analysis.kernels import BEMKernels
from panelyze.analysis.material import OrthotropicMaterial
from panelyze.analysis.solver import BEMSolver

E, nu = 10.5e6, 0.33
G = E / (2 * (1 + nu))
thickness = 0.080
mat = OrthotropicMaterial(e1=E, e2=E * 1.001, nu12=nu, g12=G, thickness=thickness)

W, H = 30.0, 15.0
geom = PanelGeometry(W, H)
geom.add_cutout(CircularCutout(W / 2, H / 2, 1.5))

n_side = 40
elements = geom.discretize(num_elements_per_side=n_side, num_elements_cutout=120)

solver = BEMSolver(BEMKernels(mat), elements)
solver.assemble()

bc_type = np.zeros(2 * len(elements), dtype=int)
bc_value = np.zeros(2 * len(elements))

q_applied = 500
for i, el in enumerate(elements):
    if np.isclose(el.center[0], 0.0):
        bc_value[2 * i] = -q_applied
    if np.isclose(el.center[0], W):
        bc_value[2 * i] = q_applied

bc_type[0:2] = 1
bc_value[0:2] = 0.0
bc_type[2 * (n_side - 1) + 1] = 1
bc_value[2 * (n_side - 1) + 1] = 0.0

u, t = solver.solve(bc_type, bc_value)

eval_pts = np.array([[W / 2, H / 2 + 1.51]])
stress = solver.compute_stress(eval_pts, u, t)

# Expect SCF ~2.94 based on stress
q_sigma = q_applied / thickness
scf = stress[0, 0] / q_sigma
print(f"Far-Field Stress: {q_sigma:.0f} [psi]")
print(f"Local Stress: {stress[0, 0]:.0f} [psi]")
print(f"K_t: {scf:.2f}")

# After solving the system
fig = plot_results(
    solver,
    u,
    t,
    deform_scale=150,
    title="Circular Cutout under X-Tension",
    stress_type="xx",
)
plt.show()
