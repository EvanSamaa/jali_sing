from matplotlib import pyplot as plt
import json
import numpy as np
import matplotlib.animation as animation
def plot_consonants(cons):
    for c in cons:
        x, y = c
        line.set_data(x, y, "k")
def plot_vowel(M_P, Mnot_Pnot, M_Pnot, Mnot_P, M, P):
    temp_P = M * M_P  +  (1.0-M) * Mnot_P
    temp_Pnot = M_Pnot * M + Mnot_Pnot * (1.0 - M)
    x = np.arange(0, Mnot_Pnot.shape[0])
    y = temp_P * P + temp_Pnot * (1.0-P)
    return x, y
def init():
    line.set_data([], [])
    return line,

if __name__ == "__main__":
    def Animmm(M, P, M_P, Mnot_Pnot, M_Pnot, Mnot_P, consonants):
        def animate(i):
            x, y = plot_vowel(M_P, Mnot_Pnot, M_Pnot, Mnot_P, M[i], P[i])
            line.set_data(x, y)
            # plot_consonants(consonants)
            line2.set_data(consonants[1][0], consonants[1][1])
            line3.set_data(consonants[2][0], consonants[2][1])
            line4.set_data(consonants[3][0], consonants[3][1])
            line5.set_data(consonants[4][0], consonants[4][1])
            line6.set_data(consonants[0][0], consonants[0][1])

            # print("here")
            return line, line2, line3,line4, line5, line6
        return animate
    f = open("curves.txt")
    f2 = open("MaPs_curves.txt")
    dict_thing = json.load(f)
    MP_dict = json.load(f2)
    consonants = ['LNTDa_pointer', 'Ya_pointer', 'FVa_pointer']
    print(dict_thing.keys())
    m = np.array(MP_dict["Jaw"])
    p = np.array(MP_dict["Lip"])
    Mnot_P = np.array(dict_thing["Ah_pointer_Mnot_P"])
    M_Pnot = np.array(dict_thing["Ah_pointer_M_Pnot"])
    M_P = np.array(dict_thing["Ah_pointer_M_P"])
    Mnot_Pnot = np.array(dict_thing["Ah_pointer_Mnot_Pnot"])
    consonants_curves = []
    print(m.shape)
    A[2]
    # consonants
    for c in consonants:
        y = []
        x = []
        for n in range(0, len(dict_thing[c])):
            val = dict_thing[c][n]
            if val > 0.001:
                y.append(val)
                x.append(n)
            if n > 1 and dict_thing[c][n-1] > 0 and val == 0:
                consonants_curves.append([np.array(x), np.array(y)])
                # plt.plot(np.array(x), np.array(y), "k")
                # y = []
                # x = []
    i = 0

    # for i in range(0, 10000):
    #     x, y = plot_vowel(M_P, Mnot_Pnot, M_Pnot, Mnot_P, m[i], p[i])
    #     plt.plot(x, y)
    #     plt.show(block=False)
    #     plt.pause(1)
    #     plt.close()

    # plot_consonants(consonants_curves)
    # plot_vowel(M_P, Mnot_Pnot, M_Pnot, Mnot_P, m[i], p[i])
    # plt.show()
    fig = plt.figure(figsize=(12,9))
    figsize = (8, 6)
    ax = plt.axes(xlim=(-100, 2500), ylim=(-1, 12))
    # ax = fig.add_subplot(111, aspect='equal', autoscale_on=False)
    fig.canvas.set_window_title('Matplotlib Animation')
    line, = ax.plot([], [], '-', lw=2, color="#f37f0c")
    line2, = ax.plot([], [], '-', lw=1, color='#adadab')
    line3, = ax.plot([], [], '-', lw=1, color='#adadab')
    line4, = ax.plot([], [], '-', lw=1, color='#adadab')
    line5, = ax.plot([], [], '-', lw=1, color='#adadab')
    line6, = ax.plot([], [], '-', lw=1, color='#adadab')

    ani = animation.FuncAnimation(fig, Animmm(m, p, M_P, Mnot_Pnot, M_Pnot, Mnot_P, consonants_curves), frames=m.shape[0]-1,
                                    blit=True, init_func=init, interval=1.0/24)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    # ani.save('double_pendulum.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    # f = "out.gif"
    # writergif = animation.PillowWriter(fps=24)
    # ani.save(f, writer=writergif)
    # plt.show()
    f = "out.mp4"
    writervideo = animation.FFMpegWriter(fps=24)
    ani.save(f, writer=writervideo)
