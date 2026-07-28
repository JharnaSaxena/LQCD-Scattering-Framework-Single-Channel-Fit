# LQCD Single-Channel Scattering Framework

**A complete pipeline for determining scattering parameters from lattice QCD energy levels using the Lüscher method and Effective Range Expansion (ERE)**

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
- [API Reference](#api-reference)
- [Output Files](#output-files)
- [Validation & Tests](#validation--tests)
- [Acknowledgments](#acknowledgments)
- [Citation](#citation)
- [License](#license)

---

## Overview

This package implements a complete **Lüscher analysis pipeline** for determining scattering parameters from lattice QCD energy levels. The code follows the methodology described in arXiv:2307.13471 for single-channel πΣ scattering analysis and uses the **Morningstar B-matrix** formalism for finite-volume corrections.

### Key Features

- **Effective Range Expansion (ERE)**: Implements Eq. 12 of arXiv:2307.13471: `(k/mπ)cotδ = (E/mπ)[a + bΔ]` with `Δ = (E² - threshold²)/threshold²`
- **Lüscher Quantization Condition**: Solves `Ω(E) = K⁻¹(E) - B(E) = 0` using adaptive root finding
- **Morningstar B-Matrix**: Full implementation with caching and hybrid zeta function evaluation
- **Correlated χ² Minimization**: Uses bootstrap covariance matrix from lattice data
- **Parallel Prediction**: Multi-core processing for energy level prediction
- **Comprehensive Statistics**: AIC, BIC, pulls, parameter covariance, and reduced χ²

### Physics Modules Implemented

| Module | Description | Key Equation |
|--------|-------------|--------------|
| ERE | Effective Range Expansion | `(k/mπ)cotδ = (E/mπ)[a + bΔ]` |
| Kinematics | Relativistic two-body kinematics | `q_cm² = (E_lab² - P²)/4 - (m1²-m2²)²/(4E_lab²)` |
| B-Matrix | Finite-volume corrections | `B = C_irrep × Z₀₀/(γπ^(3/2))` |
| Zeta Function | Finite-volume summation | `Z₀₀ = Σ_n 1/(n²-u²)exp[-α(n-d)²]` |
| Quantization | Lüscher condition | `det[K⁻¹ - B] = 0` |

---

## Physics Background

### Effective Range Expansion

The scattering amplitude in the S-wave is parameterized by the Effective Range Expansion:

$$ \frac{k}{m_\pi}\cot\delta = \frac{E}{m_\pi}\left(a + b\Delta\right) $$

where:
- `k` is the relative momentum in the center-of-mass frame
- `mπ` is the pion mass (used as the unit scale)
- `δ` is the scattering phase shift
- `E` is the center-of-mass energy
- `a` is the scattering length (dimensionless)
- `b` is the effective range parameter (dimensionless)
- `Δ = (E² - Eth²)/Eth²` is the dimensionless energy deviation
