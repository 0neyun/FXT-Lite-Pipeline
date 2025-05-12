# Author: Yun Wang <wangyun@pmo.ac.cn>
# Date: 2025-05-12
# Description: Generate DS9 region files for FXT sources with optional background calculation based on provided center coordinates.

import pandas as pd
import math

def main(obs_file, ins, ra=None, dec=None):
    """
    Generate DS9 region files based on provided center coordinates:

    1. If ra and dec are not provided:
       - Create detection_{ins}.reg
       - Include all sources from CSV as circles (radius 1') in white with label FXT.

    2. If ra and dec are provided:
       - Create s1_{ins}.reg: a single include circle (radius 1') in green at the center.
       - Create bak_{ins}.reg:
         - Include annulus around center (inner radius 10', outer radius 20') in green.
         - Exclude all sources from CSV as circles (radius 1') in green.
       - Calculate the ratio of remaining background area to the area of a 1' radius circle and print it.
    """
    # Define file paths
    path = f'./{obs_file}/fxt/products'
    input_csv = f'{path}/src_{ins}.csv'

    # Read CSV and auto-detect RA/Dec columns
    df = pd.read_csv(input_csv)
    possible_ra = [c for c in df.columns if 'ra' in c.lower()]
    possible_dec = [c for c in df.columns if 'dec' in c.lower()]
    if not possible_ra or not possible_dec:
        raise ValueError("RA/Dec columns not found in CSV header.")
    ra_col, dec_col = possible_ra[0], possible_dec[0]

    # Case 1: No center coordinates provided
    if ra is None or dec is None:
        detection_file = f'{path}/detection_{ins}.reg'
        with open(detection_file, 'w') as f:
            f.write('# Region file format: DS9 version 4.1\n')
            f.write('fk5\n')
            for _, row in df.iterrows():
                # Include all sources as white circles labeled FXT
                f.write(f'circle({row[ra_col]},{row[dec_col]},60") # color=white text={{FXT}}\n')
        print(f"Created {detection_file}")
        return

    # Case 2: Center coordinates provided
    # 1) Create s1_{ins}.reg with a single include circle
    s1_file = f'{path}/s1_{ins}.reg'
    with open(s1_file, 'w') as f:
        f.write('# Region file format: DS9 version 4.1\n')
        f.write('fk5\n')
        # Center include circle in green
        f.write(f'circle({ra},{dec},60") # color=green\n')
    print(f"Created {s1_file}")

    # 2) Create bak_{ins}.reg with annulus and excluded sources
    bak_file = f'{path}/bak_{ins}.reg'
    with open(bak_file, 'w') as f:
        f.write('# Region file format: DS9 version 4.1\n')
        f.write('fk5\n')
        # Include annulus in green
        f.write(f'annulus({ra},{dec},600",1200") # color=green\n')
        # Exclude all sources as green circles
        for _, row in df.iterrows():
            f.write(f'-circle({row[ra_col]},{row[dec_col]},60") # color=green\n')

    # Function to compute overlap area between two circles (arcmin)
    def circle_intersection_area(r, R, d):
        if d >= r + R:
            return 0.0
        if d <= abs(R - r):
            return math.pi * min(r, R)**2
        r2, R2, d2 = r*r, R*R, d*d
        alpha = math.acos((d2 + r2 - R2) / (2 * d * r))
        beta  = math.acos((d2 + R2 - r2) / (2 * d * R))
        return (r2 * alpha + R2 * beta
                - 0.5 * math.sqrt(
                    max(0.0, (-d + r + R) * (d + r - R) * (d - r + R) * (d + r + R))
                  ))

    # Parameters (arcmin)
    r_in, r_out, r_src = 10.0, 20.0, 1.0
    annulus_area = math.pi * (r_out**2 - r_in**2)

    # Sum overlap area of excluded sources with annulus
    overlap_sum = 0.0
    for _, row in df.iterrows():
        dra  = (row[ra_col] - ra) * math.cos(math.radians(dec))
        ddec = row[dec_col] - dec
        d    = math.sqrt(dra**2 + ddec**2) * 60.0
        A_out = circle_intersection_area(r_src, r_out, d)
        A_in  = circle_intersection_area(r_src, r_in,  d)
        overlap_sum += max(0.0, A_out - A_in)

    remaining_area = annulus_area - overlap_sum
    src_area = math.pi * (r_src**2)
    ratio = remaining_area / src_area

    print(f"Background annulus remaining area / 1' circle area = {ratio:.2f}")
    
#####################################################################
# input file name
#GRB 250507A
obs_file = 'ep_fxt_06800000583_AB'
main(obs_file=obs_file, ins='a')
main(obs_file=obs_file, ins='a', ra=183.0648000, dec=-23.5882000)
main(obs_file=obs_file, ins='b')
main(obs_file=obs_file, ins='b', ra=183.0646000, dec=-23.5883000)
