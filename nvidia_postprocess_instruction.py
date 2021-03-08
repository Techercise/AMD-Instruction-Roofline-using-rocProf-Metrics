import os
import pandas as pd
from nvidia_plot_roofline_hierarchical import roofline

datadir = '/Users/matthewleinhauser/PycharmProjects/roofline_plots'
files = [x for x in os.listdir(datadir) if x.endswith('.csv') and x.startswith('tweac_cc_inst_output_2021')]
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

        dfmetric['L1 Transactions'] = dfmetric['gld_transactions'] \
                                      + dfmetric['gst_transactions'] \
                                      + dfmetric['local_load_transactions'] \
                                      + dfmetric['local_store_transactions'] \
                                      + dfmetric['shared_load_transactions'] \
                                      + dfmetric['shared_store_transactions']

        dfmetric['L2 Transactions'] = dfmetric['l2_read_transactions'] + dfmetric['l2_write_transactions']

        dfmetric['HBM Transactions'] = dfmetric['dram_read_transactions'] + dfmetric['dram_write_transactions']

        dfmetric['Instruction Intensity HBM'] = (dfmetric['inst_executed']/ 32) / dfmetric['HBM Transactions']
        dfmetric['Instruction Intensity L2'] = (dfmetric['inst_executed']/ 32) / dfmetric['L2 Transactions']
        dfmetric['Instruction Intensity L1'] = (dfmetric['inst_executed']/ 32) / dfmetric['L1 Transactions']
        dfmetric['GIPS'] = (dfmetric['inst_executed'] / 32)/(pow(10, 9) * dfmetric['Time'])
        #         dfmetric.to_csv('pd_'+tag+'.csv')
        dfs[tag] = dfmetric

tags = dfs.keys()
flags = ['all']  # 'HBM','L2','L1' or 'all'
for tag in tags:
    for flag in flags:
        dfm = dfs[tag]
        LABELS = dfm.index.tolist()
        Instruction_Intensity_L1 = dfm['Instruction Intensity L1'].tolist()
        Instruction_Intensity_L2 = dfm['Instruction Intensity L2'].tolist()
        Instruction_Intensity_HBM = dfm['Instruction Intensity HBM'].tolist()
        GIPS = dfm['GIPS'].tolist()

        roofline(tag, GIPS, Instruction_Intensity_HBM, Instruction_Intensity_L2, Instruction_Intensity_L1, LABELS, flag)
