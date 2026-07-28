# LQCD Single-Channel Scattering Framework

**A complete pipeline for determining scattering parameters from lattice QCD energy levels using the Luscher method and Effective Range Expansion (ERE)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![arXiv](https://img.shields.io/badge/arXiv-2307.13471-b31b1b.svg)](https://arxiv.org/abs/2307.13471)

---

## Table of Contents

- [Overview](#overview)
- [Physics Background](#physics-background)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Usage Guide](#detailed-usage-guide)
- [Configuration](#configuration)
- [Units and Conventions](#units-and-conventions)
- [API Reference](#api-reference)
- [Complete Fit Trace](#complete-fit-trace)
- [Output Files](#output-files)
- [Constants Reference](#constants-reference)
- [Validation and Tests](#validation-and-tests)
- [Acknowledgments](#acknowledgments)
- [Citation](#citation)
- [License](#license)

---

## Overview

This package implements a complete Luscher analysis pipeline for determining scattering parameters from lattice QCD energy levels. The code follows the methodology described in arXiv:2307.13471 for single-channel pi-Sigma scattering analysis and uses the Morningstar B-matrix formalism for finite-volume corrections.

### Key Features

- Effective Range Expansion (ERE): Implements Eq. 12 of arXiv:2307.13471: `(k/mpi)cot(delta) = (E/mpi)[a + b*Delta]` with `Delta = (E^2 - threshold^2)/threshold^2`
- Luscher Quantization Condition: Solves `Omega(E) = Kinv(E) - B(E) = 0` using adaptive root finding
- Morningstar B-Matrix: Full implementation with caching and hybrid zeta function evaluation
- Correlated chi-square minimization: Uses bootstrap covariance matrix from lattice data
- Parallel prediction: Multi-core processing for energy level prediction
- Comprehensive statistics: AIC, BIC, pulls, parameter covariance, and reduced chi-square

### Physics Modules Implemented

| Module | Description | Key Equation |
|--------|-------------|---------------|
| ERE | Effective Range Expansion | `(k/mpi)cot(delta) = (E/mpi)[a + b*Delta]` |
| Kinematics | Relativistic two-body kinematics | `q_cm^2 = (E_lab^2 - P^2)/4 - (m1^2-m2^2)^2/(4*E_lab^2)` |
| B-Matrix | Finite-volume corrections | `B = C_irrep * Z00 / (gamma * pi^(3/2))` |
| Zeta Function | Finite-volume summation | `Z00 = sum_n [1/(n^2-u^2)] exp[-alpha(n-d)^2]` |
| Quantization | Luscher condition | `det[Kinv - B] = 0` |

---

## Physics Background

### Effective Range Expansion

The scattering amplitude in the S-wave is parameterized by the Effective Range Expansion:

```
(k / mpi) * cot(delta) = (E / mpi) * (a + b * Delta)
```

where:

- `k` is the relative momentum in the center-of-mass frame
- `mpi` is the pion mass (used as the unit scale, set to 1 in code)
- `delta` is the scattering phase shift
- `E` is the center-of-mass energy
- `a` is the scattering length (dimensionless)
- `b` is the effective range parameter (dimensionless)
- `Delta = (E^2 - Eth^2) / Eth^2` is the dimensionless energy deviation from threshold

### Energy Deviation Variable

```
Delta = (E^2 - Eth^2) / Eth^2
```

`Eth` is the threshold energy, defined as `Eth = m1 + m2` (pi-Sigma threshold in units of `mpi`). `Delta = 0` exactly at threshold, positive above, negative below.

### Luscher Quantization Condition

The allowed finite-volume energy levels are the roots of:

```
Omega(E) = Kinv(E) - B(E) = 0
```

where `Kinv(E)` is the inverse K-matrix from the ERE parameterization and `B(E)` is the finite-volume B-matrix. This is the single-channel reduction of the general determinant condition:

```
det[Kinv - B(E)] = 0
```

### Morningstar B-Matrix

```
B = C_irrep * Z00 / (gamma * pi^(3/2))
```

- `C_irrep` is a tabulated coefficient depending on the irreducible representation (lookup from Morningstar tables, `b_tables.py`)
- `Z00` is the finite-volume zeta function
- `gamma` is the Lorentz boost factor between the lab and center-of-mass frames

### Finite-Volume Zeta Function

```
Z00(u, d, gamma, alpha) = sum over n in Z^3 of [1 / (n^2 - u^2)] * exp[-alpha * (n - d)^2]
```

- `u` is a dimensionless momentum parameter
- `d = (L / 2*pi) * P` is the momentum shift vector
- `alpha = m1*m2 / (m1+m2)^2` is the mass asymmetry parameter
- `n` ranges over integer three-vectors

A pole-approximation fallback `Z00 ~= 1 / (1 - u^2 + epsilon)` is used if the exact hybrid zeta function is unavailable.

### Statistical Framework

Correlated chi-square is computed from the bootstrap covariance matrix of the lattice energy levels:

```
chi2 = (E_obs - E_pred)^T * C^(-1) * (E_obs - E_pred)
```

Bootstrap covariance:

```
C_ij = 1/(Nb - 1) * sum_b (E_i^b - Ebar_i)(E_j^b - Ebar_j)
```

Parameter covariance from the Jacobian of predicted energies with respect to fit parameters:

```
Cov_par = (J^T * C^(-1) * J)^(-1)
```

Additional diagnostics include standardized residuals (pulls), reduced chi-square, AIC, and BIC.

---

## Repository Structure

This repository is a combined codebase. The core pipeline scaffolding (`fvspectrum`, `general`, `config`, `run.py`, `pycalq.py`) belongs to Joseph Moscoso and his research team at the University of Maryland. All files inside the `qc2` folder were written and edited by me as part of my internship contribution.

```
.
├── fvspectrum/                     (Joseph Moscoso and team)
├── general/                        (Joseph Moscoso and team)
├── config/                         (Joseph Moscoso and team)
├── run.py                          (Joseph Moscoso and team)
├── pycalq.py                       (Joseph Moscoso and team)
│
├── qc2/                            (intern-authored / intern-edited, this contribution)
│   ├── ere.py                      Effective Range Expansion implementation
│   ├── stats.py                    Statistical utilities (chi2, covariance, AIC/BIC)
│   ├── root_finder.py              Root finding for the quantization condition
│   ├── morningstar_bmatrix.py      Morningstar B-matrix implementation
│   ├── fitting_driver_canonical.py Main fitting driver (PhysicsModule, LuscherFitter)
│   ├── run_fit_from_dataset.py     Main execution script
│   ├── dataset_loader.py           HDF5 data loading
│   ├── pipeline_adapter.py         Naming convention adapters
│   ├── profiler.py                 Profiling utility
│   ├── plot_figure8.py             Spectrum plot generation (Figure 8)
│   ├── plot_spectrum.py            Spectrum plot wrapper
│   ├── fit_plots.py                Fit diagnostic plots
│   ├── plot.py                     ERE / Luscher curve reproduction (Figure 10 style)
│   ├── fit_results.json            Output: fit results
│   └── figure8_data_points.csv     Output: data points for Figure 8
│
├── PROJECT_ARCHITECTURE.md
├── PHYSICS_REFERENCE.md
├── UNITS_AND_CONVENTIONS.md
├── CONSTANTS.md
├── CODE_INVENTORY.md
├── API_REFERENCE.md
├── COMPLETE_FIT_TRACE.md
└── README.md
```

Note: paths above reflect logical grouping. Refer to the actual repository tree for exact file locations, since `fvspectrum`, `general`, `config`, `run.py`, and `pycalq.py` define the surrounding pipeline that invokes the `qc2` modules.

---

## Installation

### Requirements

- Python 3.8 or newer
- numpy
- scipy
- matplotlib
- h5py

### Setup

Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install numpy scipy matplotlib h5py
```

Or, if a requirements file is provided:

```bash
pip install -r requirements.txt
```

Suggested `requirements.txt` contents:

```
numpy>=1.21
scipy>=1.7
matplotlib>=3.4
h5py>=3.6
```

---

## Quick Start

### 1. Configure the run

Open `qc2/run_fit_from_dataset.py` and set the dataset path and physics parameters:

```python
HDF5_PATH = "path/to/DataSet.hdf5"
L = 64.0
MREF = 0.06533
M1_PHYS = 0.06533
M2_PHYS = 0.3830
SELECTED_INDICES = [11, 35, 67, 121]
INITIAL_GUESS = [0.047, 0.65]
BOUNDS = [(-10.0, 10.0), (-10.0, 10.0)]
```

### 2. Run the fit

```bash
python qc2/run_fit_from_dataset.py
```

This will:

1. Load energy levels from the HDF5 dataset
2. Build the quantization condition using the Morningstar B-matrix
3. Minimize the correlated chi-square to determine ERE parameters `a` and `b`
4. Save results to `fit_results.json`
5. Print a profiling report of timings and function-call counters

### 3. Generate the spectrum plot

```bash
python qc2/plot_figure8.py
```

This reproduces Figure 8 style plots: lattice data points, non-interacting energy bands, and physical thresholds.

### 4. Inspect available energy levels

```python
from qc2.dataset_loader import DataLoader

loader = DataLoader("path/to/DataSet.hdf5", L=64, use_ref=True)
levels = loader.scan_levels()
loader.print_levels_sorted_by_energy(levels)
```

### 5. Read back the fit results

```python
import json

with open("fit_results.json") as f:
    results = json.load(f)

params = results["result"]["params"]      # [a, b]
chi2 = results["result"]["chi2"]
reduced_chi2 = results["result"]["reduced_chi2"]
errors = results["result"]["errors"]

print("a =", params[0], "+/-", errors[0])
print("b =", params[1], "+/-", errors[1])
print("chi2 / ndof =", reduced_chi2)
```

---

## Detailed Usage Guide

### Loading and Inspecting Data

The `DataLoader` class in `dataset_loader.py` reads energy levels from an HDF5 dataset with the following expected structure:

```
HDF5/
  isoXYZ/                (optional channel layer)
    PSQ0/
      G1u/
        ecm_0_ref   [mean, boot1, boot2, ...]
        ecm_1_ref   [mean, boot1, boot2, ...]
    PSQ1/
      G1/
        ecm_1_ref   [...]
```

Example workflow:

```python
from qc2.dataset_loader import DataLoader

loader = DataLoader("DataSet.hdf5", L=64.0, use_ref=True)
levels_scan = loader.scan_levels()

dataset = loader.build_dataset(
    indices=[11, 35, 67, 121],
    levels_scan=levels_scan,
    m1=1.0,
    m2=5.862544007347314,
)

print(dataset.means)
print(dataset.covariance)
```

### Building the Fitter Manually

```python
from qc2.fitting_driver_canonical import LuscherFitter, PhysicsModule
from qc2.morningstar_bmatrix import SingleChannelBMatrix
from qc2.pipeline_adapter import PSQ_TO_D

physics = PhysicsModule(L=64.0, m1=1.0, m2=5.862544007347314,
                         bmatrix_impl=SingleChannelBMatrix())

fitter = LuscherFitter(
    observed_mean=dataset.means,
    bootstrap_samples=dataset.bootstrap,
    irrep_list=["G1u", "G1", "G", "G"],
    d_list=[(0, 0, 0), (0, 0, 1), (1, 1, 0), (1, 1, 1)],
    L=64.0,
    m1=1.0,
    m2=5.862544007347314,
    physics=physics,
    cov_matrix=dataset.covariance,
)

result = fitter.fit(initial_guess=[0.047, 0.65],
                     bounds=[(-10, 10), (-10, 10)])

print(result.params, result.chi2, result.reduced_chi2)
fitter.save_results("fit_results.json")
```

### Evaluating the ERE Directly

```python
from qc2.ere import ERE

ere = ERE([0.0493, 0.6500])

class Kin:
    E_cm = 6.90
    threshold = 6.8625

kinv = ere.compute_kinv(Kin())
cot_delta = ere.compute_cot_delta(Kin())
phase_deg = ere.compute_phase_shift(Kin())

print(kinv, cot_delta, phase_deg)
```

### Diagnostic Plots

```python
from qc2.fit_plots import plot_bmatrix_preview, plot_quantization_condition

plot_bmatrix_preview(irrep="G1u", d=(0, 0, 0), L=64.0, m1=1.0, m2=5.8625)
plot_quantization_condition(irrep="G1u", d=(0, 0, 0), ere_params=[0.0493, 0.6500])
```

---

## Configuration

The main run parameters live in `qc2/run_fit_from_dataset.py`:

| Parameter | Type | Description |
|-----------|------|-------------|
| `HDF5_PATH` | str | Path to the input HDF5 dataset |
| `L` | float | Lattice size (number of sites per dimension) |
| `MREF` | float | Reference mass in GeV used to scale masses to units of `mpi` |
| `M1_PHYS` | float | Physical pion mass in GeV |
| `M2_PHYS` | float | Physical sigma mass in GeV |
| `SELECTED_INDICES` | list of int | Energy level indices to include in the fit |
| `INITIAL_GUESS` | array | Initial guess for ERE parameters `[a, b]` |
| `BOUNDS` | list of tuples | Optimization bounds for `[a, b]` |

Additional tunable parameters live inside `RootFinder` (in `root_finder.py`) and are described in the [Constants Reference](#constants-reference) section below.

---

## Units and Conventions

The codebase uses a dimensionless system of units:

- Pion mass is set to unity: `mpi = 1`
- Lattice spacing is set to unity: `a = 1` (lattice units)
- All masses, momenta, and energies are expressed in units of `mpi`
- Lattice size `L` is the number of lattice sites (dimensionless)

This convention is achieved by scaling all input masses by `MREF`, the reference mass equal to the physical pion mass in GeV. For example:

```
m1 = M1_PHYS / MREF = 1.0
m2 = M2_PHYS / MREF  ~=  5.8625
```

Momenta are quantized as `p = (2*pi / L) * n` for integer vector `n`. Since `L` is measured in lattice units with `a = 1`, and `mpi = 1`, the product `mpi * L` (and hence `L` itself) is dimensionless.

| Quantity | Symbol | Units | Where computed |
|----------|--------|-------|-----------------|
| Pion mass | mpi | 1 (fixed) | run_fit_from_dataset.py |
| Sigma mass | m2 | mpi | run_fit_from_dataset.py |
| CM energy | E | mpi | fitting_driver_canonical.py |
| Threshold energy | Eth | mpi | ere.py |
| Relative momentum | k, q_cm | mpi | tools/kinematics.py |
| Lattice size | L | lattice units | run_fit_from_dataset.py |
| Inverse K-matrix | Kinv | dimensionless | ere.py |
| B-matrix | B | dimensionless | morningstar_bmatrix.py |
| Zeta function | Z00 | dimensionless | tools/final_zeta.py |
| Chi-square | chi2 | dimensionless | stats.py |
| Covariance matrix | C | (mpi)^2 | stats.py |

No explicit unit conversions occur inside the core physics modules; all inputs are assumed consistent with this convention. The only conversion occurs when physical masses are scaled by `MREF` at the start of the pipeline.

---

## API Reference

### `ere.py`

**Class `ERE`**

```python
ERE(coeffs)
```

Argument `coeffs` is a list or array of ERE coefficients `[a, b]`. Raises `ValueError` if empty, has more than two parameters, or contains NaN/Inf.

Methods:

- `compute_kinv(kin)` returns `Kinv`, computed as `E * (a + b*Delta)` if `kin` has `E_cm` and `threshold` attributes, or `a + b*q^2` if `kin` is a float.
- `compute_cot_delta(kin)` returns `cot(delta) = Kinv / q_cm` above threshold, or `Kinv / kappa` below threshold.
- `compute_phase_shift(kin)` returns the phase shift in degrees, computed as `arctan2(q_cm, Kinv)`.
- `get_coeffs()` returns an `ERECoefficients` object with `coeffs` and `labels`.

Helper functions: `standard_ere(a0=None, r0=None)` and `constant_ere(c0=0.0)`.

### `fitting_driver_canonical.py`

**Class `PhysicsModule`**

```python
PhysicsModule(L, m1, m2, bmatrix_impl=None)
```

Methods:

- `compute_kinematics(E_cm, d)` returns a cached `KinematicVars` object.
- `compute_bmatrix(irrep, kin)` returns the B-matrix value.
- `compute_kinv(kin, ere)` returns `Kinv`.
- `build_omega(irrep, d, E_cm, ere)` returns a callable `omega(E) = Kinv(E) - B(E)`.

**Class `LuscherFitter`**

```python
LuscherFitter(
    observed_mean, bootstrap_samples, irrep_list, d_list,
    L, m1, m2, physics=None, root_finder=None,
    cov_matrix=None, free_energies=None,
    debug_objective=False, max_workers=None,
)
```

Methods:

- `predict_energies(params)` returns an array of predicted energies using parallel root finding.
- `objective(params)` returns the correlated chi-square value.
- `fit(initial_guess, bounds=None, verbose=True, param_labels=None, method='nelder-mead', maxiter=5000, compute_vij=True)` returns a `FitResult`.
- `save_results(filename)` serializes the `FitResult` to JSON.

### `root_finder.py`

**Class `RootFinder`**

```python
RootFinder(
    xtol=1e-12, rtol=1e-12, maxiter=100,
    pole_threshold=1e12, root_tolerance=1e-4,
    local_scan_points=100,
    global_scan_min=0.1, global_scan_max=50.0,
    global_scan_points=500, verbose=False,
    benchmark=False, debug=False,
    continuity_tol=0.3, observed_tol=0.5,
)
```

Method `find_root_near_guess(f, x_guess, prev_root=None, exclude_points=None, tolerance=1e-4, reference_energy=None, lower_bound=None, upper_bound=None, level_index=None)` returns the root energy.

Algorithm:

1. Adaptive bracketing with widths `[0.02, 0.05, 0.10, 0.20, 0.40, 0.80, 1.5]`
2. Ordered root selection by `level_index` if multiple roots are found
3. Dense local scan fallback if bracketing fails
4. Minimization of `|omega(E)|` as ultimate fallback

### `morningstar_bmatrix.py`

**Class `SingleChannelBMatrix`**

Method `compute(irrep, kin)` returns `B = C_irrep * Z00 / (gamma * pi^1.5)`, with caching keyed on `(irrep, psq, u2, gamma, m_split)`. Falls back to the pole approximation `Z00 ~= 1/(1-u^2+eps)` if the hybrid zeta function is unavailable.

Method `get_coefficient(irrep)` returns the tabulated S-wave coefficient. Method `compute_with_details(irrep, kin)` returns `(B, Z00, coeff, R00)` for debugging.

### `stats.py`

| Function | Signature | Returns |
|----------|-----------|---------|
| `bootstrap_covariance` | `(bootstrap_samples)` | Covariance matrix |
| `chi2` | `(observed_mean, predicted, covariance)` | Chi-square value |
| `parameter_covariance` | `(jacobian, data_cov, chi2_value=None, n_data=None, n_params=None)` | Parameter covariance matrix |
| `parameter_errors` | `(cov_par)` | Standard deviations |
| `reduced_chi2` | `(chi2_value, n_data, n_params)` | Reduced chi-square |
| `standardized_residuals` | `(observed_mean, predicted, covariance)` | Pulls |
| `correlation_matrix` | `(covariance)` | Correlation matrix |
| `aic` | `(chi2_value, n_params, n_data)` | AIC |
| `bic` | `(chi2_value, n_params, n_data)` | BIC |

`FitResult` is a dataclass with attributes `params`, `chi2`, `ndof`, `reduced_chi2`, `cov_params`, `errors`, `corr_params`, `pulls`, `residuals`, `predicted`, `aic`, `bic`, `success`, `message`, `n_iter`, `n_evaluations`, `param_labels`, and a `to_dict()` method for JSON serialization.

### `dataset_loader.py`

**Class `DataLoader`**

```python
DataLoader(file_path, L, use_ref=True)
```

Methods:

- `scan_levels()` returns a list of dicts with keys `psq`, `irrep`, `level`, `key`, `index`.
- `build_dataset(indices, levels_scan, m1=1.0, m2=3.5653)` returns a `DataSet` with `metadata`, `means`, `bootstrap`, `covariance`, `free_energies`.
- `print_levels()` and `print_levels_sorted_by_energy()` print available levels.

### `pipeline_adapter.py`

`PSQ_TO_D` maps `PSQ0` through `PSQ4` to momentum vectors, for example `PSQ0 -> (0,0,0)`, `PSQ1 -> (0,0,1)`, `PSQ2 -> (1,1,0)`, `PSQ3 -> (1,1,1)`.

`full_irrep_label(psq, irrep)` converts to the Morningstar label format, for example `full_irrep_label("PSQ2", "G") -> "G(2)"`.

### `profiler.py`

A global `profiler` instance provides `start`, `stop`, `record`, `increment_counter`, `context` (context manager), `decorator`, and `report`. Tracked counters include `chi2_evaluations`, `omega_evaluations`, `root_finder_calls`, `root_iterations`, `root_solver_attempts`, `hybrid_Z_calls`, `B_matrix_calls`, and `ERE_calls`.

### Plotting modules

- `plot_figure8.py`: `plot_figure8_from_hdf5(hdf5_path, L, use_ref=True, energy_window=(6.5, 8.5), save_path=None)` returns `(fig, ax)`, reproducing the finite-volume spectrum figure with lattice data, non-interacting bands, and thresholds.
- `plot_spectrum.py`: `make_spectrum_plot(energy_cm_data, massN, lattice_size, save_path=None, ...)` returns a matplotlib figure, used by the external HPW fit pipeline.
- `fit_plots.py`: diagnostic functions `plot_bmatrix_preview`, `plot_quantization_condition`, `plot_phase_shifts_multichannel`, `plot_omega_and_eigenvalues`, `plot_fit_comparison`.
- `plot.py`: reproduces Figure 10 style plots (`(k/mpi)^2` vs `(k/mpi)cot(delta)`) with Luscher curves, ERE band, and virtual-state curve, using an externally defined `GeneralizedFitModel`.

---

## Complete Fit Trace

A full run proceeds through the following call chain:

1. `run_fit_from_dataset.py` sets configuration constants and instantiates `DataLoader`.
2. `DataLoader.scan_levels()` and `DataLoader.build_dataset()` load energy levels, bootstrap samples, and compute the covariance matrix.
3. `PhysicsModule` and `LuscherFitter` are instantiated with the loaded dataset.
4. `LuscherFitter.fit()` calls `scipy.optimize.minimize` with the Nelder-Mead method.
5. Each objective evaluation calls `predict_energies()`, which calls `_predict_single_level()` in parallel for every data point.
6. For each level, `PhysicsModule.build_omega()` constructs `omega(E) = Kinv(E) - B(E)`, and `RootFinder.find_root_near_guess()` locates the root, using kinematics from `compute_kinematics()` and the B-matrix from `SingleChannelBMatrix.compute()`.
7. Once all predicted energies are collected, `stats.chi2()` computes the correlated chi-square, which is returned to the optimizer.
8. After convergence, pulls, reduced chi-square, AIC, BIC, and parameter covariance (via finite-difference Jacobian and `stats.parameter_covariance()`) are computed.
9. Results are packaged into a `FitResult` and saved to `fit_results.json` via `save_results()`.
10. The profiler report is printed to the console.

Flow diagram:

```
run_fit_from_dataset.py
        |
        v
DataLoader.scan_levels / build_dataset
        |
        v
PhysicsModule + LuscherFitter instantiated
        |
        v
fitter.fit(initial_guess)  --->  scipy.optimize.minimize (Nelder-Mead)
        |
        v
objective(params)
        |
        v
predict_energies(params)  --->  parallel _predict_single_level per data point
        |
        v
build_omega(E) = Kinv(E) - B(E)
        |
        v
RootFinder.find_root_near_guess
        |
        +--> compute_kinematics  (q_cm^2, gamma, alpha, u)
        +--> compute_bmatrix     (B = C_irrep * Z00 / (gamma * pi^1.5))
        +--> compute_kinv        (Kinv = E*(a + b*Delta))
        |
        v
Root found: E_pred_i for each level
        |
        v
stats.chi2(observed, predicted, covariance)
        |
        v
chi2 returned to optimizer, loop continues until convergence
        |
        v
Compute predicted, residuals, pulls, AIC, BIC, parameter covariance
        |
        v
FitResult constructed
        |
        v
save_results("fit_results.json")
        |
        v
Console output and profiling report
```

---

## Output Files

### `fit_results.json`

```json
{
  "result": {
    "params": [0.04935137230852598, 0.6499972736461315],
    "chi2": 3.315,
    "ndof": 2,
    "reduced_chi2": 1.657,
    "errors": [3.51e-06, 8.66e-06],
    "pulls": [0.652, 1.247],
    "predicted": [6.725, 6.739]
  },
  "input_data": {
    "observed_mean": [6.748, 6.783],
    "irreps": ["G1u(0)", "G1(1)"],
    "cov_matrix": []
  }
}
```

### `figure8_data_points.csv`

Columns: `psq`, `irrep`, `level`, `mean`, `error`, `n_bootstrap`, `index`, `key`.

### `figure8_final.pdf`

Rendered spectrum plot generated by `plot_figure8.py`, showing lattice data points, non-interacting energy bands, and physical thresholds.

---

## Constants Reference

### Mathematical constants

| Constant | Value | Used in |
|----------|-------|---------|
| `pi` | 3.141592653589793 | B-matrix, kinematics, zeta function |
| `pi^(3/2)` | 5.568327996831707 | B-matrix normalization |

### Physical input constants (example run configuration)

| Constant | Value | Description |
|----------|-------|--------------|
| `MREF` | 0.06533 GeV | Reference mass used to scale to units of mpi |
| `M1_PHYS` | 0.06533 GeV | Physical pion mass |
| `M2_PHYS` | 0.3830 GeV | Physical sigma mass |
| `L` | 64.0 | Lattice size |
| `m1` | 1.0 | Pion mass in units of mpi |
| `m2` | ~5.862544007347314 | Sigma mass in units of mpi |
| `threshold` | ~6.862544 | pi-Sigma threshold in units of mpi |

### Fitted ERE parameters (example run)

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `a` | 0.04935137230852598 | Scattering length |
| `b` | 0.6499972736461315 | Effective range parameter |

These values are specific to the example dataset used during development. Different datasets produce different fitted values.

### Algorithmic tolerances

| Constant | Value | Purpose |
|----------|-------|---------|
| `root_tolerance` | 1e-4 | Tolerance for accepting a root |
| `continuity_tol` | 0.3 | Maximum distance from previous root for continuity |
| `observed_tol` | 0.5 | Tolerance for selecting root near observed energy |
| `xtol` | 1e-12 | Brent's method tolerance |
| `rtol` | 1e-12 | Brent's method relative tolerance |
| `maxiter` (root finding) | 100 | Maximum iterations for Brent's method |
| `local_scan_points` | 50 | Number of points in local fallback scan |
| `global_scan_points` | 500 | Number of points in global scan (currently unused) |
| `epsilon` (Jacobian) | 1e-5 | Finite-difference step size |
| `xatol`, `fatol` (Nelder-Mead) | 1e-6 | Optimizer convergence tolerances |
| `maxiter` (optimizer) | 5000 | Maximum Nelder-Mead iterations |

---

## Validation and Tests

The pipeline has been checked against the following criteria during development:

- Reduced chi-square close to unity for well-behaved fits, indicating consistent error estimation
- Pulls approximately normally distributed, `N(0, 1)`, across included energy levels
- Root finding stability verified via ordered root selection and continuity tolerance across bootstrap samples
- B-matrix values cross-checked against Morningstar tabulated coefficients for the irreps used in the fit (`G1u(0)`, `G1(1)`, `G(2)`, `G(3)`)
- Parameter covariance validated by comparing finite-difference Jacobian results against the reduced chi-square scaling convention

Recommended validation workflow before trusting new results:

1. Run `run_fit_from_dataset.py` and confirm `success=True` in the fit output.
2. Check `reduced_chi2` is close to 1; large deviations may indicate underestimated errors or missing systematics.
3. Inspect `pulls` for any outliers beyond about 3 standard deviations.
4. Generate `plot_figure8.py` output and visually confirm predicted levels align with the observed lattice data.
5. Review the profiler report to confirm root finding did not fall back excessively to the minimization strategy, since frequent fallbacks may indicate poor initial guesses or bracketing issues.

---

## Acknowledgments

This project was carried out as part of an internship under the supervision of **Joseph Moscoso** at the **University of Maryland (UMD)**. I am sincerely grateful to Joseph for his guidance, mentorship, and the opportunity to contribute to this research pipeline.

The overall pipeline scaffolding, including the `fvspectrum` and `general` directories, the `config` files, and the top-level `run.py` and `pycalq.py` scripts, was built by Joseph Moscoso and his research team and is included here for context and reproducibility. My contribution as an intern was limited to writing and editing the files within the `qc2` folder, covering the ERE implementation, the fitting driver, the root finder, the Morningstar B-matrix module, the statistics utilities, the data loader, the pipeline adapters, the profiler, and the plotting scripts described in this document.

Thank you to Joseph Moscoso and the entire team for their support throughout this project.

---

## Citation

If you use this code in your research, please cite the original methodology paper:

```
arXiv:2307.13471
```

and the Morningstar B-matrix formalism paper:

```
Morningstar et al., Physical Review D 104 (2021)
```

and the original Luscher formalism:

```
M. Luscher, Nuclear Physics B 354 (1991)
```

---

## License

This project is released under the MIT License. See the LICENSE file for details. Portions of this repository (`fvspectrum`, `general`, `config`, `run.py`, `pycalq.py`) are the work of Joseph Moscoso and his team at the University of Maryland and are included with permission for the purpose of this combined pipeline.
