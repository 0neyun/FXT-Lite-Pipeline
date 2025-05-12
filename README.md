# FXT-Lite-Pipeline
FXT Lite-Pipeline is a lightweight command-line tool tailored for SVOM Burst Advocates (BAs) to analyze EP-FXT follow-up observations of SVOM-triggered events.

HEASoft: https://heasarc.gsfc.nasa.gov/docs/software/lheasoft/ \
FXT docker: http://epfxt.ihep.ac.cn/analysis 

Step 1: Generate Region Files
-----------------------------
Download the source detection CSV files from the web interface and save them as:

- src_a.csv
- src_b.csv

Then run the script to generate region files for FXT-A and FXT-B: \
    python get_src_reg.py

Step 2: Extract Source and Background Spectrum
---------------------------------------------
Use xselect to extract source and background spectra: \
    xselect @extract_spec.xco

Step 3: Generate ARF and RMF Using Docker
-----------------------------------------
Run the following command to start the container:
    docker run -it --rm \
        -v /Users/wangyun/fxtdata:/mnt/fxtdata \
        -v /Users/wangyun/fxtcaldb/:/caldb \
        9c037045129c bash

Inside the container: \
    chmod +x group_spectra.sh \
    ./gen_arf_rmf.sh

Step 4: Group the Spectrum
--------------------------
Run the grouping script: \
    ./grppha_spec.sh

Step 5: Load and Fit Spectrum in XSPEC
-------------------------------------
Load the spectra and perform fitting: \
    xspec - fit_a_b.xcm
