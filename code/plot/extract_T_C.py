import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats

LINEAR_RANGES = {
    "-2.0": [12, 18],
    "-2.5": [8, 12.5],
    "-3.0": [6, 8],
    "-3.5": [5, 9],
    "-4.0": [4.5, 5.5],
    "-5.0": [3.5, 4.5],
    "-6.0": [3.5, 4],
}


if __name__ == "__main__":
    U_list = sys.argv[1:-2]

    plot_path = Path(sys.argv[-1])
    plot_path.mkdir(exist_ok=True, parents=True)
    csv_path = Path(sys.argv[-2]).parent

    critical_temperatures = pd.DataFrame(
        columns=["U", "T_C", "beta_C"], index=range(len(U_list))
    )

    fig, ax = plt.subplots()

    for index, U_dir in enumerate(U_list):
        U = U_dir.split("/")[-1].split("_")[-1].strip(".csv")
        U_plot_path = plot_path.joinpath(f"U_{U}")
        U_plot_path.mkdir(exist_ok=True, parents=True)

        results = pd.read_csv(U_dir)

        linear_T_interval = results[
            (results["beta"] > LINEAR_RANGES[U][0])
            & (results["beta"] < LINEAR_RANGES[U][1])
        ]
        linear_reg = stats.linregress(
            linear_T_interval["temperature"],
            np.abs(linear_T_interval["order_parameter"]) ** 2,
        )

        ax.plot(
            linear_T_interval.loc[:, "temperature"],
            np.abs(linear_T_interval.loc[:, "order_parameter"]) ** 2,
            "x--",
        )
        ax.plot(
            linear_T_interval.loc[:, "temperature"],
            linear_reg.intercept
            + linear_reg.slope * linear_T_interval.loc[:, "temperature"],
            "r-",
        )
        ax.set_xlabel("$T$")
        ax.set_ylabel("$\\vert OP \\vert^2$")

        fig.savefig(U_plot_path.joinpath("temperature_OP_fit.pdf"))
        ax.cla()

        critical_temp = -linear_reg.intercept / linear_reg.slope

        # critical_temperatures["U"] = U
        critical_temperatures.loc[index] = [U, critical_temp, 1 / critical_temp]

    critical_temperatures.to_csv(csv_path.joinpath("T_C_vs_U.csv"), index=False)
