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
# plot rool locus damping lines
#####################################################
def plot_root_locus_damping_lines_for_matlab(eigen_real, eigen_imag, axis, nzetalines=19,
                                             max_axis='auto', max_real=1000.0, max_imag=1000.0,
                                             color='black', label=None, linestyle='dotted',
                                             linewidth=0.5, marker=None, markersize=None,
                                             add_pos_damping_numbers=False,
                                             min_damp_for_adding_numbers=0.4,
                                             max_damp_for_adding_numbers=1.0,
                                             n_segments=1):
    print('----------------')
    print('Function: ', plot_root_locus_damping_lines_for_matlab.__name__)

    if max_axis == 'auto':
        max_abs_real = 1.1 * np.max(np.abs(eigen_real))
        max_abs_imag = 1.1 * np.max(np.abs(eigen_imag))
    else:
        max_abs_real = np.abs(max_real)
        max_abs_imag = np.abs(max_imag)

    amp_max = 2.0 * np.max([max_abs_real, max_abs_imag])

    angles = np.pi / 180.0 * np.linspace(90.0, 270.0, nzetalines)

    x = np.zeros(nzetalines)  # x = np.zeros(angles.size)
    y = np.zeros(nzetalines)

    x[0] = 0
    y[0] = max_abs_imag
    axis.plot([0, x[0]], [0, y[0]], color=color, label=label, linestyle=linestyle,
              linewidth=linewidth, marker=marker, markersize=markersize)

    x[-1] = 0
    y[-1] = -max_abs_imag
    axis.plot([0, x[-1]], [0, y[-1]], color=color, label=label, linestyle=linestyle,
              linewidth=linewidth, marker=marker, markersize=markersize)

    if n_segments <= 1:
        for i in range(1, nzetalines - 1, 1):
            y[i] = amp_max * np.sin(angles[i])
            if y[i] > max_abs_imag:
                y[i] = max_abs_imag
                x[i] = y[i] / np.tan(angles[i])
                if x[i] < -max_abs_real:
                    x[i] = -max_abs_real
                    y[i] = x[i] * np.tan(angles[i])
            elif y[i] < -max_abs_imag:
                y[i] = -max_abs_imag
                x[i] = y[i] / np.tan(angles[i])
                if x[i] < -max_abs_real:
                    x[i] = -max_abs_real
                    y[i] = x[i] * np.tan(angles[i])
            else:
                x[i] = amp_max * np.cos(angles[i])
                if x[i] < -max_abs_real:
                    x[i] = -max_abs_real
                    y[i] = x[i] * np.tan(angles[i])

            axis.plot([0, x[i]], [0, y[i]], color=color, label=label, linestyle=linestyle,
                      linewidth=linewidth, marker=marker, markersize=markersize)

            if add_pos_damping_numbers and y[i] > 0.00001:
                auxd = - x[i] / (x[i] ** 2 + y[i] ** 2) ** 0.5
                if auxd > min_damp_for_adding_numbers and auxd < max_damp_for_adding_numbers:
                    axis.text(x=x[i], y=y[i],
                              s=r"$\zeta={:.2f}$".format(auxd),
                              ha='left', va='top')

    else:
        amps = np.logspace(-2, np.log10(amp_max), n_segments, endpoint=True, base=10)
        x = np.zeros(len(amps) + 1)
        y = np.zeros(len(amps) + 1)
        for i in range(1, nzetalines - 1, 1):
            for j in range(0, len(amps), 1):
                y[j + 1] = amps[j] * np.sin(angles[i])
                if y[j + 1] > max_abs_imag:
                    y[j + 1] = max_abs_imag
                    x[j + 1] = y[j + 1] / np.tan(angles[i])
                    if x[j + 1] < -max_abs_real:
                        x[j + 1] = -max_abs_real
                        y[j + 1] = x[j + 1] * np.tan(angles[i])
                elif y[j + 1] < -max_abs_imag:
                    y[j + 1] = -max_abs_imag
                    x[j + 1] = y[j + 1] / np.tan(angles[i])
                    if x[j + 1] < -max_abs_real:
                        x[j + 1] = -max_abs_real
                        y[j + 1] = x[j + 1] * np.tan(angles[i])
                else:
                    x[j + 1] = amps[j] * np.cos(angles[i])
                    if x[j + 1] < -max_abs_real:
                        x[j + 1] = -max_abs_real
                        y[j + 1] = x[j + 1] * np.tan(angles[i])

            axis.plot(x, y, color=color, label=label, linestyle=linestyle,
                      linewidth=linewidth, marker=marker, markersize=markersize)

            if add_pos_damping_numbers and y[-1] > 0.00001:
                if i == 5:
                    auxind = n_segments - 20
                elif i == 6:
                    auxind = n_segments - 60
                elif i == 7:
                    auxind = n_segments - 60
                elif i == 8:
                    auxind = n_segments - 60
                else:
                    auxind = -1

                auxd = - x[auxind] / (x[auxind] ** 2 + y[auxind] ** 2) ** 0.5
                if auxd > min_damp_for_adding_numbers and auxd < max_damp_for_adding_numbers:
                    axis.text(x=x[auxind], y=y[auxind],
                              s=r"$\zeta={:.2f}$".format(auxd),
                              ha='left', va='top')


#####################################################
# plot eigen value charts and the frequency measurement from a set of csv files
#####################################################
def plot_eigen_from_7_csvs(simcount_total=7,
                               csvfolder="../MatLab/",
                               offsetfrequency=False,
                               Fn=50.0):
    print("#####################")
    print("Function name: ", plot_eigen_from_7_csvs.__name__)

    figeigename = csvfolder + '/figeigenmatlab.eps'

    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 4.5
    figsizey = 2.75
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')

    xmax = 0.0
    xmin = -5.0

    ymax = 2.0
    ymin = -2.0# -0.25

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
            legendas.append('GTs only')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append('gray')
            legendas.append('GTs+ESS')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append('blue')
            legendas.append('ESS only')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append('gray')
            legendas.append('')
            marker.append('+')
            estilos.append(':')

    grossuras = 0.75
    markersize = 5

    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        csvname = csvfolder + "/mateigen_run_" + str(simcount+1) + '.csv'

        df_eigen = pd.read_csv(csvname, names=['real', 'imag'])  # header=None

        ##########################################################################
        # plots eigen values, aux lines, and names
        ##########################################################################
        axs_eigen.plot(df_eigen['real'], df_eigen['imag'],
                       color=cores[simcount],
                       label=legendas[simcount],
                       linestyle='None',
                       linewidth=grossuras,
                       marker=marker[simcount],
                       markersize=markersize)

        if simcount == 0:
            # pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
            #                                   eigen_imag=df_eigen['imag'],
            #                                   axis=axs_eigen,  # nzetalines=31,
            #                                   nzetalines=19,
            #                                   max_real=np.abs(xmin), max_imag=ymax,
            #                                   add_pos_damping_numbers=True,
            #                                   max_axis='manual',
            #                                   min_damp_for_adding_numbers=0.55)

            plot_root_locus_damping_lines_for_matlab(eigen_real=df_eigen['real'],
                                                     eigen_imag=df_eigen['imag'],
                                                     axis=axs_eigen,
                                                     nzetalines=19,
                                                     max_real=20.0,
                                                     max_imag=2,
                                                     add_pos_damping_numbers=True,
                                                     max_axis='manual',
                                                     min_damp_for_adding_numbers=0.6,
                                                     max_damp_for_adding_numbers=1.0,
                                                     n_segments=200)

    ##########################################################################
    # arrows
    ##########################################################################
    axs_eigen.annotate('',
                       xy=(-1.5, 0.75), xycoords='data',
                       xytext=(-1.0, 1.3), textcoords='data',
                       arrowprops=dict(arrowstyle='simple',  # '"->",
                       connectionstyle="arc3", color='gray'))

    axs_eigen.annotate('',
                       xy=(-1.5, -0.75), xycoords='data',
                       xytext=(-1.0, -1.3), textcoords='data',
                       arrowprops=dict(arrowstyle='simple',  # '"->",
                                       connectionstyle="arc3", color='gray'))

    ##########################################################################
    # axis names
    ##########################################################################
    # axs_eigen.set_xticks(np.arange(-30, 10, 1))
    # axs_eigen.set_xlim([xmin, xmax])

    axs_eigen.set_xscale('symlog',
                          linthresh=3,
                          subs=np.arange(1, 3),
                          linscale=1.0)  # 0.75
    axs_eigen.set_xlim([-20, 0])
    axs_eigen.set_xticks([-20, -10, -5, -3, -2, -1, 0])
    axs_eigen.set_xticklabels([-20, -10, -5, -3, -2, -1, 0])

    axs_eigen.set_yticks(np.arange(-5, 10, 0.5))
    axs_eigen.set_ylim([ymin, ymax])

    axs_eigen.legend(loc='lower left', frameon=True)

    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    fig_eigen.tight_layout()
    fig_eigen.savefig(figeigename, format='eps')

    plt.show()


#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_eigen_from_7_csvs()
    # print("Nothing else done")


if __name__ == '__main__':
    main()

