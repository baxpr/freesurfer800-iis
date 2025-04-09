#!/usr/bin/env python3
#
# Relabeling of Freesurfer hippocampus subfields following
#
# McHugo M, Talati P, Woodward ND, Armstrong K, Blackford JU, Heckers S. 
# Regionally specific volume deficits along the hippocampal long axis in 
# early and chronic psychosis. Neuroimage Clin. 2018;20:1106-1114. 
# doi: 10.1016/j.nicl.2018.10.021. PMID: 30380517; PMCID: PMC6202690.
#
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6202690/

import argparse
import os
import pandas

print(f'Running {__file__}')

pandas.set_option('display.max_rows', None)

parser = argparse.ArgumentParser()
parser.add_argument('--havol_csv', required=True)
parser.add_argument('--stats_dir', required=True)
args = parser.parse_args()

vols = pandas.read_csv(args.havol_csv)

mmregions = list()
mmvols = list()

for hemi in ['lh', 'rh']:

    mmregions.append(f'{hemi}_anterior_hippocampus')
    mmvols.append(
        vols[f'{hemi}_presubiculum_head'].array[0] +
        vols[f'{hemi}_subiculum_head'].array[0] +
        vols[f'{hemi}_ca1_head'].array[0] +
        vols[f'{hemi}_ca3_head'].array[0] +
        vols[f'{hemi}_ca4_head'].array[0] +
        vols[f'{hemi}_gc_ml_dg_head'].array[0] +
        vols[f'{hemi}_molecular_layer_hp_head'].array[0]
        )

    mmregions.append(f'{hemi}_posterior_hippocampus')
    mmvols.append(
        vols[f'{hemi}_hippocampal_tail'].array[0] +
        vols[f'{hemi}_presubiculum_body'].array[0] +
        vols[f'{hemi}_subiculum_body'].array[0] +
        vols[f'{hemi}_ca1_body'].array[0] +
        vols[f'{hemi}_ca3_body'].array[0] +
        vols[f'{hemi}_ca4_body'].array[0] +
        vols[f'{hemi}_gc_ml_dg_body'].array[0] +
        vols[f'{hemi}_molecular_layer_hp_body'].array[0]
        )
        
    mmregions.append(f'{hemi}_head_ca')
    mmvols.append(
        vols[f'{hemi}_subiculum_head'].array[0] +
        vols[f'{hemi}_ca1_head'].array[0] +
        vols[f'{hemi}_ca3_head'].array[0] +
        vols[f'{hemi}_molecular_layer_hp_head'].array[0]
        )
    
    mmregions.append(f'{hemi}_head_dg')
    mmvols.append(
        vols[f'{hemi}_ca4_head'].array[0] +
        vols[f'{hemi}_gc_ml_dg_head'].array[0]
        )

    mmregions.append(f'{hemi}_head_subiculum')
    mmvols.append(
        vols[f'{hemi}_presubiculum_head'].array[0]
        )

    mmregions.append(f'{hemi}_body_ca')
    mmvols.append(
        vols[f'{hemi}_subiculum_body'].array[0] +
        vols[f'{hemi}_ca1_body'].array[0] +
        vols[f'{hemi}_ca3_body'].array[0] +
        vols[f'{hemi}_molecular_layer_hp_body'].array[0]
        )

    mmregions.append(f'{hemi}_body_dg')
    mmvols.append(
        vols[f'{hemi}_ca4_body'].array[0] +
        vols[f'{hemi}_gc_ml_dg_body'].array[0]
        )

    mmregions.append(f'{hemi}_body_subiculum')
    mmvols.append(
        vols[f'{hemi}_presubiculum_body'].array[0]
        )

    mmregions.append(f'{hemi}_tail')
    mmvols.append(
        vols[f'{hemi}_hippocampal_tail'].array[0]
        )
    
        
mmdata = pandas.DataFrame([mmregions,mmvols])
os.makedirs(args.stats_dir, exist_ok=True)
mmdata.to_csv(os.path.join(args.stats_dir,'MMhippvol.csv'),
    index=False, header=False)
