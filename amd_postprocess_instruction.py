import os
import pandas as pd
from amd_plot_roofline_hierarchical import roofline

datadir = '/Users/root/projects_folder/project'
files = [x for x in os.listdir(datadir) if x.endswith('.csv') and x.startswith('mi60_tweac_cc_inst_output')]
files.sort()
files = [os.path.join(datadir, file) for file in files]
dfs = {}
for file in files:
    tag, ext = os.path.splitext(os.path.basename(file))
    dfs[tag] = pd.DataFrame()
    with open(file, 'r') as f:
        cnt = 0
        while True:
            ln = f.readline()
            if not ln:
                break
            cnt += 1
            if 'Host Name' in ln:
                break
        df = pd.read_csv(file, skiprows=cnt - 1)
        dft = df.groupby(['Kernel Name', 'Metric Name']).sum()
        dfmetric = pd.pivot_table(dft, index='Kernel Name', columns='Metric Name', values='Metric Value')
        dfmetric['Count'] = df.groupby(['Kernel Name']).count()['ID'].div(dfmetric.shape[1])

        dfmetric['Time'] = dfmetric['time'] * pow(10, -6)

        dfmetric['Write_Size'] = dfmetric['WriteSize']

        dfmetric['Fetch_Size'] = dfmetric['FetchSize']

        dfmetric['Instructions'] = (dfmetric['SQ_INSTS_VALU'] * 4) + dfmetric['SQ_INSTS_SALU']

        dfmetric['Instruction Intensity HBM'] = \
            (dfmetric['Instructions'] / 64) / ((dfmetric['Fetch_Size'] + dfmetric['Write_Size']) * dfmetric['Time'])
        dfmetric['GIPS'] = (dfmetric['Instructions'] / 64) / (pow(10, 9) * dfmetric['Time'])
        #         dfmetric.to_csv('pd_'+tag+'.csv')
        dfs[tag] = dfmetric

tags = dfs.keys()
flags = ['HBM']  # 'HBM','L2','L1' or 'all'
for tag in tags:
    for flag in flags:
        dfm = dfs[tag]
        LABELS = dfm.index.tolist()
        Instruction_Intensity_HBM = dfm['Instruction Intensity HBM'].tolist()
        GIPS = dfm['GIPS'].tolist()

        roofline(tag, GIPS, Instruction_Intensity_HBM, [0], [0], LABELS, flag)
