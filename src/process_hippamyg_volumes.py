#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import os
import pandas
import string

print(f'Running {__file__}')

parser = argparse.ArgumentParser()
parser.add_argument('--subject_dir')
parser.add_argument('--out_dir')
args = parser.parse_args()

mri_dir = f'{args.subject_dir}/mri'

# Function to sanitize varnames. Alphanumeric or underscore only
def sanitize(input_string):
    validchars = string.ascii_letters + string.digits + '_'
    output_string = ''
    for i in input_string:
        if i in validchars:
            output_string += i.lower()
        else:
            output_string += '_'
    return output_string

# Load freesurfer volumes data
hipp_lh = pandas.read_csv(os.path.join(mri_dir,'lh.hippoSfVolumes.txt'),
    sep=' ',header=None)
hipp_rh = pandas.read_csv(os.path.join(mri_dir,'rh.hippoSfVolumes.txt'),
    sep=' ',header=None)
amyg_lh = pandas.read_csv(os.path.join(mri_dir,'lh.amygNucVolumes.txt'),
    sep=' ',header=None)
amyg_rh = pandas.read_csv(os.path.join(mri_dir,'rh.amygNucVolumes.txt'),
    sep=' ',header=None)

# Append hemisphere to var name
hipp_lh[0] = [f'lh_{x}' for x in hipp_lh[0]]
hipp_rh[0] = [f'rh_{x}' for x in hipp_rh[0]]
amyg_lh[0] = [f'lh_{x}' for x in amyg_lh[0]]
amyg_rh[0] = [f'rh_{x}' for x in amyg_rh[0]]

# Concatenate
hippamyg = pandas.concat([hipp_lh, hipp_rh, amyg_lh, amyg_rh], axis=0)

# Sanitize varnames
hippamyg[0] = [sanitize(x) for x in hippamyg[0]]

# Use known list of desired outputs. Fill any missing (and drop any
# that are unexpected)
rois = [
    'lh_hippocampal_tail',
    'lh_subiculum_body',
    'lh_ca1_body',
    'lh_subiculum_head',
    'lh_hippocampal_fissure',
    'lh_presubiculum_head',
    'lh_ca1_head',
    'lh_presubiculum_body',
    'lh_parasubiculum',
    'lh_molecular_layer_hp_head',
    'lh_molecular_layer_hp_body',
    'lh_gc_ml_dg_head',
    'lh_ca3_body',
    'lh_gc_ml_dg_body',
    'lh_ca4_head',
    'lh_ca4_body',
    'lh_fimbria',
    'lh_ca3_head',
    'lh_hata',
    'lh_whole_hippocampus',
    'lh_whole_hippocampal_body',
    'lh_whole_hippocampal_head',
    'rh_hippocampal_tail',
    'rh_subiculum_body',
    'rh_ca1_body',
    'rh_subiculum_head',
    'rh_hippocampal_fissure',
    'rh_presubiculum_head',
    'rh_ca1_head',
    'rh_presubiculum_body',
    'rh_parasubiculum',
    'rh_molecular_layer_hp_head',
    'rh_molecular_layer_hp_body',
    'rh_gc_ml_dg_head',
    'rh_ca3_body',
    'rh_gc_ml_dg_body',
    'rh_ca4_head',
    'rh_ca4_body',
    'rh_fimbria',
    'rh_ca3_head',
    'rh_hata',
    'rh_whole_hippocampus',
    'rh_whole_hippocampal_body',
    'rh_whole_hippocampal_head',
    'lh_lateral_nucleus',
    'lh_basal_nucleus',
    'lh_accessory_basal_nucleus',
    'lh_anterior_amygdaloid_area_aaa',
    'lh_central_nucleus',
    'lh_medial_nucleus',
    'lh_cortical_nucleus',
    'lh_corticoamygdaloid_transitio',
    'lh_paralaminar_nucleus',
    'lh_whole_amygdala',
    'rh_lateral_nucleus',
    'rh_basal_nucleus',
    'rh_accessory_basal_nucleus',
    'rh_anterior_amygdaloid_area_aaa',
    'rh_central_nucleus',
    'rh_medial_nucleus',
    'rh_cortical_nucleus',
    'rh_corticoamygdaloid_transitio',
    'rh_paralaminar_nucleus',
    'rh_whole_amygdala',
    ]
vals = list()
for roi in rois:
    mask = [x==roi for x in rois]
    if sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    elif sum(mask)==1:
        vals.append(hippamyg[1].loc[hippamyg[0]==roi].array[0])
    else:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)

# Make data frame and write to file
haout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
haout.to_csv(os.path.join(args.out_dir,'HAvol.csv'), 
    header=False, index=False)
