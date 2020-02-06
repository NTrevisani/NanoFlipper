# Flipper
Charge flip probability measurement

## Prerequisite:
  - latest version of ROOT: > 6.18/04 to use RDataframe
  - python 2.6
  
## How to run
### Nutple datasets
For now only two dataset (latino) are considered, DATA and DY, the weights and definition is found in `datasets.py`, run it by

```
python ntupler.py
```

### Harvesting results

Run `flipper.py` to harvest 1D kinematics results (pt,eta,mll) for lepton1,2 in Same Sign and Opposite Sign region ; 1D ratio plot (charge flip probabilities) and 2D ratio plot. It also running chi2fit on 2D ratio plot. The fitting mechanism is in ` chi2fit.py`

```
python flipper.py
```
