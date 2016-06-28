# Molecular Investigation of Ageing via Transcriptional Drift

Tong Shu Li ([Su Lab](http://sulab.org)) and Michael Petrascheck ([Lab Website](http://www.scripps.edu/petrascheck/index.html))

---

## Directory Contents

- `data`: Data storage directory. Also contains simple scripts used to clean
    the raw data.
- `src`: Frequently used functions and utilities.
- `analysis`: Jupyter notebooks containing analyses of the data.

## Environment Settings

Program | Version
--- | ---
Operating system | Fedora 23 (64 bit)
GCC | 5.3.1
Git | 2.5.5
Python | 3.4.3
R | 3.3.0 (Supposedly Educational)

## Cloning the Repository

From the command line run: `git clone https://github.com/veleritas/ageing.git`

## Installing Dependencies

### Python Dependencies

1. Create a virtual environment: `pyvenv venv`
2. Start the virtual environment: `source venv/bin/activate`
2. Install dependencies with `pip`: `pip install -r requirements.txt`

### R Dependencies

No R packages other than the default ones were used.

## Running Notebooks

1. Start the virtual environment: `source venv/bin/activate`
2. Start the Jupyter server: `jupyter notebook`
