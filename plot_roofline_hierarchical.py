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

    # Performance Roofline TWEAC Compute Current
    # mem_roofs = [('L1', 53745492062956.53/pow(10, 9)), ('L2', 2563824266041.38/pow(10, 9)),
    #              ('HBM', 898420553656.06/pow(10, 9))]

    # Performance Roofline TWEAC Move and Mark
    # mem_roofs = [('L1', 53764596694247.59/pow(10, 9)), ('L2', 2565679718831.03/pow(10, 9)),
    #              ('HBM', 898794568766.48/pow(10, 9))]

    # Performance Roofline LaserWakefield Compute Current
    mem_roofs = [('L1', 53543223771983.02/pow(10, 9)), ('L2', 2534607640994.54/pow(10, 9)),
                 ('HBM', 897397210430.56/pow(10, 9))]

    # Performance Roofline LaserWakefield Move and Mark
    # mem_roofs = [('L1', 53624941608307.18/pow(10, 9)), ('L2', 2545099416980.03/pow(10, 9)),
    #              ('HBM', 897182543898.99/pow(10, 9))]

    # Instruction Roofline TWEAC Compute Current
    # mem_roofs = [('L1', (53745492062956.53/pow(10, 9))/32), ('L2', (2563824266041.38/pow(10, 9))/32),
    #              ('HBM', (898420553656.06/pow(10, 9))/32)]

    # Instruction Roofline TWEAC Move and Mark
    # mem_roofs = [('L1 GTXN/s', (53764596694247.59/pow(10, 9))/32), ('L2 GTXN/s', (2565679718831.03/pow(10, 9))/32),
    #              ('HBM GTXN/s', (898794568766.48/pow(10, 9))/32)]

    # Instruction Roofline LaserWakefield Compute Current
    # mem_roofs = [('L1', (53543223771983.02/pow(10, 9))/32), ('L2', (2534607640994.54/pow(10, 9))/32),
    #              ('HBM', (897397210430.56/pow(10, 9))/32)]

    # Instruction Roofline LaserWakefield Move and Mark
    # mem_roofs = [('L1', (53624941608307.18/pow(10, 9))/32), ('L2', (2545099416980.03/pow(10, 9))/32),
                 # ('HBM', (897182543898.99/pow(10, 9))/32)]

    # Instruction Roofline MI60
    # mem_roofs = [('HBM', 808975476000.00/pow(10, 9))]

    # Instruction Roofline MI100
    # mem_roofs = [('HBM', 933355781000.00/pow(10, 9))]

    # Instruction Roofline MI60 And MI100
    # mem_roofs = [('MI100 HBM', 933355781000.00/pow(10, 9)), ('MI60 HBM', 808975476000.00 / pow(10, 9))]

    # Computational Rooflines in TFLOP/s

    # Performance Roofline TWEAC Compute Current
    # cmp_roofs = [('SP', 13436373015739.15/pow(10, 12))]

    # Performance Roofline TWEAC Single Precision Move and Mark
    # cmp_roofs = [('SP', 13441149173561.90/pow(10, 12))]

    # Performance Roofline TWEAC Double Precision Move and Mark
    # cmp_roofs = [('DP', 6720574586780.95/pow(10, 12))]

    # Performance Roofline TWEAC Both Precisions Move and Mark
    # cmp_roofs = [('SP', 13436373015739.15 / pow(10, 12)), ('DP', 6720574586780.95 / pow(10, 12))]

    # Performance Roofline LaserWakefield Compute Current
    cmp_roofs = [('FP32', 13385805942995.75/pow(10, 12))]

    # Performance Roofline LaserWakefield Move and Mark
    # cmp_roofs = [('SP', 13406235402076.79/pow(10, 12))]

    # Instruction Roofline ALL V100 Simulations
    # cmp_roofs = [('Theoretical Peak', 489600000000/pow(10, 12))]

    # Instruction Roofline ALL MI60 Simulations
    # cmp_roofs = [('Theoretical Peak', 11520000000/pow(10, 12))]

    # Instruction Roofline ALL MI100 Simulations
    # cmp_roofs = [('Theoretical Peak', 180240000000/pow(10, 12))]

    # Instruction Roofline MI60 and MI100 simulations
    # cmp_roofs = [('MI100 Theoretical Peak', 180240000000 / pow(10, 12)),
    #              ('MI60 Theoretical Peak', 115200000000 / pow(10, 12))]

    fig = plt.figure(1, figsize=(10.67, 6.6))
    plt.clf()
    ax = fig.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Performance Roofline
    ax.set_xlabel('Arithmetic Intensity [FLOPs/Byte]')
    ax.set_ylabel('Performance [GFLOP/sec]')

    # NVIDIA Instruction Roofline
    # ax.set_xlabel('Instruction Intensity (warp Instructions per Transaction)')
    # ax.set_ylabel('Performance (warp GIPS)')

    # AMD Instruction Roofline
    # ax.set_xlabel('Instruction Intensity (wavefront Instructions per Byte)')
    # ax.set_ylabel('Performance (wavefront GIPS)')

    # Performance Roofline
    nx = 10000
    xmin = -3
    xmax = 3
    ymin = 1
    ymax = 200000

    # NVIDIA Instruction Roofline
    # nx = 10000
    # xmin = -2
    # xmax = 2
    # ymin = 1
    # ymax = 2000

    # AMD Instruction Roofline
    # nx = 10000
    # xmin = -2
    # xmax = 2
    # ymin = 0.1
    # ymax = 2000

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

    for i in range(len(cmp_roofs)):
        roof = cmp_roofs[i][1] * 1024
        y = np.ones(len(x)) * roof
        ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c='k', ls='-', lw='2')
        # if i == 0:
        #     ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c='k', ls='-', lw='2')
        # else:
        #     ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c='r', ls='-', lw='2')

    for i in range(len(mem_roofs)):
        roof = mem_roofs[i][1]
        y = x * roof
        ax.plot(x[:smem_ix_elbow[i] + 1], y[:smem_ix_elbow[i] + 1], c='k', ls='-', lw='2')
        # if i == 0:
        #     ax.plot(x[:smem_ix_elbow[i] + 1], y[:smem_ix_elbow[i] + 1], c='k', ls='-', lw='2')
        # else:
        #     ax.plot(x[:smem_ix_elbow[i] + 1], y[:smem_ix_elbow[i] + 1], c='r', ls='-', lw='2')

    for i in range(len(hbm_ai)):
        if flag == 'L1':
            ax.plot(float(l1_ai[i]), float(flops[i]), c=colors[i % 10], marker=styles[0], linestyle='None',
                    ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
        elif flag == 'L2':
            ax.plot(float(l2_ai[i]), float(flops[i]), c=colors[i % 10], marker=styles[1],
                    linestyle='None', ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
        elif flag == 'HBM':
            ax.plot(float(hbm_ai[i]), float(flops[i]), c=colors[3], marker=styles[2],
                    linestyle='None', ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
            # MI100 HBM
            # ax.plot(float(0.092024325), float(1.141301142), c=colors[6], marker=styles[8],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

        # elif flag == 'all':
            # Regular L1
            # ax.plot(float(l1_ai[i]), float(flops[i]), c=colors[2], marker=styles[0],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
            # DP L1
            # ax.plot(float(0.39776702157496163), float(221.46128516402553), c=colors[1], marker=styles[0],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

            # Regular L2
            # ax.plot(float(l2_ai[i]), float(flops[i]), c=colors[2], marker=styles[1],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
            # DP L2
            # ax.plot(float(0.6055599996779025), float(221.46128516402553), c=colors[1], marker=styles[1],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

            # Regular HBM
            # ax.plot(float(hbm_ai[i]), float(flops[i]), c=colors[2], marker=styles[2],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

            # DP HBM
            # ax.plot(float(1.1484335077527577), float(221.46128516402553), c=colors[1], marker=styles[2],
            #         linestyle='None', ms=markersize, markerfacecolor='none',
            #         markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

    marker_handles = []

    if flag == 'L1':
        marker_handles.append(ax.plot([], [], c='k', marker=styles[0], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[0][0])[0])
    elif flag == 'L2':
        marker_handles.append(ax.plot([], [], c='k', marker=styles[1], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[1][0])[0])
    elif flag == 'HBM':
        # Comment out for AMD Instrution Rooflines
        marker_handles.append(ax.plot([], [], c='k', marker=styles[2], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[2][0])[0])

        # Uncomment for AMD Instruction Rooflines
        # marker_handles.append(ax.plot([], [], c=colors[3], marker=styles[2], linestyle='None', ms=markersize,
        #                               markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[1][0])[0])
        # marker_handles.append(ax.plot([], [], c=colors[6], marker=styles[8], linestyle='None', ms=markersize,
        #                               markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[0][0])[0])

    elif flag == 'all':
        for i in range(len(mem_roofs)):
            marker_handles.append(ax.plot([], [], c=colors[2], marker=styles[i], linestyle='None', ms=markersize,
                                          markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[i][0])[
                                      0])

    # cmp_roof_count = 0
    for roof in cmp_roofs:
        # if cmp_roof_count == 0: # comment out if statement if not doing AMD rooflines
        ax.text(x[-ixx], roof[1] * 1024,
                roof[0] + ': ' + '{0:.1f}'.format(roof[1]) + ' TFLOP/s',
                # roof[0] + ': ' + '{0:.1f}'.format(roof[1]) + ' warp TIPS',
                # roof[0] + ': ' + str(float(roof[1]) * 1000) + ' wavefront GIPS',
                horizontalalignment='right',
                verticalalignment='bottom')
            # cmp_roof_count += 1 # comment out for NVIDIA rooflines
        # else: # comment out entire else block if not doing AMD rooflines
        #     ax.text(x[-ixx], roof[1] * 1024,
        #             # roof[0] + ': ' + '{0:.1f}'.format(roof[1]) + ' TFLOP/s',
        #             # roof[0] + ': ' + '{0:.1f}'.format(roof[1]) + ' warp TIPS',
        #             roof[0] + ': ' + str(float(roof[1]) * 1000) + ' wavefront GIPS',
        #             horizontalalignment='right',
        #             verticalalignment='bottom', color='r')
    # Comment out for AMD Instruction Rooflines
    for roof in mem_roofs:
        ang = np.arctan(np.log10(xlim[1] / xlim[0]) / np.log10(ylim[1] / ylim[0])
                        * fig.get_size_inches()[1] / fig.get_size_inches()[0])
        if x[ixx] * roof[1] > ymin:
            ax.text(x[ixx], x[ixx] * roof[1] * (1 + 0.25 * np.sin(ang) ** 2),
                    roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GB/s',
                    # roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GTXN/s',
                    horizontalalignment='left',
                    verticalalignment='bottom',
                    rotation=180 / np.pi * ang)
        else:
            ymin_ix_elbow = list()
            ymin_x_elbow = list()
            for ix in range(1, nx):
                if roof[1] * x[ix] >= ymin > roof[1] * x[ix - 1]:
                    ymin_x_elbow.append(x[ix - 1])
                    ymin_ix_elbow.append(ix - 1)
                    break
            ax.text(x[ixx + ymin_ix_elbow[0]], x[ixx + ymin_ix_elbow[0]] * roof[1] * (1 + 0.25 * np.sin(ang) ** 2),
                    roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GB/s',
                    # roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GTXN/s',
                    horizontalalignment='left',
                    verticalalignment='bottom',
                    rotation=180 / np.pi * ang)

    leg1 = plt.legend(handles=marker_handles, loc='lower right', ncol=len(flag[0]) if 'all' not in flag else 3,
                      bbox_to_anchor=(1, 0))
    ax.add_artist(leg1)

    patch_handles = list()
    for i in range(0, len(hbm_ai)):
        if flops[i] > 0:
            patch_handles.append(mpatches.Patch(color=colors[i % 10], label=labels[i] if labels else "unknown"))

    ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'NVIDIA V100 Roofline Model', horizontalalignment='left',
            verticalalignment='top')

    # plt.savefig('_'.join([filename, flag]) + '.png')
    plt.savefig('generic_v100_roofline.png')
    # plt.savefig('_'.join([filename,flag])+'.eps')

    plt.show()
