#!/usr/bin/env python3
"""
run_fit_from_dataset.py - Fits the ERE parametrization to lattice data.
Uses raw statistical covariance from HDF5 bootstrap samples (paper method).
"""
import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset_loader import DataLoader
from pipeline_adapter import PSQ_TO_D, full_irrep_label
from morningstar_bmatrix import SingleChannelBMatrix as MorningstarBMatrix
from fitting_driver_canonical import LuscherFitter, PhysicsModule
from profiler import profiler

# Configuration
HDF5_PATH = os.path.expanduser("~/Desktop/Last_Week/my_work/DataSet.hdf5")
L = 64.0
MREF = 0.06533
M1_PHYS = 0.06533
M2_PHYS = 0.3830
SELECTED_INDICES = [11, 35, 67, 121]
INITIAL_GUESS = np.array([0.047, 0.65])
BOUNDS = [(-10.0, 10.0), (-10.0, 10.0)]

# Load dataset
loader = DataLoader(HDF5_PATH, L, use_ref=True)
levels = loader.scan_levels()
m1 = M1_PHYS / MREF
m2 = M2_PHYS / MREF
dataset = loader.build_dataset(SELECTED_INDICES, levels, m1=m1, m2=m2)

print("\nLoaded dataset:")
for i, meta in enumerate(dataset.metadata):
    free_str = f", free={dataset.free_energies[i]:.6f}" if dataset.free_energies[i] is not None else ""
    print(f"  {i}: {meta['psq']} {meta['irrep']} level {meta['level']}  mean={dataset.means[i]:.6f}{free_str}")
observed_mean = dataset.means
bootstrap_samples = dataset.bootstrap
irrep_list = [full_irrep_label(meta['psq'], meta['irrep']) for meta in dataset.metadata]
d_list = [PSQ_TO_D[meta['psq']] for meta in dataset.metadata]

# Use raw statistical covariance from bootstrap
total_cov_matrix = dataset.covariance
print("\nUsing raw statistical covariance from HDF5 bootstrap (paper method)")
print(f"Covariance matrix:\n{total_cov_matrix}")
print(f"Condition number: {np.linalg.cond(total_cov_matrix):.3e}")

# Build PhysicsModule
bmatrix_impl = MorningstarBMatrix()
physics = PhysicsModule(L, m1, m2, bmatrix_impl=bmatrix_impl)

# Instantiate fitter
fitter = LuscherFitter(
    observed_mean=observed_mean,
    bootstrap_samples=bootstrap_samples,
    irrep_list=irrep_list,
    d_list=d_list,
    L=L,
    m1=m1,
    m2=m2,
    physics=physics,
    cov_matrix=total_cov_matrix,
    free_energies=dataset.free_energies,
)

# Run the fit
print("\nRunning optimizer")
start_time = time.perf_counter()
result = fitter.fit(
    initial_guess=INITIAL_GUESS,
    bounds=BOUNDS,
    verbose=True,
    method='lbfgsb',
    maxiter=5000,
)
fit_time = time.perf_counter() - start_time
print(f"\nOptimization finished in {fit_time:.2f} seconds.")

fitter.save_results("fit_results.json")
print("PROFILING REPORT")
profiler.report()
