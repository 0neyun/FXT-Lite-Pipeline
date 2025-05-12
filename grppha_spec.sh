
#!/bin/bash

# set min photon number for per bin 
GROUPING="group min 20"

# ======== s1_a ==========
grppha << EOF
s1_a.pha
s1_a.pi
chkey BACKFILE s1_a_bk.pha
chkey RESPFILE fxta.rmf
chkey ANCRFILE fxta.arf
$GROUPING
exit
EOF

# ======== s1_b ==========
grppha << EOF
s1_b.pha
s1_b.pi
chkey BACKFILE s1_b_bk.pha
chkey RESPFILE fxtb.rmf
chkey ANCRFILE fxtb.arf
$GROUPING
exit
EOF

echo "Finished grppha processing for s1_a and s1_b"
