from pathlib import Path
import subprocess
import io
import os
import pandas as pd
import numpy as np
import shutil
import typing as T

R = Path(__file__).parent
src_dir = R / "src"
build_dir = R / "build"
TXW0 = 1e3  # ITU assumes 1kW power

ninja = shutil.which("ninja")

grwave_exe = shutil.which("grwave.bin", path=str(build_dir))
if not grwave_exe:
    if shutil.which("cmake"):
        opts = []
        if ninja:
            opts = ["-G", "Ninja"]
        elif os.name == "nt":
            opts = ["-G", "MinGW Makefiles", "-DCMAKE_SH=CMAKE_SH-NOTFOUND"]
        subprocess.run(["cmake", "-S", str(src_dir), "-B", str(build_dir)] + opts)
        subprocess.run(["cmake", "--build", str(build_dir)])
    elif shutil.which("meson") and ninja:
        subprocess.run(["meson", str(src_dir), str(build_dir)])
        subprocess.run(["ninja", "-C", str(build_dir)])
grwave_exe = shutil.which("grwave.bin", path=str(build_dir))
if not grwave_exe:
    raise ImportError("need to compile grwave.bin")


def grwave(wls: T.Dict[str, T.Any]) -> pd.DataFrame:

    strin = (
        f'ans {wls["ans"]}\n'
        f'hscale {wls["hscale"]}\n'
        f'ipolrn {wls["ipolrn"]}\n'
        f'freq {wls["freqMHz"]}\n'
        f'sigma {wls["sigma"]}\n'
        f'epslon {wls["epslon"]}\n'
        f'dmax {wls["dmax"]}\n'
        f'dmin {wls["dmin"]}\n'
        f'hrr {wls["hrr"]}\n'
        f'htt {wls["htt"]}\n'
        f'loglin {wls["loglin"]}\n'
        f'dstep {wls["dstep"]}\n'
        "GO"
    )

    out = subprocess.check_output([grwave_exe], input=strin, universal_newlines=True)
    # Remove error lines
    splitout = out.split("\n")
    matches = [x for x in splitout if x[len(x)-3:] == "(R)"]
    for match in matches:
        splitout.remove(match)
        
    out = "\n".join(splitout)
    # %%
    data = pd.read_csv(io.StringIO(out), sep=r"\s+", index_col=0, skiprows=31, names=["fs", "pathloss"])

    data.dropna(how="all", axis=0, inplace=True)
    data = data[~data.index.duplicated(keep="last")]
    data.index = data.index.astype(float)

    data["fs"] *= np.sqrt(wls["txwatt"] / TXW0)

    return data
