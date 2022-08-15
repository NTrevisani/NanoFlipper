# Skim module

Module to produce skimmed ntuple for charge-flip probability calculations.

### Download and install

    cmsrel CMSSW_12_4_0

    cd CMSSW_12_4_0/src

    cmsenv

    git clone git@github.com:NTrevisani/NanoFlipper.git

To source a recent version of ROOT (needed to use RDataFrame):

    source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.02/x86_64-centos7-gcc48-opt/bin/thisroot.sh

### Interesting files and directories in `ntuple` folder

- `interface/config.h`: contains leptons working points and scale factors, pT thresholds, variables to store in the output files, DY pT corrections, and trigger paths.

- `data/nano_v7/`: files with list of data and MC samples, and lepton SFs are stored here.

- `interface/helper.h`: contains the list of file with leptons SFs.

- `interface/selection.h`: contains the definitions of selections and output variables, in RDataFrame format.

- `flipskim.py`: contains the datasets definitions

- `runFlipSkim.sh`: list of commands to run `flipskim.py` on the interesting samples and eras

### Actual instructions

Submit condor jobs to produce skimmed files:

    cd ntuple

    ./runFlipSkim.sh

Once jobs are done, merge the resulting rootfiles;   # and move them to eos (to avoid using too much space in the work area):

    bash mergeJobs.sh

    # cp -r results/* /eos/user/n/ntrevisa/charge_flip/

When the skimmed rootfiles are merged, we can move to the actual charge-flip probabilities calculations. The interesting file is `analysis/analysis.py`, containing the definitions of the electrons IDs for which we want to get the probabilities:

    cd ../analysis

    python analysis.py

The rootfiles with the results are then available in the `analysis/data` directory.

Finally, we can also run the validation step, after having fixed the eras definitions in `validation/validation.py`:

    cd ../validation

    python validation.py