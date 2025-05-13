#!/bin/bash

# === path for mkf ===
MKF="../hk/fxt_08500000346_mkf_0ac.fits"

echo "[1] Generating exposure map for s1_a..."
fxtexpogen mkffile=$MKF evtfile=fxt_a_08500000346_ff_01_po_cl_2ac.fits outfile=fxta-expo_a.fits

echo "[2] Generating ARF for s1_a..."
fxtarfgen specfile=s1_a.pha expfile=fxta-expo_a.fits psfcor=1 outfile=fxta.arf

echo "[3] Generating RMF for s1_a..."
fxtrmfgen specfile=s1_a.pha outfile=fxta.rmf

echo "[4] Generating exposure map for s1_b..."
fxtexpogen mkffile=$MKF evtfile=fxt_b_08500000346_ff_01_po_cl_2ac.fits outfile=fxta-expo_b.fits

echo "[5] Generating ARF for s1_b..."
fxtarfgen specfile=s1_b.pha expfile=fxta-expo_b.fits psfcor=1 outfile=fxtb.arf

echo "[6] Generating RMF for s1_b..."
fxtrmfgen specfile=s1_b.pha outfile=fxtb.rmf

echo "Done generating all response files."
