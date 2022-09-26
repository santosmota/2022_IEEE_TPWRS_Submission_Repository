import numpy as np

###############################################################
# According to the git below, these colors are more colorblind friendly
# https://gist.github.com/thriveth/8560036
###############################################################
cor_dalt = {
    'blue':   '#377eb8',        # (55,  126, 184)
    'orange': '#ff7f00',        # (255, 127, 0),
    'green':  '#4daf4a',        # (77,  175, 74),
    'pink':   '#f781bf',        # (247, 129, 191),
    'brown':  '#a65628',        # (166, 86,  40),
    'purple': '#984ea3',        # (152, 78,  163),
    'red':    '#e41a1c',        # (228, 26,  28),
    'yellow': '#dede00',        # (222, 222, 0)
    'gray':  '#999999'         # (153, 153, 153)
}


###############################################################################################
# FUNCTION: time offset
###############################################################################################
def time_offset(time, offset=0.0):
    print('----------------')
    print('Function: ', time_offset.__name__)

    if offset == 0.0:
        return time
    else:
        n_row = len(time)
        result_time = np.zeros(n_row)
        for t in range(0, n_row):
            result_time[t] = time[t] + offset
        return result_time

###############################################################################################
# FUNCTION: Damping lines for the root locus
###############################################################################################
def plot_root_locus_damping_lines(eigen_real, eigen_imag, axis, nzetalines=19,
                                  max_axis='auto', max_real=1000.0, max_imag=1000.0,
                                  color='black', label=None, linestyle='dotted',
                                  linewidth=0.5, marker=None, markersize=None,
                                  add_pos_damping_numbers=False,
                                  min_damp_for_adding_numbers=0.4,
                                  max_damp_for_adding_numbers=1.0,
                                  n_segments=1):
    print('----------------')
    print('Function: ', plot_root_locus_damping_lines.__name__)

    if max_axis == 'auto':
        max_abs_real = 1.1*np.max(np.abs(eigen_real))
        max_abs_imag = 1.1*np.max(np.abs(eigen_imag))
    else:
        max_abs_real = np.abs(max_real)
        max_abs_imag = np.abs(max_imag)

    amp_max = 2.0*np.max([max_abs_real, max_abs_imag])

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
        for i in range(1, nzetalines-1, 1):
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
                auxd = - x[i] / (x[i]**2 + y[i]**2)**0.5
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
                y[j+1] = amps[j] * np.sin(angles[i])
                if y[j+1] > max_abs_imag:
                    y[j+1] = max_abs_imag
                    x[j+1] = y[j+1] / np.tan(angles[i])
                    if x[j+1] < -max_abs_real:
                        x[j+1] = -max_abs_real
                        y[j+1] = x[j+1] * np.tan(angles[i])
                elif y[j+1] < -max_abs_imag:
                    y[j+1] = -max_abs_imag
                    x[j+1] = y[j+1] / np.tan(angles[i])
                    if x[j+1] < -max_abs_real:
                        x[j+1] = -max_abs_real
                        y[j+1] = x[j+1] * np.tan(angles[i])
                else:
                    x[j+1] = amps[j] * np.cos(angles[i])
                    if x[j+1] < -max_abs_real:
                        x[j+1] = -max_abs_real
                        y[j+1] = x[j+1] * np.tan(angles[i])

            axis.plot(x, y, color=color, label=label, linestyle=linestyle,
                      linewidth=linewidth, marker=marker, markersize=markersize)

            if add_pos_damping_numbers and y[-1] > 0.00001:
                if i == 1:
                    auxind = n_segments - 30
                elif i == 2:
                    auxind = n_segments - 40
                elif i == 3:
                    auxind = n_segments - 47
                elif i == 4:
                    auxind = n_segments - 58
                elif i == 5:
                    auxind = n_segments - 60
                elif i == 6:
                    auxind = n_segments - 48
                elif i == 7:
                    auxind = n_segments - 48
                elif i == 8:
                    auxind = n_segments - 48
                else:
                    auxind = -1


                auxd = - x[auxind] / (x[auxind] ** 2 + y[auxind] ** 2) ** 0.5
                if auxd > min_damp_for_adding_numbers and auxd < max_damp_for_adding_numbers:
                    axis.text(x=x[auxind], y=y[auxind],
                              s=r"$\zeta={:.2f}$".format(auxd),
                              ha='left', va='top')



###############################################################################################
# FUNCTION: Open Project and Study Case
###############################################################################################
def add_root_locus_part_names(eigen_real,
                              eigen_imag,
                              eigen_part_names,
                              axis,
                              zeta_threshold=0.7,
                              real_min=-1000,
                              real_max=1000,
                              imag_min=-1000,
                              imag_max=1000,
                              xanot_offset=0,
                              yanot_offset=0,
                              hor_orient='right',
                              vert_orient='center'
                              ):
    print('----------------')
    print('Function: ', add_root_locus_part_names.__name__)

    for (r, j, name) in zip(eigen_real, eigen_imag, eigen_part_names):
        amp = (r**2.0 + j**2.0)**0.5
        zeta = -r / amp
        if zeta < zeta_threshold:
            if r > real_min and r < real_max and j > imag_min and  j < imag_max:
                axis.text(x=r+xanot_offset,
                          y=j+yanot_offset,
                          s=name.replace('_', '-'),
                          ha=hor_orient, va=vert_orient)
            


###############################################################################################
# FUNCTION: Open Project and Study Case
###############################################################################################
def add_root_locus_participation_name(df,
                              axis,
                              modes=[0],
                              xanot_offset=0.0,
                              yanot_offset=0.0,
                              hor_orient='right',
                              vert_orient='center',
                              text_color='black',
                              names='',

                              ):
    print('----------------')
    print('Function: ', add_root_locus_participation_name.__name__)

    if names == '':
        for mode in modes:
            axis.text(x=df.iloc[mode, df.columns.get_loc('real')] + xanot_offset,
                      y=df.iloc[mode, df.columns.get_loc('imag')] + yanot_offset,
                      s=df.iloc[mode, df.columns.get_loc('names')].replace('_', '-'),
                      ha=hor_orient, va=vert_orient, color=text_color)
    else:
        for [mode, name] in zip(modes, names):
            axis.text(x=df.iloc[mode, df.columns.get_loc('real')] + xanot_offset,
                      y=df.iloc[mode, df.columns.get_loc('imag')] + yanot_offset,
                      s=name.replace('_', '-'),
                      ha=hor_orient, va=vert_orient, color=text_color)