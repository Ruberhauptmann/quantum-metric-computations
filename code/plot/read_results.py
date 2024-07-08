import glob
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


def clean_results():
    U_list = sys.argv[1:-1]

    csv_path = Path(sys.argv[-1])
    csv_path.mkdir(exist_ok=True, parents=True)

    result_list = {}

    for U_dir in U_list:
        U = U_dir.split("/")[-1].split("_")[-1]
        beta_file_list = glob.glob(f"{U_dir}/beta_*")
        beta_list = []
        order_parameter_list = []

        for beta_file in beta_file_list:
            beta = float(beta_file.split("/")[-1].split("_")[1].strip(".zip"))
            beta_list.append(beta)

            with zipfile.ZipFile(f"{beta_file}", "r") as beta_zip:
                with io.TextIOWrapper(beta_zip.open(f"beta_{beta}/dmft.result")) as f:
                    ifile = iter(f.readlines())
                    for line in ifile:
                        if line.startswith("# orbital    2    1"):
                            order_parameter_list.append(float(next(ifile, "").strip()))

        results = pd.DataFrame(
            {
                "beta": beta_list,
                "temperature": 1 / np.array(beta_list),
                "order_parameter": order_parameter_list,
            }
        )
        results.sort_values(by=["beta"], inplace=True)
        results.reset_index(inplace=True)
        results.drop(["index"], axis=1, inplace=True)
        results.to_csv(csv_path.joinpath(f"U_{U}.csv"), index=False)

    return result_list


if __name__ == "__main__":
    clean_results()
