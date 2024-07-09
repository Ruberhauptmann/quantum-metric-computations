import time
from pathlib import Path
import click
import numpy as np
from quant_met import mean_field, utils
from scipy import optimize


@click.command()
@click.option("--mu", type=float, prompt="Chemical potential")
@click.option("--v", type=float, prompt="V")
@click.option("--path", 'results_path', type=click.Path(), prompt="Path for saving results")
@click.option("--nprocs", type=int, prompt="Number of processor cores available")
def minimise(mu: float, v: float, results_path: str, nprocs:int):

    results_path = Path(results_path)
    results_path.mkdir(exist_ok=True, parents=True)

    #U_range = np.linspace(start=0.01, stop=3, num=20)
    U_range = [1]

    lattice_constant = np.sqrt(3)

    all_K_points = (
        4
        * np.pi
        / (3 * lattice_constant)
        * np.array(
            [
                (np.sin(i * np.pi / 6), np.cos(i * np.pi / 6))
                for i in [1, 3, 5, 7, 9, 11]
            ]
        )
    )

    BZ_grid = utils.generate_uniform_grid(
        20, 20, all_K_points[1], all_K_points[5], origin=np.array([0, 0])
    )

    for i, U in enumerate(U_range):
        egx_h = mean_field.EGXHamiltonian(
            hopping_gr=1,
            hopping_x=0.01,
            hopping_x_gr_a=v,
            lattice_constant=lattice_constant,
            mu=mu,
            coloumb_gr=U,
            coloumb_x=U,
        )

        print(f"Calculating V = {v}, mu = {mu}, U = {U}")
        start = time.time()

        solution = optimize.differential_evolution(
            func=mean_field.free_energy_complex_gap,
            polish=True,
            tol=1e-5,
            #workers=nprocs,
            #updating="deferred",
            args=(egx_h, BZ_grid),
            bounds=[
                (-100, 100),
                (-100, 100),
                (-100, 100),
                (-100, 100),
                (-100, 100),
                (-100, 100),
            ],
        )
        egx_h.delta_orbital_basis = solution.x[0::2] + 1j * solution.x[1::2]
        egx_h.save(results_path.joinpath(f"U_{U:.2f}.hdf5"))
        print(f"Solution success: {solution.success}")
        print(f"V = {v}, mu = {mu}, U = {U}, solution: {solution.x}")
        end = time.time()
        print(f"Time taken to solve the gap equation: {end - start:0.2f} seconds")

        mean_field.superfluid_weight(h=egx_h, k_grid=BZ_grid)


if __name__ == "__main__":
    minimise()
