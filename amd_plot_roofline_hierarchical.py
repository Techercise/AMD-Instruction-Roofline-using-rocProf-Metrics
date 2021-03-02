import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

font = {'size': 12}
plt.rc('font', **font)

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
          'tab:olive', 'tab:cyan']
styles = ['o', 's', 'v', '^', 'D', ">", "<", "*", "h", "H", "+", "1", "2", "3", "4", "8", "p", "d", "|", "_", ".", ","]

markersize = 10
markerwidth = 2
maxchar = 25


def roofline(filename, flops, hbm_ai, l2_ai=None, l1_ai=None, labels=None, flag='HBM'):
    if not flops:
        print('FLOPS can not be empty!')
        return
    if max(flops) == 0:
        print('FLOPS are all 0s!')
        return
    if (not hbm_ai) and (not l2_ai) and (not l1_ai):
        print('AIHBM, AIL2 and AIL1 can not all be empty!')
        return
    if (len(flops) != len(hbm_ai)) or (len(flops) != len(l2_ai)) or (len(flops) != len(l1_ai)):
        print('FLOPS needs to have the same length as AI!')
        return
    if (flag != 'HBM') and (flag != 'L2') and (flag != 'L1') and (flag != 'all'):
        print('flag needs to be one of HBM, L2, L1, and all!')
        return
    labels = [x[:maxchar] for x in labels]

    # Memory Rooflines in GB/s
    # If you want to measure more than one GPU, add another entry to the list (like what's shown in line 42)

    # Instruction Roofline MI100
    mem_roofs = [('HBM', 933355781000.00/pow(10, 9))]

    # Instruction Roofline MI60 And MI100
    # mem_roofs = [('MI100 HBM', 933355781000.00/pow(10, 9)), ('MI60 HBM', 808975476000.00 / pow(10, 9))]

    # Computational Rooflines in TFLOP/s
    # If you want to measure more than one GPU, add another entry to the list (like what's shown in line 49)

    # Instruction Roofline ALL MI100 Simulations
    cmp_roofs = [('Theoretical Peak', 180240000000/pow(10, 12))]

    # Instruction Roofline MI60 and MI100 simulations
    # cmp_roofs = [('MI100 Theoretical Peak', 180240000000 / pow(10, 12)),
    #              ('MI60 Theoretical Peak', 115200000000 / pow(10, 12))]

    fig = plt.figure(1, figsize=(10.67, 6.6))
    plt.clf()
    ax = fig.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')

    # AMD Instruction Roofline
    ax.set_xlabel('Instruction Intensity (wavefront Instructions per Byte)')
    ax.set_ylabel('Performance (wavefront GIPS)')

    # AMD Instruction Roofline
    nx = 10000
    xmin = -2
    xmax = 2
    ymin = 0.1
    ymax = 2000

    ax.set_xlim(10 ** xmin, 10 ** xmax)
    ax.set_ylim(ymin, ymax)

    ixx = int(nx * 0.02)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    scomp_x_elbow = []
    scomp_ix_elbow = []
    smem_x_elbow = []
    smem_ix_elbow = []

    x = np.logspace(xmin, xmax, nx)
    for roof in cmp_roofs:
        for ix in range(1, nx):
            a = float(mem_roofs[0][1] * x[ix])
            b = roof[1] * 1024
            c = (mem_roofs[0][1] * x[ix - 1])
            if a >= b > c:
                scomp_x_elbow.append(x[ix - 1])
                scomp_ix_elbow.append(ix - 1)
                break

    for roof in mem_roofs:
        for ix in range(1, nx):
            if roof[1] * x[ix] >= cmp_roofs[0][1] * 1024 > roof[1] * x[ix - 1]:
                smem_x_elbow.append(x[ix - 1])
                smem_ix_elbow.append(ix - 1)
                break

    # The if-else block contained in this for loop makes the second computational roofline appear red
    # The red coloring is used to differentiate the two (or more) rooflines if they appear close together
    for i in range(len(cmp_roofs)):
        roof = cmp_roofs[i][1] * 1024
        y = np.ones(len(x)) * roof
        if i == 0:
            ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c='k', ls='-', lw='2')
        else:
            ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c='r', ls='-', lw='2')

    # The if-else block contained in this for loop makes the second computational roofline appear red
    # The red coloring is used to differentiate the two (or more) rooflines if they appear close together
    for i in range(len(mem_roofs)):
        roof = mem_roofs[i][1]
        y = x * roof
        if i == 0:
            ax.plot(x[:smem_ix_elbow[i] + 1], y[:smem_ix_elbow[i] + 1], c='k', ls='-', lw='2')
        else:
            ax.plot(x[:smem_ix_elbow[i] + 1], y[:smem_ix_elbow[i] + 1], c='r', ls='-', lw='2')

    for i in range(len(hbm_ai)):
        if flag == 'L1':
            ax.plot(float(l1_ai[i]), float(flops[i]), c=colors[i % 10], marker=styles[0], linestyle='None',
                    ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
        elif flag == 'L2':
            ax.plot(float(l2_ai[i]), float(flops[i]), c=colors[i % 10], marker=styles[1],
                    linestyle='None', ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

        # In our case, on the AMD GPUs we were only able to extract metrics from the HBM
        # For adding a second value, for instance when plotting performance on the MI60 and MI100 GPU, uncomment the
        # block of code starting at line 139
        elif flag == 'HBM':
            ax.plot(float(hbm_ai[i]), float(flops[i]), c=colors[3], marker=styles[2],
                    linestyle='None', ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
            # MI100 HBM
            # ax.plot(float(0.092024325), float(1.141301142), c=colors[6], marker=styles[8],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

    marker_handles = []

    if flag == 'L1':
        marker_handles.append(ax.plot([], [], c='k', marker=styles[0], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[0][0])[0])
    elif flag == 'L2':
        marker_handles.append(ax.plot([], [], c='k', marker=styles[1], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[1][0])[0])

    # Uncomment lines 156 and 157 if plotting more than one device's performance
    elif flag == 'HBM':
        marker_handles.append(ax.plot([], [], c=colors[3], marker=styles[2], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[1][0])[0])

        # marker_handles.append(ax.plot([], [], c=colors[6], marker=styles[8], linestyle='None', ms=markersize,
        #                               markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[0][0])[0])

    elif flag == 'all':
        for i in range(len(mem_roofs)):
            marker_handles.append(ax.plot([], [], c=colors[2], marker=styles[i], linestyle='None', ms=markersize,
                                          markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[i][0])[
                                      0])

    cmp_roof_count = 0
    for roof in cmp_roofs:
        if cmp_roof_count == 0:
            ax.text(x[-ixx], roof[1] * 1024,
                    roof[0] + ': ' + str(float(roof[1]) * 1000) + ' wavefront GIPS',
                    horizontalalignment='right',
                    verticalalignment='bottom')
            cmp_roof_count += 1

        # This else statement is used when measuring performance for more than one device
        else:
            ax.text(x[-ixx], roof[1] * 1024,
                    roof[0] + ': ' + str(float(roof[1]) * 1000) + ' wavefront GIPS',
                    horizontalalignment='right',
                    verticalalignment='bottom', color='r')

    # If the memory bandwidth rooflines appear too close together when the plot is generated, the text indicating
    # their respective bandwidths will overlap with the rooflines. For that reason, this loop is commented out

    # for roof in mem_roofs:
    #     ang = np.arctan(np.log10(xlim[1] / xlim[0]) / np.log10(ylim[1] / ylim[0])
    #                     * fig.get_size_inches()[1] / fig.get_size_inches()[0])
    #     if x[ixx] * roof[1] > ymin:
    #         ax.text(x[ixx], x[ixx] * roof[1] * (1 + 0.25 * np.sin(ang) ** 2),
    #                 roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GB/s',
    #                 horizontalalignment='left',
    #                 verticalalignment='bottom',
    #                 rotation=180 / np.pi * ang)
    #     else:
    #         ymin_ix_elbow = list()
    #         ymin_x_elbow = list()
    #         for ix in range(1, nx):
    #             if roof[1] * x[ix] >= ymin > roof[1] * x[ix - 1]:
    #                 ymin_x_elbow.append(x[ix - 1])
    #                 ymin_ix_elbow.append(ix - 1)
    #                 break
    #         ax.text(x[ixx + ymin_ix_elbow[0]], x[ixx + ymin_ix_elbow[0]] * roof[1] * (1 + 0.25 * np.sin(ang) ** 2),
    #                 roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GB/s',
    #                 horizontalalignment='left',
    #                 verticalalignment='bottom',
    #                 rotation=180 / np.pi * ang)

    leg1 = plt.legend(handles=marker_handles, loc='lower right', ncol=len(flag[0]) if 'all' not in flag else 3,
                      bbox_to_anchor=(1, 0))
    ax.add_artist(leg1)

    patch_handles = list()
    for i in range(0, len(hbm_ai)):
        if flops[i] > 0:
            patch_handles.append(mpatches.Patch(color=colors[i % 10], label=labels[i] if labels else "unknown"))

    ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'AMD MI100 Instruction Roofline Model', horizontalalignment='left',
            verticalalignment='top')

    plt.savefig('generic_mi100_roofline.png')

    plt.show()

