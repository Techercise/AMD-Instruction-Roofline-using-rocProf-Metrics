import os
import numpy as np
import pandas as pd
from plot_roofline_hierarchical import roofline

datadir = '/Users/root/projects_folder/current_project_folder'
files = [x for x in os.listdir(datadir) if x.endswith('.csv') and x.startswith('lw_cc_output')]
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

        dfmetric['Time'] = dfmetric['sm__cycles_elapsed.avg'] / \
                           (dfmetric['sm__cycles_elapsed.avg.per_second'] / dfmetric['Count'])

        dfmetric['CC FLOPs'] = 2 * dfmetric['sm__sass_thread_inst_executed_op_dfma_pred_on.sum'] \
                               + dfmetric['sm__sass_thread_inst_executed_op_dmul_pred_on.sum'] \
                               + dfmetric['sm__sass_thread_inst_executed_op_dadd_pred_on.sum'] \
                               + 2 * dfmetric['sm__sass_thread_inst_executed_op_ffma_pred_on.sum'] \
                               + dfmetric['sm__sass_thread_inst_executed_op_fmul_pred_on.sum'] \
                               + dfmetric['sm__sass_thread_inst_executed_op_fadd_pred_on.sum'] \
                               + 2 * dfmetric['sm__sass_thread_inst_executed_op_hfma_pred_on.sum'] \
                               + dfmetric['sm__sass_thread_inst_executed_op_hmul_pred_on.sum'] \
                               + dfmetric['sm__sass_thread_inst_executed_op_hadd_pred_on.sum']

        dfmetric['TC FLOPs'] = 512 * dfmetric['sm__inst_executed_pipe_tensor.sum']
        dfmetric['all FLOPs'] = dfmetric['CC FLOPs'] + dfmetric['TC FLOPs']

        dfmetric['AI HBM'] = dfmetric['all FLOPs'].div(dfmetric['dram__bytes.sum'])
        dfmetric['AI L2'] = dfmetric['all FLOPs'].div(dfmetric['lts__t_bytes.sum'])
        dfmetric['AI L1'] = dfmetric['all FLOPs'].div(dfmetric['l1tex__t_bytes.sum'])

        dfmetric['GFLOP/s'] = dfmetric['all FLOPs'] / dfmetric['Time'] / 1024 / 1024 / 1024
        dfmetric['TC GFLOP/s'] = dfmetric['TC FLOPs'] / dfmetric['Time'] / 1024 / 1024 / 1024
        dfmetric.to_csv('pd_'+tag+'.csv')
        dfs[tag] = dfmetric

tags = dfs.keys()
flags = ['all']  # 'HBM','L2','L1' or 'all'
for tag in tags:
    for flag in flags:
        dfm = dfs[tag]
        LABELS = dfm.index.tolist()
        AIL1 = dfm['AI L1'].tolist()
        AIL2 = dfm['AI L2'].tolist()
        AIHBM = dfm['AI HBM'].tolist()
        FLOPS = dfm['GFLOP/s'].tolist()

        roofline(tag, FLOPS, AIHBM, AIL2, AIL1, LABELS, flag)
