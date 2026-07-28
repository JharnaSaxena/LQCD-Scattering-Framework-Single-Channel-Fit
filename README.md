<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>fvspectrum · Lüscher Analysis Pipeline</title>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
    <!-- Google Fonts: Inter + JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <style>
        /* ---------- Reset & Base ---------- */
        *,
        *::before,
        *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f9fafb;
            color: #1e293b;
            line-height: 1.7;
            padding: 2rem 1rem;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.06);
            padding: 2.5rem 2.5rem 3.5rem;
        }
        @media (max-width: 720px) {
            .container {
                padding: 1.5rem 1.2rem;
            }
            body {
                padding: 1rem 0.5rem;
            }
        }

        /* ---------- Typography ---------- */
        h1,
        h2,
        h3,
        h4 {
            font-weight: 600;
            line-height: 1.3;
            letter-spacing: -0.02em;
        }
        h1 {
            font-size: 2.6rem;
            margin-bottom: 0.25rem;
            background: linear-gradient(145deg, #0b1e33, #1a3a5c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        h1 .sub {
            font-weight: 400;
            font-size: 1.1rem;
            color: #475569;
            -webkit-text-fill-color: #475569;
            display: block;
            margin-top: 0.1rem;
        }
        h2 {
            font-size: 1.8rem;
            margin-top: 2.8rem;
            margin-bottom: 1rem;
            padding-bottom: 0.4rem;
            border-bottom: 3px solid #e9edf4;
        }
        h2 i {
            color: #2563eb;
            margin-right: 0.5rem;
        }
        h3 {
            font-size: 1.3rem;
            margin-top: 2rem;
            margin-bottom: 0.7rem;
            color: #0b1e33;
        }
        h4 {
            font-size: 1.05rem;
            margin-top: 1.6rem;
            margin-bottom: 0.4rem;
            color: #1e293b;
        }
        a {
            color: #2563eb;
            text-decoration: none;
            transition: color 0.15s;
        }
        a:hover {
            color: #1d4ed8;
            text-decoration: underline;
        }
        p {
            margin-bottom: 1rem;
        }
        code,
        .code-inline {
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.875em;
            background: #f1f4f9;
            padding: 0.15rem 0.45rem;
            border-radius: 0.3rem;
            color: #0b1e33;
        }
        pre {
            background: #0f172a;
            color: #e2e8f0;
            padding: 1.4rem 1.6rem;
            border-radius: 1rem;
            overflow-x: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            line-height: 1.6;
            margin: 1.2rem 0;
            border: 1px solid #1e293b;
        }
        pre code {
            background: transparent;
            padding: 0;
            color: inherit;
            font-size: inherit;
        }
        hr {
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 2.5rem 0;
        }

        /* ---------- Badges / Meta ---------- */
        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem 1.2rem;
            margin: 0.75rem 0 1.5rem;
            align-items: center;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: #eef2f6;
            padding: 0.25rem 0.9rem;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 500;
            color: #1e293b;
        }
        .badge i {
            color: #2563eb;
        }
        .badge.primary {
            background: #dbeafe;
            color: #1e40af;
        }
        .badge.primary i {
            color: #2563eb;
        }
        .badge.green {
            background: #dcfce7;
            color: #166534;
        }
        .badge.green i {
            color: #16a34a;
        }

        /* ---------- Cards & Grids ---------- */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 1.2rem;
            margin: 1.2rem 0;
        }
        .card {
            background: #f8fafc;
            border-radius: 1rem;
            padding: 1.2rem 1.4rem;
            border: 1px solid #e9edf4;
            transition: border 0.15s;
        }
        .card:hover {
            border-color: #b9c7da;
        }
        .card .title {
            font-weight: 600;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card .title i {
            color: #2563eb;
            width: 1.2rem;
        }
        .card .desc {
            font-size: 0.9rem;
            color: #475569;
            margin-top: 0.3rem;
        }

        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 0.6rem;
            margin: 0.8rem 0 1.2rem;
        }
        .file-tag {
            background: #f1f4f9;
            padding: 0.25rem 0.9rem;
            border-radius: 50px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            border: 1px solid #e2e8f0;
            display: inline-block;
        }
        .file-tag i {
            margin-right: 0.3rem;
            color: #64748b;
        }

        /* ---------- Tables ---------- */
        .table-wrap {
            overflow-x: auto;
            margin: 1.2rem 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }
        th,
        td {
            padding: 0.6rem 0.9rem;
            border-bottom: 1px solid #e9edf4;
            text-align: left;
        }
        th {
            background: #f1f4f9;
            font-weight: 600;
            color: #0b1e33;
        }
        tr:hover td {
            background: #fafbfc;
        }

        /* ---------- Special blocks ---------- */
        .note {
            background: #f0f7ff;
            border-left: 4px solid #2563eb;
            padding: 1rem 1.4rem;
            border-radius: 0.6rem;
            margin: 1.2rem 0;
            font-size: 0.95rem;
        }
        .note i {
            color: #2563eb;
            margin-right: 0.5rem;
        }
        .warning {
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 1rem 1.4rem;
            border-radius: 0.6rem;
            margin: 1.2rem 0;
            font-size: 0.95rem;
        }
        .warning i {
            color: #f59e0b;
            margin-right: 0.5rem;
        }

        .equation {
            background: #f8fafc;
            border-radius: 0.8rem;
            padding: 1rem 1.5rem;
            margin: 1.2rem 0;
            text-align: center;
            font-size: 1.15rem;
            font-weight: 500;
            border: 1px solid #e2e8f0;
            font-family: 'Times New Roman', serif;
            font-style: italic;
        }
        .equation .label {
            font-family: 'Inter', sans-serif;
            font-style: normal;
            font-weight: 600;
            font-size: 0.85rem;
            color: #64748b;
            display: block;
            margin-bottom: 0.3rem;
        }

        .mermaid-container {
            background: #f8fafc;
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
            margin: 1.5rem 0;
            overflow-x: auto;
        }
        .mermaid-container svg {
            max-width: 100%;
            height: auto;
        }

        /* ---------- Footer / Credit ---------- */
        .credit {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #e9edf4;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            font-size: 0.95rem;
        }
        .credit .profile {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        .credit .profile img {
            border-radius: 50%;
            width: 48px;
            height: 48px;
            object-fit: cover;
            border: 2px solid #dbeafe;
        }
        .credit .profile .name {
            font-weight: 600;
        }
        .credit .profile .title {
            font-size: 0.85rem;
            color: #475569;
        }

        /* ---------- Responsive tweaks ---------- */
        @media (max-width: 600px) {
            h1 {
                font-size: 2rem;
            }
            h2 {
                font-size: 1.4rem;
            }
            .card-grid {
                grid-template-columns: 1fr;
            }
            .file-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        /* smooth scroll */
        html {
            scroll-behavior: smooth;
        }
        .toc {
            background: #f8fafc;
            border-radius: 1rem;
            padding: 1.2rem 1.8rem;
            margin: 1.5rem 0 2rem;
            border: 1px solid #e2e8f0;
        }
        .toc ul {
            columns: 2 200px;
            list-style: none;
            padding: 0;
            margin: 0.5rem 0 0;
        }
        .toc li {
            margin: 0.2rem 0;
        }
        .toc a {
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .toc a i {
            color: #64748b;
            font-size: 0.7rem;
        }
        @media (max-width: 500px) {
            .toc ul {
                columns: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">

        <!-- ============================================
        HEADER
        ============================================ -->
        <header>
            <h1>
                fvspectrum
                <span class="sub">Lüscher analysis pipeline for πΣ scattering &amp; ERE determination</span>
            </h1>
            <div class="badge-row">
                <span class="badge primary"><i class="fas fa-code-branch"></i> qc2 / intern work</span>
                <span class="badge green"><i class="fas fa-check-circle"></i> active</span>
                <span class="badge"><i class="fas fa-file-pdf"></i> arXiv:2307.13471</span>
                <span class="badge"><i class="fas fa-cube"></i> L = 64</span>
                <span class="badge"><i class="fas fa-chart-line"></i> correlated χ²</span>
            </div>
            <p style="font-size:1.05rem; color:#334155; max-width:800px;">
                A production‑ready Python implementation of the Lüscher finite‑volume formalism
                for extracting scattering parameters (<em>a</em>, <em>b</em>) from lattice QCD energy levels.
                Built for the πΣ channel following Morningstar <em>et al.</em> and the ERE parametrisation
                of arXiv:2307.13471.
            </p>
        </header>

        <!-- ============================================
        TABLE OF CONTENTS
        ============================================ -->
        <div class="toc">
            <strong style="font-size:1.05rem;"><i class="fas fa-list-ul"></i> Contents</strong>
            <ul>
                <li><a href="#overview"><i class="fas fa-chevron-right"></i> Overview</a></li>
                <li><a href="#physics"><i class="fas fa-atom"></i> Physics summary</a></li>
                <li><a href="#repo-structure"><i class="fas fa-folder-open"></i> Repository structure</a></li>
                <li><a href="#installation"><i class="fas fa-cogs"></i> Installation &amp; requirements</a></li>
                <li><a href="#usage"><i class="fas fa-play"></i> Running the pipeline</a></li>
                <li><a href="#files"><i class="fas fa-file-code"></i> File inventory</a></li>
                <li><a href="#equations"><i class="fas fa-square-root-variable"></i> Key equations</a></li>
                <li><a href="#flow"><i class="fas fa-project-diagram"></i> Data flow</a></li>
                <li><a href="#audits"><i class="fas fa-clipboard-list"></i> Audits &amp; reference</a></li>
                <li><a href="#credit"><i class="fas fa-user-graduate"></i> Credit</a></li>
            </ul>
        </div>

        <!-- ============================================
        OVERVIEW
        ============================================ -->
        <section id="overview">
            <h2><i class="fas fa-globe"></i> Overview</h2>
            <p>
                This codebase implements a <strong>Lüscher analysis pipeline</strong> for determining
                Effective Range Expansion (ERE) parameters from lattice QCD energy levels. It follows
                the single‑channel πΣ scattering methodology described in
                <a href="https://arxiv.org/abs/2307.13471" target="_blank">arXiv:2307.13471</a>.
            </p>
            <p><strong>Pipeline steps:</strong></p>
            <ul style="margin-left:1.6rem; margin-bottom:1.2rem;">
                <li>Load energy levels from an HDF5 dataset</li>
                <li>Construct the quantization condition using the Morningstar B‑matrix</li>
                <li>Fit the ERE parameters (<em>a</em>, <em>b</em>) by minimising correlated χ²</li>
                <li>Generate publication‑quality spectrum figures (Figure 8)</li>
            </ul>
            <div class="note">
                <i class="fas fa-info-circle"></i>
                <strong>Repository context:</strong> This repository is part of the broader
                <code>fvspectrum</code> project. The general configuration, test harness,
                <code>run.py</code>, and <code>pycalq.py</code> were authored by
                <strong>Joseph Moscoso</strong> and his team at UMD. My contribution (as an intern)
                consists of the <strong><code>qc2/</code></strong> folder — the core fitting driver,
                physics modules, and analysis scripts documented here.
            </div>
        </section>

        <!-- ============================================
        PHYSICS SUMMARY
        ============================================ -->
        <section id="physics">
            <h2><i class="fas fa-atom"></i> Physics summary</h2>

            <h3>Effective Range Expansion (ERE)</h3>
            <div class="equation">
                <span class="label">Eq. 12 (arXiv:2307.13471)</span>
                <span style="font-size:1.3rem;">
                    <span style="font-style:italic;">k</span> / <span style="font-style:italic;">m</span><sub>π</sub> · cot <span style="font-style:italic;">δ</span>
                    &nbsp;=&nbsp;
                    <span style="font-style:italic;">E</span> / <span style="font-style:italic;">m</span><sub>π</sub> · ( <span style="font-style:italic;">a</span> + <span style="font-style:italic;">b</span> Δ )
                </span>
            </div>
            <p>
                where Δ = (<em>E</em>² − <em>E</em><sub>th</sub>²) / <em>E</em><sub>th</sub>².
                The left‑hand side is the inverse K‑matrix; <em>a</em> is the scattering length,
                <em>b</em> the effective‑range parameter. Both are dimensionless in units of
                <em>m</em><sub>π</sub> = 1.
            </p>

            <h3>Quantization condition</h3>
            <div class="equation">
                <span class="label">Lüscher condition</span>
                <span style="font-size:1.2rem;">
                    Ω(<em>E</em>) &nbsp;=&nbsp; <em>K</em><sup>−1</sup>(<em>E</em>) − <em>B</em>(<em>E</em>) &nbsp;=&nbsp; 0
                </span>
            </div>
            <p>
                <em>B</em>(<em>E</em>) is the Morningstar B‑matrix, constructed from the finite‑volume
                zeta function <em>Z</em><sub>00</sub> and irrep‑specific coefficients.
                The roots of Ω(<em>E</em>) give the predicted finite‑volume energy levels.
            </p>

            <h3>Correlated χ² fit</h3>
            <div class="equation">
                <span class="label">Objective function</span>
                <span style="font-size:1.2rem;">
                    χ² &nbsp;=&nbsp; ( <strong>E</strong><sub>obs</sub> − <strong>E</strong><sub>pred</sub> )<sup>T</sup>
                    <strong>C</strong><sup>−1</sup> ( <strong>E</strong><sub>obs</sub> − <strong>E</strong><sub>pred</sub> )
                </span>
            </div>
            <p>
                <strong>C</strong> is the bootstrap covariance matrix of the energy levels.
                The fit uses Nelder‑Mead optimisation with parallel root finding.
            </p>
        </section>

        <!-- ============================================
        REPO STRUCTURE
        ============================================ -->
        <section id="repo-structure">
            <h2><i class="fas fa-folder-open"></i> Repository structure</h2>
            <pre style="font-size:0.8rem; line-height:1.7;">
                fvspectrum/
                ├── run.py                 # general entry point (J. Moscoso)
                ├── pycalq.py              # calibration / test harness (J. Moscoso)
                ├── test/                  # test configuration (J. Moscoso)
                │   └── ...
                ├── qc2/                   # ★ MY INTERN CONTRIBUTION ★
                │   ├── ere.py                     # ERE parameterisation
                │   ├── fitting_driver_canonical.py # main fitter + PhysicsModule
                │   ├── morningstar_bmatrix.py     # B‑matrix with caching
                │   ├── root_finder.py             # adaptive root bracketing
                │   ├── stats.py                   # correlated χ², covariance, AIC/BIC
                │   ├── dataset_loader.py          # HDF5 loader + DataSet container
                │   ├── pipeline_adapter.py        # PSQ→D mapping, irrep labels
                │   ├── profiler.py                # timing &amp; call counters
                │   ├── run_fit_from_dataset.py    # main execution script
                │   ├── plot_figure8.py            # spectrum plot (Figure 8)
                │   ├── plot_spectrum.py           # wrapper for spectrum plotting
                │   ├── fit_plots.py               # diagnostic plots (B‑matrix, phase shifts)
                │   ├── plot.py                    # Morningstar/BaSc Fig. 10 reproduction
                │   ├── fit_results.json           # output: best‑fit params, χ², pulls
                │   ├── figure8_data_points.csv    # data points for Figure 8
                │   └── figure8_final.pdf          # generated spectrum figure
                └── README.md                # this file (HTML)
            </pre>
            <p>
                <i class="fas fa-arrow-right" style="color:#2563eb;"></i>
                The <code>qc2/</code> folder contains <strong>all physics‑relevant code</strong>
                for the Lüscher analysis. Files outside <code>qc2/</code> are part of the
                general <code>fvspectrum</code> framework and are maintained by the UMD team.
            </p>
        </section>

        <!-- ============================================
        INSTALLATION
        ============================================ -->
        <section id="installation">
            <h2><i class="fas fa-cogs"></i> Installation &amp; requirements</h2>

            <h3>Python dependencies</h3>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr><th>Package</th><th>Version</th><th>Purpose</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><code>numpy</code></td><td>≥ 1.24</td><td>Numerical arrays, linear algebra</td></tr>
                        <tr><td><code>scipy</code></td><td>≥ 1.10</td><td>Optimisation, Brent, linear solvers</td></tr>
                        <tr><td><code>matplotlib</code></td><td>≥ 3.7</td><td>Plotting (Figure 8, diagnostics)</td></tr>
                        <tr><td><code>h5py</code></td><td>≥ 3.8</td><td>HDF5 data loading</td></tr>
                        <tr><td><code>multiprocessing</code></td><td>stdlib</td><td>Parallel energy prediction</td></tr>
                    </tbody>
                </table>
            </div>

            <h3>External modules (not in this repo)</h3>
            <p>
                The pipeline imports several helper modules that are part of the larger
                <code>fvspectrum</code> ecosystem:
            </p>
            <ul style="margin-left:1.6rem;">
                <li><code>tools.kinematics</code> — kinematic variables (q², γ, α, u)</li>
                <li><code>tools.final_zeta</code> — finite‑volume zeta function <em>Z</em><sub>00</sub></li>
                <li><code>b_tables</code> — Morningstar B‑matrix coefficients (TABLE_B1–B8)</li>
                <li><code>general.data_reader</code> — HDF5 reader base class</li>
                <li><code>general.plotting_handler</code> — plotting utilities</li>
            </ul>
            <div class="note">
                <i class="fas fa-check-circle" style="color:#16a34a;"></i>
                These modules are provided by the UMD team and are expected to be in your
                <code>PYTHONPATH</code>. The <code>qc2/</code> code is designed to work with
                the existing framework.
            </div>

            <h3>Quick install</h3>
            <pre><code>pip install numpy scipy matplotlib h5py</code></pre>
            <p>
                Then ensure the <code>fvspectrum</code> root directory is in your
                <code>PYTHONPATH</code>, or run scripts from within the repo.
            </p>
        </section>

        <!-- ============================================
        USAGE
        ============================================ -->
        <section id="usage">
            <h2><i class="fas fa-play"></i> Running the pipeline</h2>

            <h3>1. Prepare your HDF5 dataset</h3>
            <p>
                The expected HDF5 structure is:
            </p>
            <pre><code>DataSet.hdf5/
    └── isoXYZ/              # channel layer (optional)
        └── PSQ0/
            └── G1u/
                ├── ecm_0_ref  [mean, boot1, boot2, …]
                └── ecm_1_ref  [mean, boot1, boot2, …]
        └── PSQ1/
            └── G1/
                └── ecm_1_ref  […]
        …</code></pre>

            <h3>2. Configure the fit</h3>
            <p>
                Edit <code>qc2/run_fit_from_dataset.py</code>:
            </p>
            <pre><code>HDF5_PATH = "~/path/to/DataSet.hdf5"
L = 64.0
MREF = 0.06533
M1_PHYS = 0.06533   # pion mass in lattice units
M2_PHYS = 0.3830    # sigma mass
SELECTED_INDICES = [11, 35, 67, 121]   # levels to include
INITIAL_GUESS = np.array([0.047, 0.65])  # [a, b]
BOUNDS = [(-10.0, 10.0), (-10.0, 10.0)]</code></pre>

            <h3>3. Run the fit</h3>
            <pre><code>cd qc2
python run_fit_from_dataset.py</code></pre>
            <p>
                This will:
            </p>
            <ul style="margin-left:1.6rem;">
                <li>Load the selected energy levels and bootstrap samples</li>
                <li>Optimise <em>a</em> and <em>b</em> using correlated χ²</li>
                <li>Print a summary to the console</li>
                <li>Save <code>fit_results.json</code> with parameters, errors, pulls, and predictions</li>
                <li>Display a profiling report (call counts, timings)</li>
            </ul>
            <h3>4. Generate the spectrum plot (Figure 8)</h3>
            <pre><code>python plot_figure8.py</code></pre>
            <p>
                This produces <code>figure8_final.pdf</code> showing the finite‑volume spectrum
                with non‑interacting bands and thresholds.
            </p>
        </section>
        <!-- ============================================
        FILE INVENTORY
        ============================================ -->
        <section id="files">
            <h2><i class="fas fa-file-code"></i> File inventory</h2>
            <p>
                The table below lists every source file in <code>qc2/</code> with its role and status.
            </p>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr><th>File</th><th>Category</th><th>Description</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><code>ere.py</code></td><td>Core Physics</td><td>ERE parameterisation: <em>K</em><sup>−1</sup>, cot δ, phase shifts</td></tr>
                        <tr><td><code>fitting_driver_canonical.py</code></td><td>Core Physics</td><td><code>PhysicsModule</code> + <code>LuscherFitter</code>; χ² minimisation</td></tr>
                        <tr><td><code>morningstar_bmatrix.py</code></td><td>Core Physics</td><td>Single‑channel B‑matrix with caching &amp; zeta fallback</td></tr>
                        <tr><td><code>root_finder.py</code></td><td>Core Physics</td><td>Adaptive bracketing + Brent + ordered root selection</td></tr>
                        <tr><td><code>stats.py</code></td><td>Utilities</td><td>Bootstrap covariance, χ², AIC/BIC, pulls, parameter covariance</td></tr>
                        <tr><td><code>profiler.py</code></td><td>Utilities</td><td>Timing decorators and counters</td></tr>
                        <tr><td><code>dataset_loader.py</code></td><td>Utilities</td><td>HDF5 loader, <code>DataSet</code> container</td></tr>
                        <tr><td><code>pipeline_adapter.py</code></td><td>Utilities</td><td><code>PSQ_TO_D</code> mapping, irrep label formatting</td></tr>
                        <tr><td><code>run_fit_from_dataset.py</code></td><td>Main script</td><td>Orchestrates loading, fitting, saving</td></tr>
                        <tr><td><code>plot_figure8.py</code></td><td>Visualization</td><td>Generates Figure 8: spectrum + non‑interacting bands</td></tr>
                        <tr><td><code>plot_spectrum.py</code></td><td>Visualization</td><td>Wrapper for spectrum plotting (used by external scripts)</td></tr>
                        <tr><td><code>fit_plots.py</code></td><td>Visualization</td><td>Diagnostic plots: B‑matrix, phase shifts, eigenvector decomposition</td></tr>
                        <tr><td><code>plot.py</code></td><td>Visualization</td><td>Reproduces Morningstar/BaSc Fig. 10</td></tr>
                        <tr><td><code>fit_results.json</code></td><td>Output</td><td>Best‑fit parameters, χ², errors, pulls, predictions</td></tr>
                        <tr><td><code>figure8_data_points.csv</code></td><td>Output</td><td>Data points for Figure 8</td></tr>
                        <tr><td><code>figure8_final.pdf</code></td><td>Output</td><td>Generated spectrum figure</td></tr>
                    </tbody>
                </table>
            </div>
        </section>
        <!-- ============================================
        KEY EQUATIONS
        ============================================ -->
        <section id="equations">
            <h2><i class="fas fa-square-root-variable"></i> Key equations</h2>
            <p>
                A selection of the most important equations implemented in the pipeline.
                For a complete list, see the <a href="#audits">audits</a> below.
            </p>
            <div class="equation">
                <span class="label">ERE parameterisation</span>
                <em>K</em><sup>−1</sup> = <em>E</em> ( <em>a</em> + <em>b</em> Δ )
            </div>
            <div class="equation">
                <span class="label">Energy deviation</span>
                Δ = ( <em>E</em>² − <em>E</em><sub>th</sub>² ) / <em>E</em><sub>th</sub>²
            </div>
            <div class="equation">
                <span class="label">B‑matrix</span>
                <em>B</em> = <em>C</em><sub>irrep</sub> · <em>Z</em><sub>00</sub> / ( <em>γ</em> π<sup>3/2</sup> )
            </div>
            <div class="equation">
                <span class="label">Quantization condition</span>
                Ω(<em>E</em>) = <em>K</em><sup>−1</sup>(<em>E</em>) − <em>B</em>(<em>E</em>) = 0
            </div>
            <div class="equation">
                <span class="label">Correlated χ²</span>
                χ² = ( <strong>E</strong><sub>obs</sub> − <strong>E</strong><sub>pred</sub> )<sup>T</sup> <strong>C</strong><sup>−1</sup> ( <strong>E</strong><sub>obs</sub> − <strong>E</strong><sub>pred</sub> )
            </div>
            <div class="equation">
                <span class="label">Parameter covariance</span>
                <strong>C</strong><sub>par</sub> = ( <strong>J</strong><sup>T</sup> <strong>C</strong><sup>−1</sup> <strong>J</strong> )<sup>−1</sup>
            </div>
        </section>
        <!-- ===========================================
        DATA FLOW
        ============================================ -->
        <section id="flow">
            <h2><i class="fas fa-project-diagram"></i> Data flow &amp; execution trace</h2>
            <p>
                The diagram below shows the complete execution path from the main script
                through data loading, root finding, and optimisation.
            </p>
            <div class="mermaid-container">
                <!-- Mermaid flowchart injected via CDN -->
                <pre class="mermaid" style="background:transparent;padding:0;margin:0;border:none;">
                    flowchart TD
                    A[run_fit_from_dataset.py] --> B[DataLoader.load_data]
                    B --> C[DataLoader.scan_levels]
                    C --> D[DataLoader.build_dataset]
                    D --> E[DataSet: means, bootstrap, covariance]
                    E --> F[Instantiate PhysicsModule &amp; LuscherFitter]
                    F --> G[fitter.fit(initial_guess)]
                    G --> H{Optimizer Loop<br>scipy.optimize.minimize}
                    H --> I[objective(params)]
                    I --> J[predict_energies(params)]
                    J --> K[Parallel: _predict_single_level for each data point]
                    K --> L[Build omega(E) = K⁻¹(E) - B(E)]
                    L --> M[RootFinder.find_root_near_guess]
                    M --> N[Evaluate omega at many E]
                    N --> O[PhysicsModule.compute_kinematics]
                    O --> P[Kinematic equations:<br>q_cm², γ, α, u]
                    P --> Q[PhysicsModule.compute_bmatrix]
                    Q --> R[SingleChannelBMatrix.compute]
                    R --> S[B = C_irrep * Z00/(γ π^1.5)]
                    S --> T[ERE.compute_kinv]
                    T --> U[K⁻¹ = E_cm*(a + b*Δ)<br>Δ=(E_cm² - Eth²)/Eth²]
                    U --> V[Omega = K⁻¹ - B]
                    V --> W[Root found: E_pred_i]
                    W --> X[Collect all E_pred]
                    X --> Y[stats.chi2]
                    Y --> Z[χ² = (E_obs - E_pred)^T C⁻¹ (E_obs - E_pred)]
                    Z --> AA[Return χ² to optimizer]
                    AA --> H
                    H --> AB[Converged? No -> continue; Yes -> exit loop]
                    AB --> AC[Get best_params, best_chi2]
                    AC --> AD[Compute predicted, residuals, pulls, AIC, BIC]
                    AD --> AE[Compute parameter covariance via vij]
                    AE --> AF[FitResult]
                    AF --> AG[save_results('fit_results.json')]
                    AG --> AH[Console output + JSON file]
                </pre>
            </div>
            <p style="font-size:0.9rem; color:#475569;">
                <i class="fas fa-arrow-right" style="color:#2563eb;"></i>
                The trace follows the <code>run_fit_from_dataset.py</code> entry point.
                Each step is annotated with the corresponding function calls.
            </p>
        </section>
        <!-- ============================================
        AUDITS
        ============================================ -->
        <section id="audits">
            <h2><i class="fas fa-clipboard-list"></i> Audits &amp; reference documents</h2>
            <p>
                The following comprehensive audits are included in this repository to provide
                complete documentation of the codebase, physics, units, constants, and API.
            </p>
            <div class="card-grid">
                <div class="card">
                    <div class="title"><i class="fas fa-sitemap"></i> PROJECT_ARCHITECTURE</div>
                    <div class="desc">Detailed file‑by‑file documentation, dependency graph, data flow diagram, and algorithm descriptions.</div>
                </div>
                <div class="card">
                    <div class="title"><i class="fas fa-book-open"></i> PHYSICS_REFERENCE</div>
                    <div class="desc">All equations with variable definitions, units, source paper references, and implementation locations.</div>
                </div>
                <div class="card">
                    <div class="title"><i class="fas fa-ruler"></i> UNITS_AND_CONVENTIONS</div>
                    <div class="desc">Dimensionless system (<em>m</em><sub>π</sub> = 1, <em>a</em> = 1) and variable unit table.</div>
                </div>
                <div class="card">
                    <div class="title"><i class="fas fa-weight-scale"></i> CONSTANTS</div>
                    <div class="desc">Numerical constants: masses, fitted parameters, tolerances, B‑matrix coefficients.</div>
                </div>
                <div class="card">
                    <div class="title"><i class="fas fa-list"></i> CODE_INVENTORY</div>
                    <div class="desc">Classification of every source file by category and status (active / experimental / external).</div>
                </div>
                <div class="card">
                    <div class="title"><i class="fas fa-code"></i> API_REFERENCE</div>
                    <div class="desc">Complete API reference for all public classes, methods, signatures, exceptions, and examples.</div>
                </div>
                <div class="card">
                    <div class="title"><i class="fas fa-route"></i> COMPLETE FIT TRACE</div>
                    <div class="desc">Step‑by‑step execution trace from <code>run_fit_from_dataset.py</code> through the entire pipeline.</div>
                </div>
            </div>
            <p>
                These documents are maintained in the repository root and are updated with
                each major release. They serve as both developer reference and scientific
                documentation for the methodology.
            </p>
        </section>
        <!-- ============================================
        CREDIT
        ============================================ -->
        <section id="credit">
            <h2><i class="fas fa-user-graduate"></i> Credit &amp; acknowledgments</h2>
            <div class="credit">
                <div class="profile">
                    <!-- placeholder avatar; you can replace with actual image -->
                    <div style="width:48px;height:48px;border-radius:50%;background:#dbeafe;display:flex;align-items:center;justify-content:center;font-weight:700;color:#1e40af;font-size:1.2rem;">
                        JM
                    </div>
                    <div>
                        <div class="name">Joseph Moscoso</div>
                        <div class="title">Supervisor · University of Maryland</div>
                        <div style="font-size:0.85rem; color:#475569;">
                            <i class="fas fa-code"></i> General framework, <code>run.py</code>, <code>pycalq.py</code>, test harness
                        </div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:500;">Intern contribution</div>
                    <div style="font-size:0.9rem; color:#475569;">
                        <i class="fas fa-folder-open"></i> <code>qc2/</code> folder · core physics modules · fitting driver · analysis scripts
                    </div>
                    <div style="font-size:0.85rem; color:#64748b; margin-top:0.2rem;">
                        <i class="fas fa-calendar-alt"></i> Summer 2026
                    </div>
                </div>
            </div>
            <div style="margin-top:1.5rem; padding:1.2rem 1.8rem; background:#f1f4f9; border-radius:1rem; border:1px solid #e2e8f0;">
                <p style="margin:0;">
                    <i class="fas fa-heart" style="color:#dc2626;"></i>
                    <strong>Thank you</strong> to Joseph Moscoso and the UMD lattice QCD group
                    for the opportunity to contribute to this project. The general
                    <code>fvspectrum</code> infrastructure, test configuration, and calibration
                    tools provided the foundation for this work. All physics‑specific modules
                    in <code>qc2/</code> were developed during my internship and are released
                    as part of the ongoing collaboration.
                </p>
            </div>
            <div style="margin-top:1.5rem; font-size:0.9rem; color:#64748b; display:flex; flex-wrap:wrap; gap:0.5rem 1.5rem;">
                <span><i class="far fa-file-alt"></i> arXiv:2307.13471</span>
                <span><i class="fas fa-university"></i> UMD Lattice QCD Group</span>
                <span><i class="fas fa-tag"></i> v1.0 · 2026</span>
                <span><i class="fab fa-github"></i> <a href="#" style="color:#64748b;">github.com/umd-lqcd/fvspectrum</a></span>
            </div>
        </section>
        <!-- ============================================
        FOOTER
        ============================================ -->
        <hr />
        <footer style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; font-size:0.85rem; color:#64748b; gap:1rem;">
            <span>
                <i class="fas fa-code"></i> Built with Python · SciPy · NumPy · Matplotlib
            </span>
            <span>
                <i class="far fa-copyright"></i> 2026 · fvspectrum / UMD LQCD
            </span>
            <span>
                <i class="fas fa-arrows-spin"></i> Maintained by the qc2 team
            </span>
        </footer>
    </div>
    <!-- end container -->
    <!-- Mermaid JS for flowcharts -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js">
    </script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            mermaid.initialize({
                theme: 'base',
                themeVariables: {
                    background: '#ffffff',
                    primaryColor: '#2563eb',
                    primaryTextColor: '#0b1e33',
                    primaryBorderColor: '#1e40af',
                    lineColor: '#475569',
                    secondaryColor: '#f1f4f9',
                    tertiaryColor: '#e9edf4',
                    fontFamily: 'Inter, sans-serif',
                },
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: 'basis',
                }
            });
        });
    </script>
</body>
</html>
