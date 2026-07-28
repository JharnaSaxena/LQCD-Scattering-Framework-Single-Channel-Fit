"""
Implementation of the single-channel Morningstar B-matrix
The B-matrix is constructed using the coefficients from Morningstar's tables together with the finite-volume zeta
function, computed values are cached since the optimizer often evaluates the same kinematic point multiple times.
"""
import numpy as np
from typing import Tuple, Optional, Dict, Any
import warnings
import sys
import os
from profiler import profiler

try:
    from b_tables import TABLE_B1, TABLE_B2, TABLE_B3, TABLE_B4, \
                         TABLE_B5, TABLE_B6, TABLE_B7, TABLE_B8
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from b_tables import TABLE_B1, TABLE_B2, TABLE_B3, TABLE_B4, \
                         TABLE_B5, TABLE_B6, TABLE_B7, TABLE_B8

hybrid_Z_refined = None
try:
    from tools.final_zeta import hybrid_Z as hybrid_Z_refined
except ImportError:
    try:
        from final_zeta import hybrid_Z as hybrid_Z_refined
    except ImportError:
        try:
            from .tools.final_zeta import hybrid_Z as hybrid_Z_refined
        except ImportError:
            hybrid_Z_refined = None
            warnings.warn("fast zeta function (tools.final_zeta.hybrid_Z) not found, using a simple pole approximation for B-matrix.",
                UserWarning
            )

class SingleChannelBMatrix:
    def __init__(self):
        self.compute_calls = 0
        self._b_cache = {}
        self._all_tables = {}
        for tbl in [TABLE_B1, TABLE_B2, TABLE_B3, TABLE_B4,
                    TABLE_B5, TABLE_B6, TABLE_B7, TABLE_B8]:
            self._all_tables.update(tbl)
        self._coeff_cache = {}

    def get_coefficient(self, irrep: str) -> float:
        if irrep in self._coeff_cache:
            return self._coeff_cache[irrep]
        for key, value in self._all_tables.items():
            if key[0] == irrep and key[-3:] == (0, 0, 1):
                for coeff, l, m, is_imag in value:
                    if l == 0 and m == 0 and not is_imag:
                        self._coeff_cache[irrep] = float(coeff)
                        return float(coeff)
                self._coeff_cache[irrep] = float(value[0][0])
                return float(value[0][0])
        self._coeff_cache[irrep] = 1.0
        return 1.0

    @profiler.decorator('Morningstar B')
    def compute(self, irrep: str, kin) -> float:
        self.compute_calls += 1
        profiler.increment_counter('B_matrix_calls')
        psq = kin.get_psq_label()
        u2 = round(kin.u2, 12)
        gamma = round(kin.gamma, 12)
        m_split = round(2.0 * kin.alpha, 12)
        key = (irrep, psq, u2, gamma, m_split)
        if key in self._b_cache:
            return self._b_cache[key]
        coeff = self.get_coefficient(irrep)
        if hybrid_Z_refined is not None:
            try:
                with profiler.context('Hybrid Zeta'):
                    Z00 = hybrid_Z_refined(
                        u2=kin.u2,
                        psq=psq,
                        gamma=kin.gamma,
                        m_split=m_split,
                        L=kin.L,
                    )
                profiler.increment_counter('hybrid_Z_calls')
            except Exception as e:
                warnings.warn(f"Zeta function failed: {e}, using pole approximation.")
                Z00 = 1.0 / (1.0 - kin.u2 + 1e-10)
        else:
            Z00 = 1.0 / (1.0 - kin.u2 + 1e-10)

        R00 = Z00 / (kin.gamma * np.pi**1.5)
        B = coeff * R00
        B_val = float(np.real(B))
        self._b_cache[key] = B_val
        return B_val

    def compute_with_details(self, irrep: str, kin):
        coeff = self.get_coefficient(irrep)
        psq = kin.get_psq_label()
        m_split = round(2.0 * kin.alpha, 12)
        u2 = round(kin.u2, 12)
        gamma = round(kin.gamma, 12)
        key = (irrep, psq, u2, gamma, m_split)
        if key in self._b_cache:
            B = self._b_cache[key]
            # We don't store Z00 separately compute only if needed for debug
            # we recompute Z00 (rarely used)
        if hybrid_Z_refined is not None:
            try:
                Z00 = hybrid_Z_refined(
                    u2=kin.u2,
                    psq=psq,
                    gamma=kin.gamma,
                    m_split=2.0*kin.alpha,
                    L=kin.L,
                )
            except Exception:
                Z00 = 1.0 / (1.0 - kin.u2 + 1e-10)
        else:
            Z00 = 1.0 / (1.0 - kin.u2 + 1e-10)
        R00 = Z00 / (kin.gamma * np.pi**1.5)
        B = coeff * R00
        return float(np.real(B)), float(np.real(Z00)), float(coeff), float(np.real(R00))

    def print_coefficients(self):
        print("\nS wave Coefficients:")
        test_irreps = ['A1g', 'T1u', 'G1u', 'G', 'A2']
        for ir in test_irreps:
            coeff = self.get_coefficient(ir)
            print(f"  {ir:>6}- {coeff:8.4f}")
        print("-" * 50)
        print(f"Compute calls- {self.compute_calls}")

    def get_stats(self) -> Dict[str, Any]:
        return {'compute_calls': self.compute_calls}

def compute_B(irrep: str, kin) -> float:
    bmatrix = SingleChannelBMatrix()
    return bmatrix.compute(irrep, kin)

def compute_R00(kin) -> float:
    psq = kin.get_psq_label()
    m_split = 2.0 * kin.alpha
    L = kin.L
    if hybrid_Z_refined is not None:
        try:
            Z00 = hybrid_Z_refined(
                u2=kin.u2,
                psq=psq,
                gamma=kin.gamma,
                m_split=m_split,
                L=L,
            )
        except Exception:
            Z00 = 1.0 / (1.0 - kin.u2 + 1e-10)
    else:
        Z00 = 1.0 / (1.0 - kin.u2 + 1e-10)
    return Z00 / (kin.gamma * np.pi**1.5)

if __name__ == "__main__":
    print("Morningstar BMat with cache")
