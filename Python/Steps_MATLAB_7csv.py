#################################################################
# Generates figure ??
# which contains the eigen values of the Matlab model
#   rotating mass model + reserves with time delays (Low-pass filters(
#################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'cmr10'  # 'https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/font_file.html
plt.rc('axes', unicode_minus=False)
# https://stackoverflow.com/questions/29188757/matplotlib-specify-format-of-floats-for-tick-labels

#############
# solves a warning with a previous syntax for using the package
# https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'


#####################################################
# plot eigen value charts and the frequency measurement from a set of csv files
#####################################################
def plot_eigen_fmeas_from_csvs(simcount_total=3,
                               csvfolder="//REDACTED/2022_Journal_Data/Powerfactory/simdata/20220729",
                               offsetfrequency=False,
                               Fn=50.0,
                               plotFmeasBTC=False,
                               plotvpcc=True,
                               timeoffset=0.0,
                               detailplot=True):
    print("#####################")
    print("Function name: ", plot_eigen_fmeas_from_csvs.__name__)

    if detailplot:
        figeigename = csvfolder + '/figeigen.eps'
    else:
        figeigename = csvfolder + '/figeigenGeral.eps'

    if plotFmeasBTC:
        figstepsname = csvfolder + '/figstepsBTC.eps'
    else:
        figstepsname = csvfolder + '/figsteps.eps'

    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 4.5
    figsizey = 5.5
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')
    figsizex = 4
    figsizey = 2
    fig_steps, axs_steps = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step')

    if plotvpcc:
        figsizex = 4.5
        figsizey = 3
        figstepsnamevpcc = csvfolder + '/figstepsfvpcc.eps'
        fig_steps_vpcc, axs_steps_vpcc = plt.subplots(2, 1, sharex=True,
                                                      figsize=(figsizex, figsizey),
                                                      num='StepFVpcc')

    ##########################################################################
    # style of the plots
    ##########################################################################
    cores = []
    legendas = []
    marker = []
    estilos = []
    for simcount in range(0, simcount_total, 1):
        if simcount == 0:
            cores.append('red')
            legendas.append('GTs')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append('gray')
            legendas.append('GTs+BTC+FLX')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append('blue')
            legendas.append('BTC+FLX')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append('gray')
            legendas.append('')
            marker.append('+')
            estilos.append(':')

    grossuras = 0.75
    markersize = 5

    # if plotFmeasBTC:
    #     csvname = csvfolder + '/timedomainBTC.csv'
    # else:
    #     csvname = csvfolder + '/timedomain.csv'

    #

    # if plotvpcc:
    #     csvname = csvfolder + '/timedomain11kV.csv'
    #     figstepsnamevpcc = csvfolder + '/figstepsnamevpcc.eps'
    #     df_td_vpcc = pd.read_csv(csvname)

    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        if simcount < 10:
            csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'
            colname = "fmeas_0" + str(simcount)
            csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'
        else:
            csvname = csvfolder + "/eigenvalues_" + str(simcount) + '.csv'
            colname = "fmeas_" + str(simcount)
            csvtimedomainname = csvfolder + "/timedomain_" + str(simcount) + '.csv'

        df_eigen = pd.read_csv(csvname)
        df_td = pd.read_csv(csvtimedomainname)

        ##########################################################################
        # name replacements, erasing
        ##########################################################################
        df_eigen['names'] = df_eigen['names'].str.replace('FLEXpll', 'FLXfmeas ')
        df_eigen['names'] = df_eigen['names'].str.replace('FLEXctrl', 'FLXctrl')

        df_eigen['names'] = df_eigen['names'].str.replace('BCpll', 'BTCfmeas')
        df_eigen['names'] = df_eigen['names'].str.replace('BCiactref', 'BTCctrl')
        df_eigen['names'] = df_eigen['names'].str.replace('BATLR', 'BTL ')

        df_eigen['names'] = df_eigen['names'].str.replace('FCictrl', 'FCCctrl')
        df_eigen['names'] = df_eigen['names'].str.replace('FCLR', 'FCL ')

        df_eigen['names'] = df_eigen['names'].str.replace('ELictrl', 'ELCctrl')
        df_eigen['names'] = df_eigen['names'].str.replace('ELLR', 'ELL ')

        df_eigen['names'] = df_eigen['names'].str.replace('GT2', 'GT2 ')

        df_eigen['names'] = df_eigen['names'].str.replace('GT2 exc', 'GT2exc ')

        df_eigen['names'] = df_eigen['names'].str.replace('WT1', 'WT')
        df_eigen['names'] = df_eigen['names'].str.replace('WT2', 'WT')
        df_eigen['names'] = df_eigen['names'].str.replace('WT3', 'WT')

        # df_eigen['names'] = df_eigen['names'].str.replace('FCpll','')
        # df_eigen['names'] = df_eigen['names'].str.replace('ELpll','')

        # df_eigen['names'] = df_eigen['names'].str.replace('ESSDC+', '')
        # df_eigen['names'] = df_eigen['names'].str.replace('ESSDC-', '')

        # df_eigen['names'] = df_eigen['names'].str.replace('PLATpll','')
        df_eigen['names'] = df_eigen['names'].str.replace('PLAT', 'SEC')

        df_eigen['names'] = df_eigen['names'].str.replace('pll', 'fmeas')

        df_eigen['names'] = df_eigen['names'].str.replace('govdb', 'gov')

        df_eigen['names'] = df_eigen['names'].str.replace('udcquacctrl', 'ctrl')

        df_eigen['names'] = df_eigen['names'].str.replace('ESSGC', 'ESSGC ')
        df_eigen['names'] = df_eigen['names'].str.replace('ESSGC ctrl', 'ESSGCctrl')

        ##########################################################################
        # plots ei gen values, aux lines, and names
        ##########################################################################
        axs_eigen.plot(df_eigen['real'], df_eigen['imag'],
                       color=cores[simcount],
                       label=legendas[simcount],
                       linestyle='None',
                       linewidth=grossuras,
                       marker=marker[simcount],
                       markersize=markersize)

        if detailplot:
            maxrealred = 8.0
            maximagred = 4.5

            namesrealminred = -6.0
            namesimagminred = 0.0
            namesimagmaxred = 3.0

            eigenxticks = 1.0
            eigenyticks = 0.5

            namesrealminblue = -5.1
            namesrealmaxblue = -0.5
            namesimagminblue = -0.5
            namesimagmaxblue = 4

            mindampforaddnumbers = 0.55

            legendx = 0.52
            legendy = 0.6

            namesvertorientred = 'bottom'
            namesvertorientblue = 'top'

        else:
            # maxrealred = 70
            # maximagred = 25

            maxrealred = 300
            maximagred = 200

            namesrealminred = -10

            namesimagminred = 1.2
            namesimagmaxred = 1.5

            eigenxticks = 10.0
            eigenyticks = 2.0

            # eigenxticks = 100.0
            # eigenyticks = 100.0

            namesrealminblue = -maximagred
            namesrealmaxblue = -0.5
            namesimagminblue = 3.0
            namesimagmaxblue = maximagred

            mindampforaddnumbers = 0.1

            legendx = 0.55
            legendy = 0.85

            namesvertorientred = 'center'
            namesvertorientblue = 'center'

        if simcount == 0:

            if detailplot:
                n_segments = 1
            else:
                n_segments = 200

            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen,  # nzetalines=31,
                                              nzetalines=19,
                                              max_real=maxrealred, max_imag=maximagred,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=mindampforaddnumbers,
                                              n_segments=n_segments)

            # red
            pth.add_root_locus_part_names(eigen_real=df_eigen['real'],
                                          eigen_imag=df_eigen['imag'],
                                          eigen_part_names=df_eigen['names'],
                                          axis=axs_eigen,
                                          zeta_threshold=1,
                                          real_min=namesrealminred,
                                          real_max=0.0,
                                          imag_min=namesimagminred,
                                          imag_max=namesimagmaxred,
                                          vert_orient=namesvertorientred)

        if simcount == simcount_total - 1:  # blue
            pth.add_root_locus_part_names(eigen_real=df_eigen['real'],
                                          eigen_imag=df_eigen['imag'],
                                          eigen_part_names=df_eigen['names'],
                                          axis=axs_eigen,
                                          zeta_threshold=1,
                                          real_min=namesrealminblue,
                                          real_max=namesrealmaxblue,
                                          imag_min=namesimagminblue,
                                          imag_max=namesimagmaxblue,
                                          vert_orient=namesvertorientblue)

        if offsetfrequency:
            df_td[colname] = df_td[colname] - (df_td[colname][0] - Fn)

        axs_steps.plot(df_td['time'] + timeoffset,
                       df_td['fmeasSEC'],
                       linestyle=estilos[simcount],
                       linewidth=grossuras,
                       color=cores[simcount],
                       label=legendas[simcount])

        if plotvpcc:
            axs_steps_vpcc[0].plot(df_td['time'] + timeoffset,
                                   df_td['fmeasSEC'],
                                   linestyle=estilos[simcount],
                                   linewidth=grossuras,
                                   color=cores[simcount],
                                   label=legendas[simcount])
            axs_steps_vpcc[1].plot(df_td['time'] + timeoffset,
                                   df_td['vpcc'],
                                   linestyle=estilos[simcount],
                                   linewidth=grossuras,
                                   color=cores[simcount],
                                   label=legendas[simcount])

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps.set_xlabel(r'Time (s)')
    axs_steps.set_ylabel(r'Frequency (Hz)')

    axs_steps.set_xticks(np.arange(-20, 180, 5))
    axs_steps.set_xlim([0, 30])

    # axs_steps.set_yticks(np.arange(49.90, 50.10, 0.025))
    # axs_steps.set_ylim([49.95, 50.075])

    axs_steps.legend(loc='best', frameon=False)

    if plotvpcc:
        axs_steps_vpcc[0].set_ylabel(r'Frequency (Hz)')

        axs_steps_vpcc[1].set_xlabel(r'Time (s)')
        axs_steps_vpcc[1].set_ylabel(r'Voltage (kV)')

        axs_steps_vpcc[1].set_xticks(np.arange(-20, 180, 1))
        axs_steps_vpcc[1].set_xlim([0, 8])

        axs_steps_vpcc[1].set_yticks(np.arange(10.0, 11.1, 0.01))
        axs_steps_vpcc[1].set_ylim([10.97, 11.0])

        corlegenda = 'whitesmoke'

        axs_steps_vpcc[0].annotate(r'a', xy=(0.0625, 0.2), xycoords='axes fraction',
                                   bbox=dict(boxstyle='circle', fc=corlegenda))

        axs_steps_vpcc[1].annotate(r'b', xy=(0.0625, 0.2), xycoords='axes fraction',
                                   bbox=dict(boxstyle='circle', fc=corlegenda))

        axs_steps_vpcc[1].legend(loc='lower right', frameon=False)

        fig_steps_vpcc.tight_layout()
        fig_steps_vpcc.show()

        fig_steps_vpcc.savefig(figstepsnamevpcc, format='eps')

    if detailplot:
        axs_eigen.set_xticks(np.arange(-maxrealred, 10, eigenxticks))
        axs_eigen.set_xlim([-maxrealred, 0])

        axs_eigen.set_yticks(np.arange(- eigenyticks, maximagred + eigenyticks, eigenyticks))
        axs_eigen.set_ylim([-0.25, maximagred])

        axs_eigen.legend(loc=(legendx, legendy), frameon=True)  # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))

    else:
        axs_eigen.grid(which='major', axis='both', linestyle=':', linewidth=0.5, color='gray')

        axs_eigen.set_xscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=0.75)
        axs_eigen.set_xlim([-maxrealred, 0])
        axs_eigen.set_xticks([-maxrealred, -100, -10, -8, -6, -4, -2, 0])
        axs_eigen.set_xticklabels([-maxrealred, -100, -10, -8, -6, -4, -2, 0])

        axs_eigen.set_yscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=1)
        axs_eigen.set_yticks([0, 2, 4, 8, 6, 8, 10, 100, maximagred])
        axs_eigen.set_yticklabels([0, 2, 4, 8, 6, 8, 10, 100, maximagred])
        axs_eigen.set_ylim([-2.0, maximagred])

        axs_eigen.legend(loc=(legendx, legendy), frameon=True)  # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))

    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    fig_steps.tight_layout()
    fig_steps.show()
    fig_steps.savefig(figstepsname, format='eps')

    fig_eigen.tight_layout()
    fig_eigen.savefig(figeigename, format='eps')

    plt.show()


#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_fmeas_from_csvs()
    # print("Nothing else done")


if __name__ == '__main__':
    main()

