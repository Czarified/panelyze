import numpy as np

from panelyze.analysis.geometry import CircularCutout, PanelGeometry
from panelyze.analysis.kernels import BEMKernels
from panelyze.analysis.material import OrthotropicMaterial
from panelyze.analysis.solver import BEMSolver


def verify_isotropic_plate_imperial():
    # 1. Setup Material (Imperial: psi)
    # Al 6061-T6 approx: E = 10 Msi, nu = 0.33
    E, nu = 10.0e6, 0.33
    G = E / (2 * (1 + nu))
    # Pseudo-isotropic perturbation
    mat = OrthotropicMaterial(e1=E, e2=E * 1.001, nu12=nu, g12=G)

    # 2. Setup Geometry (Imperial: inches)
    W, H = 10.0, 10.0
    radius = 0.5
    geom = PanelGeometry(W, H)
    geom.add_cutout(CircularCutout(W / 2, H / 2, radius))

    # 3. Discretize
    n_side = 20
    elements = geom.discretize(num_elements_per_side=n_side, num_elements_cutout=80)

    # 4. Assemble
    solver = BEMSolver(BEMKernels(mat), elements)
    solver.assemble()

    # 5. Boundary Conditions
    bc_type = np.zeros(2 * len(elements), dtype=int)
    bc_value = np.zeros(2 * len(elements))

    # Tension sigma = 1000 psi on sides
    sigma = 1000.0
    for i, el in enumerate(elements):
        if np.isclose(el.center[0], 0.0):  # Left
            bc_value[2 * i] = -sigma
        if np.isclose(el.center[0], W):  # Right
            bc_value[2 * i] = sigma

    # Corner Constraints
    bc_type[0:2] = 1  # u=0, v=0 at (0,0)
    bc_value[0:2] = 0.0

    k_br = n_side - 1  # (W,0)
    bc_type[2 * k_br + 1] = 1  # v=0
    bc_value[2 * k_br + 1] = 0.0

    u, t = solver.solve(bc_type, bc_value)

    # 6. Evaluate stress at hole pole (r=0.51 in, i.e., 1.02R)
    eval_pts = np.array([[W / 2, H / 2 + 0.51]])
    stresses = solver.compute_stress(eval_pts, u, t)

    scf = stresses[0, 0] / sigma
    print(f"Stress sigma_xx at hole pole (r=0.51): {stresses[0, 0]:.4f} psi")
    print(f"Calculated SCF: {scf:.4f}")

    return scf


if __name__ == "__main__":
    verify_isotropic_plate_imperial()
