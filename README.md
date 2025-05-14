# FXT-Lite-Pipeline
FXT Lite-Pipeline is a lightweight command-line tool tailored for SVOM Burst Advocates (BAs) to analyze EP-FXT follow-up observations of SVOM-triggered events.

HEASoft: https://heasarc.gsfc.nasa.gov/docs/software/lheasoft/ \
FXT docker: http://epfxt.ihep.ac.cn/analysis 

There are some aspects of the path that are difficult to describe—please refer to the figure below.
![截屏2025-05-14 11 52 11](https://github.com/user-attachments/assets/b67f25fb-4374-4302-adef-ec3ecd40f63a)


Step 1: Generate Region Files
-----------------------------
Download the source detection CSV files from the web interface and save them as:

- src_a.csv
- src_b.csv


Modify the corresponding FXT data folder in get_src_reg.py .
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
