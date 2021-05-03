import math as math
import scipy.optimize as optimize
import numpy as np
import itertools as itertools
import time as time
import scipy.ndimage


class TwoGradOptimize:

    def __init__(self, instrument_params, method_params, input_params, rawdata):
        
        ## Instrument
        self.instrument_name = instrument_params[0]
        self.td = instrument_params[8]
    
        ## Column
        self.col_name = instrument_params[1]
        self.col_length = instrument_params[2]
        self.col_diameter = instrument_params[3]
        self.particle_size = instrument_params[4]
        self.pore_diameter = instrument_params[5]
        self.N = instrument_params[6]
        self.t0 = instrument_params[7]
        
        ## Method
        self.flow_rate = method_params[0]
        self.tG_final = method_params[1]
        self.phi0_init = np.array([method_params[2]], dtype='float64')
        self.phif_init = np.array([method_params[3]], dtype='float64')
        self.UV = method_params[4]
        self.tG1 = method_params[5]
        self.tG2 = method_params[6]
    
        ## Data
        self.peaknum = input_params[0]
        self.peakinterest = input_params[1]
        self.rawdata = rawdata
    
        ## Peak
        self.calcParams = []
    
        ## Resolution
        self.phi0 = np.array([method_params[2]], dtype='float64')
        self.phif = np.array([method_params[3]], dtype='float64')
        self.tG = np.array([method_params[1]], dtype='int64')
        self.total_Rs = 0
        self.critical_Rs = 0
    
        ## Graph
        self.y_max = 0


    def calculateParameters(self):

        def estimate_b(beta, tr1, tr2):
            b = math.sqrt(((self.t0 * math.log10(beta)) / (tr1 - (tr2/beta) - (self.t0 + self.td)*(beta - 1)/beta))**2)
            return(b)

        def calculate_logk0(b, tr):
            logk0_est = b * (tr - self.t0 - self.td) / self.t0-math.log10(2.3*b)
            return(logk0_est)

        def calculate_s(b, tG, delta_phi):
            s = (b * tG) / (self.t0 * delta_phi)
            return(s)

        def calculate_logkw(logk0, s):
            logkw = logk0 + (s * self.phi0_init)
            return(logkw)

        def estimate_N(logk0, b, w):
            k_star = (10**logk0) / (2.3 * b * ((10**logk0) / 2) - (self.t0 / self.td) + 1)
            N = (4 * ((k_star + 2)**2) * (self.t0**2)) / w**2
            return(N)

        avg_params = []

        for n in range(self.peaknum):

            tr1 = self.rawdata[n][0][0] 
            tr2 = self.rawdata[n][0][1]
            w1 = self.rawdata[n][2][0]
            w2 = self.rawdata[n][2][1]
            tr_list = [tr1, tr2]
            w_list = [w1, w2]
            tG_list = [self.tG1, self.tG2]
            delta_phi = np.subtract(self.phif_init, self.phi0_init)

            beta_list = [tG_list[1]/tG_list[0], tG_list[0]/tG_list[1]]

            s_sum = 0
            logkw_sum = 0
            N_sum = 0
            counter = 0

            for beta in beta_list:
                b_est = estimate_b(beta, tr1, tr2)
                tr1, tr2 = tr2, tr1
                tG = tG_list[counter]
                tr = tr_list[counter]
                w = w_list[counter]

                logk0_est = calculate_logk0(b_est, tr)

                def retention_f(b):
                    tr_est = (self.t0/b_est) * math.log10(2.3 * (10**logk0_est) * b * (1 - (self.td / (self.t0 * (10**logk0_est)))) + 1) + self.t0 + self.td
                    return(math.sqrt((tr_est - tr)**2))

                b_opt = optimize.root(retention_f, b_est).x[0]

                s = calculate_s(b_opt, tG, delta_phi)
                logk0 = calculate_logk0(b_opt, tr)
                logkw = calculate_logkw(logk0, s)
                N = estimate_N(logk0, b_opt, w)

                s_sum += s
                logkw_sum += logkw
                N_sum += N
                counter += 1

            s_avg = s_sum/2
            logkw_avg = logkw_sum/2
            N_avg = N_sum/2

            avg_params.append((s_avg, logkw_avg, N_avg))

        self.calcParams = avg_params
                

    def predictRetentionWidth(self):

        def calculate_logk0(logkw, s):
            logk0 = logkw - (s * self.phi0) 
            return(logk0)

        def calculate_b(s, delta_phi):
            b = (s * (self.t0) * delta_phi) / self.tG_final
            return(b)
        
        def calculate_tr_smallk0(logk0):
            tr = self.t0 * (1 + (10**logk0))
            return(tr)

        def calculate_tr_largek0(b, logk0):
            tr = (self.t0 / b) * np.log10(2.3 * (10**logk0) * b * (1 - (self.td / (self.t0 * (10**logk0)))) + 1) + self.t0 + self.td
            return(tr)

        def calculate_w(logk0, b, N):
            k_star = (10**logk0) / (2.3 * b * ((10**logk0) / 2) - (self.t0 / self.td) + 1)
            w = (4 * (N**(-1/2))) * self.t0 * (1 + (k_star / 2))
            return(w)

        tr_w_list = []

        delta_phi = np.subtract(self.phif, self.phi0)

        iso = np.where(delta_phi==0)
        delta_phi[iso] = 0.001

        for p in self.calcParams:
            i = self.calcParams.index(p)
            s = self.calcParams[i][0]
            logkw = self.calcParams[i][1]
            N = self.calcParams[i][2]
            logk0 = calculate_logk0(logkw, s)
            b = calculate_b(s, delta_phi)

            tr = np.zeros(len(self.phi0))

            smallk0 = np.where((self.t0 * (10**logk0)) <= self.td)
            tr[smallk0] = calculate_tr_smallk0(logk0[smallk0])
            
            largek0 = np.where(tr == 0)
            tr[largek0] = calculate_tr_largek0(b[largek0], logk0[largek0])

            beforedelay = np.where(tr < self.t0)
            tr[beforedelay] = self.t0

            w = calculate_w(logk0, b, N)

            tr_w_list.append((tr, w, i))

        self.tr_w_list = tr_w_list


    def predictResolution(self):

        def calculate_res(tr1, tr2, w1, w2):
            res = np.sqrt((2*(tr2 - tr1)/(w1 + w2))**2)
            return(res)

        total_Rs = np.zeros(len(self.tr_w_list[0][0]))
        critical_Rs = np.zeros(len(self.tr_w_list[0][0]))

        tr_w_combos = itertools.combinations(self.tr_w_list, 2)

        for tr_w_pair in tr_w_combos:
            tr1 = tr_w_pair[0][0]
            tr2 = tr_w_pair[1][0]
            w1 = tr_w_pair[0][1]
            w2 = tr_w_pair[1][1]
            i1 = tr_w_pair[0][2]
            i2 = tr_w_pair[1][2]

            t_Rs = np.zeros(len(tr1), dtype='float64')
            c_Rs = np.zeros(len(tr1), dtype='float64')

            valid = np.where((tr1 < self.tG_final) | (tr2 < self.tG_final))
            t_Rs[valid] = calculate_res(tr1[valid], tr2[valid], w1[valid], w2[valid])

            interest = np.where(((i1 == self.peakinterest - 1) & (tr1 < self.tG_final)) | ((i2 == self.peakinterest - 1) & (tr2 < self.tG_final)))
            c_Rs[interest] = calculate_res(tr1[interest], tr2[interest], w1[interest], w2[interest])

            total_Rs = np.add(total_Rs, t_Rs)
            critical_Rs = np.vstack([critical_Rs, c_Rs])

        critical_Rs = np.delete(critical_Rs, (0), axis=0)
        critical_Rs[critical_Rs==0] = np.nan
        critical_Rs = np.nanmin(critical_Rs, axis=0)

        return((total_Rs, critical_Rs))

    
    def generateXY(self):

        y_list = []
        y_max_list = []
        x = np.linspace(0, self.tG_final, 1000)

        for i, tr_w in enumerate(self.tr_w_list):
            tr, w = tr_w[0:2]
            c = 1000
            area = sum(self.rawdata[i][1])/2
            h = area/(math.sqrt(math.pi)*c)
            y = h * np.exp(-1*((x - tr)**2)/((w/2)**2))
            y_max_list.append(np.amax(y))
            y_list.append(y)

        y_max = max(y_max_list)
        self.y_max = y_max + (0.1 * y_max)
        total_y = sum(y_list)
        return((x, total_y))


    def generatePlot(self, FigCanvas):

        FigCanvas.ax1.set_visible(True)

        self.predictRetentionWidth()
        x, y = self.generateXY()
        self.total_Rs, self.critical_Rs = self.predictResolution()

        self.graph, = FigCanvas.ax1.plot(x,y, linewidth=1.2)
        FigCanvas.ax1.set_xlim([0,self.tG_final])
        FigCanvas.ax1.set_ylim([(0 - self.y_max/100),self.y_max])
        if self.tG_final <= 1:
            FigCanvas.ax1.set_xticks(np.round(np.linspace(0,self.tG_final,(self.tG_final/0.2)+1),1))
        elif self.tG_final <= 2:
            FigCanvas.ax1.set_xticks(np.round(np.linspace(0,self.tG_final,(self.tG_final/0.4)+1),1))
        elif self.tG_final <= 4:
            FigCanvas.ax1.set_xticks(np.linspace(0,self.tG_final,(self.tG_final/0.5)+1))
        elif self.tG_final <= 20:
            FigCanvas.ax1.set_xticks(range(0,self.tG_final+1,1))
        elif self.tG_final <= 50:
            FigCanvas.ax1.set_xticks(range(0,self.tG_final+1,2))
        else:
            FigCanvas.ax1.set_xticks(range(0,self.tG_final+1,5))


    def maximiseRes(self):

        m = np.linspace(0, 1, 501)
        n = np.linspace(0, 1, 501)
        o = np.array(np.meshgrid(m, n))
        p = o.transpose()
        valid = np.where((o[0] - o[1] >= 0.15))
        conditions = np.array(p[valid], dtype='float64')

        self.phi0 = conditions[:,0]
        self.phif = conditions[:,1]

        self.predictRetentionWidth()
        critical_res = self.predictResolution()[1]
        max_condition = conditions[np.nanargmax(critical_res)]

        self.phi0, self.phif = max_condition

        return(max_condition)


    def updatePlot(self, FigCanvas):

        self.predictRetentionWidth()
        self.total_Rs, self.critical_Rs = self.predictResolution()
        x, y = self.generateXY()

        self.graph.set_data(x,y)
        FigCanvas.ax1.set_xlim([0,self.tG_final])
        if self.tG_final <= 1:
            FigCanvas.ax1.set_xticks(np.round(np.linspace(0,self.tG_final,(self.tG_final/0.2)+1),1))
        elif self.tG_final <= 2:
            FigCanvas.ax1.set_xticks(np.round(np.linspace(0,self.tG_final,(self.tG_final/0.4)+1),1))
        elif self.tG_final <= 4:
            FigCanvas.ax1.set_xticks(np.linspace(0,self.tG_final,(self.tG_final/0.5)+1))
        elif self.tG_final <= 20:
            FigCanvas.ax1.set_xticks(range(0, self.tG_final+1,1))
        elif self.tG_final <= 50:
            FigCanvas.ax1.set_xticks(range(0,self.tG_final+1,2))
        else:
            FigCanvas.ax1.set_xticks(range(0,self.tG_final+1,5))

        FigCanvas.fig.canvas.draw()


    def plotResMap(self, FigCanvas):

        ax2 = FigCanvas.ax2

        m = np.linspace(0, 1, 501)
        n = np.linspace(0, 1, 501)
        o = np.array(np.meshgrid(m, n))
        p = o.transpose()
        valid = np.where((o[0] - o[1] >= 0.15))
        conditions = np.array(p[valid], dtype='float64')

        self.phi0 = conditions[:,0]
        self.phif = conditions[:,1]

        self.predictRetentionWidth()
        total_res, critical_res = self.predictResolution()
        critical_res = np.nan_to_num(critical_res)
        max_res = np.max(critical_res)

        ax2.tricontourf(self.phi0, self.phif, critical_res, levels = [0, max_res/4, max_res/2, max_res/1.5, max_res], colors=['blue', 'green', 'yellow', 'red'])