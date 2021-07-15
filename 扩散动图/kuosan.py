#导入所需的库
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Strategy:
    def __init__():
        # print("初始化")
        pass

    # 指定隔离
    def assignSegregated(d_step, P0, segregatedXY):
        for x, y in segregatedXY:
            d_step[y*20+x] = 0.0    # index从0开始计，设置不移动
            P0[y*20+x] = 0.05       # 减少基础感染率

    # 随机隔离
    def randomSegregated(d_step, P0, percentage):
        pass



# 创建扩散模型类
class Diffusion:

    # 初始化
    def __init__(self, N):
        self.N = N              # 边长
        self.NI = N**2          # 个体数量为N^2
        self.indivduals = None
        self.dist = None        # 个体间初始距离
        self.NoP = 0            # 保存目前的感染数
       
    # 初始化个体位置
    def init_pos(self, dist):
        self.dist = dist
        N = self.N
        # [  0.   6.  12.  18.  24.  30.  36.  42.  48.  54.  60.  66.  72.  78.  84.  90.  96. 102. 108. 114.]
        x, y = np.linspace(0, (N-1)*dist, N), np.linspace(0, (N-1)*dist, N)
        # 以左下角为坐标原点
        # vx [[  0.   6.  12.  18.  24.  30.  36.  42.  48.  54.  60.  66.  72.  78.  84.  90.  96. 102. 108. 114.] 第一排的x（最下）
        #     [  0.   6.  12.  18.  24.  30.  36.  42.  48.  54.  60.  66.  72.  78.  84.  90.  96. 102. 108. 114.] 第二排的x
        #     ...]
        # vy [[  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.  0.   0.   0.   0.   0.   0.] 第一排的y（最下）
        #     [  6.   6.   6.   6.   6.   6.   6.   6.   6.   6.   6.   6.   6.   6.  6.   6.   6.   6.   6.   6.] 第二排的y
        #     ...]
        vx, vy = np.meshgrid(x, y)

        # 变成一排
        self.ix, self.iy = vx.flatten(), vy.flatten() # flatten变成一排
        # 
        self.iix, self.iiy = vx.flatten(), vy.flatten()

    # 设置模型参数
    def init_para(self, D0, P0, P1, W, d_step = 0.05, t_step = 0.01, A=np.e):
        self.D0 = np.asarray(D0)        # 临界距离      (1, NI)
        self.P0 = np.asarray(P0)        # 基础感染率    (1, NI)
        self.P1 = np.asarray(P1)        # 传染率        (1, NI)
        self.size = 110 - self.P1*100         # 感染者可视化大小，P1越小，传染性越强，点越大(范围在10 - 110)
        self.W = np.asarray(W)          # 亲密度        (NI, NI)
        self.A = np.asarray(A)          # 概率计算底数，所有人都一样，反映了超过临界距离后被感染风险的衰减程度

        # d0 = np.max(self.D0) 作者写的
        d0 = np.max(self.D0)            # 修正后，使得感染门槛稍小一点
        p0 = np.max(self.P0)            # 如果用min求得最小，若有很小的P0，则全图很快被感染, 因此每次循环时间也很长（对每位感染者的循环）
        p1 = np.min(self.P1)            # 若用max，则可能使得self.p_min很小，很快全图感染
        w = np.min(self.W)
        a = np.min(self.A)

        self.t_step = t_step                                # 移动一次的时间步长
        self.d_step = np.asarray(d_step)                    # 每个个体的移动步长 (1, NI)
        dist = self.dist
        self.p_min = (1+w)*p0/(p1*(a**(dist-d0)))                # 修正后的 最小感染几率

        self.patients = np.zeros(self.NI, dtype = int)      # 几率这一轮被感染的人

    # 放置感染源
    def place_source(self, source):
        self.patients[source] = 1
       

    # 个体游走
    def walk(self, t):
        t_step = self.t_step
        d_step = self.d_step
        NI = self.NI
        step_d = d_step*self.dist
        n_step = int(t//t_step) # t反映了游走时间长度, n_step为这一轮要走多少步

        # random_integers，[1, 4]之间，生成n_step*NI个数
        # moves [[2 3 1 ... 1 3 3]
        #       [1 1 3 ... 2 3 2]
        #       [4 3 2 ... 1 4 3]
        #       ...
        #       [2 1 1 ... 2 2 4]
        #       [2 1 2 ... 2 1 3]
        #       [3 2 1 ... 4 3 2]]
        moves = np.random.random_integers(1,4, n_step*NI).reshape(n_step, NI) # 一排为所有点的这一步的走法

        ix, iy = self.ix, self.iy # 保存着所有点的坐标
        iix, iiy = self.iix, self.iiy
        UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

        # 走n_step步
        for step in range(n_step):
            thisStep = moves[step]
            # np.where(condition, x, y), 满足条件(condition)，返回x，不满足返回y
            ix += np.where(thisStep == RIGHT, d_step, 0.)
            ix -= np.where(thisStep == LEFT, d_step, 0.)
            iy += np.where(thisStep == UP, d_step, 0.)
            iy -= np.where(thisStep == DOWN, d_step, 0.)

            # np.any对矩阵所有元素做或运算，因此若存在True则返回True
            if np.any(self.patients): # 如果有病人
                self.update_patients()

        # 保存目前的感染数
        self.NoP = np.nonzero(self.patients)[0].shape[0]
    
    
    # 更新感染者
    def update_patients(self):
        dist = self.dist
        current_patients = np.nonzero(self.patients)[0] # 记录被感染者的index，范围0-399
        
        for patient in current_patients:
            Dx = self.ix[patient] - self.ix         # 与每个人的x轴距离
            Dy = self.iy[patient] - self.iy         # 与每个人的y轴距离

            Dxy = np.hypot(Dx, Dy)                  # 返回欧几里德范数 sqrt(x*x + y*y)
            Dxy = np.where(Dxy>dist, dist, Dxy)     # 距离大于【个体间初始距离】，则按初始距离dist算，否则按实际距离算

            Dij = Dxy-self.D0                           # 减去每个人自身的临界距离，求得Dij
            p1j = self.P1[patient]

            WP0 = (1+self.W)*self.P0/p1j                # 求得感染概率（Dij＜＝临界距离时）
            WP1 = WP0/self.A**(Dij)                     # 求得感染概率（Dij＞临界距离时）
            Pij0 = np.where(Dij<=0, WP0, 0.)            # 临界内，返回概率WP0
            Pij1 = np.where(Dij>0, WP1, 0.)             # 临界外，返回概率WP1
            Pij = Pij0 + Pij1                           # 合并得到每个个体最终感染概率
            
            # numpy.random.uniform(low,high,size)，从一个均匀分布[low,high)中随机采样
            Pr = np.random.uniform(self.p_min, 1, self.NI)      # 在最低值和最高值之间随机选择，来决定感染门槛，大于该门槛则感染
            DP = Pr - Pij
            infected = np.argwhere(DP < 0)
            self.patients[infected] = 1


    def plot(self):
        ix,iy = self.ix,self.iy
        patients = self.patients
        x_max,x_min = np.max(ix),np.min(ix)
        y_max,y_min = np.max(iy),np.min(iy)
        x_max,x_min = x_max+10,x_min-10
        y_max,y_min = y_max+10,y_min-10
        # print(patients)

        infected = np.where(patients == 1.)
        # print(infected)
        noninfected = np.where(patients != 1.)
        selfIsolation = np.array([130, 131, 150, 151, 170, 171, 190, 191, 210, 211]) # 自隔离的
        selfIsoX = [60, 66, 60, 66, 60, 66, 60, 66, 60, 66]
        selfIsoY = [36, 36, 42, 42, 48, 48, 54, 54, 60, 60]
        # print(noninfected)
        noninfected = np.setdiff1d(noninfected, selfIsolation)
        # print(noninfected)
        
        iix = ix[infected]
        iiy = iy[infected]
        nix = ix[noninfected]
        niy = iy[noninfected]
        plt.clf() # 会直接导致最后生成的gif只有最后一帧图像，前面的全被清除了
        plt.axis([x_min,x_max,y_min,y_max])

        im = plt.scatter(nix, niy, marker = "*", color = "b").findobj()
        # 130, 131, 150, 151, 170, 171, 190, 191, 210, 211, 
        im += plt.scatter(selfIsoX, selfIsoY, marker = "*",color = "g").findobj()
        im += plt.scatter(iix, iiy, marker = ".", s=self.size[infected], color = "r").findobj()
        return im
        
if __name__ == '__main__':
    seed = int(time.time())
    random.seed(seed)

    N = 20  
    D0 = 2.             # 临界距离；可传入矩阵(1, NI)，设置每个个体临界距离，代表病原体离该个体的距离小于该个体的临界距离，则该个体被感染风险很大
    P0 = 0.3            # 个体基础感染几率；可传入矩阵(1, NI)，健康群体自身被感染者感染的几率；基础理解为抵抗力，抵抗力越强，基础感染率越小
    P0 = np.asarray([P0]*400)
    P1 = 0.5            # 传染性：感染者对健康群体的传染性, 越接近于0，传染性越强
    P1 = np.asarray([(random.random()/2)+0.25 for _ in range(400)]) # 随机传染性
    W = 0               # 亲密度，越大越容易感染；可传入矩阵(NI, NI)，每个个体与其他所有个体的亲密度，可认为wij = wji
    dist = 6.           # 个体间初始距离
    t_step = 0.01       # 移动一次的时间步长
    # d_step = [0.05]*130 + [0., 0.] + [0.05]*18 + [0., 0.] + [0.05]*18 + [0., 0.] + [0.05]*18 + [0., 0.] + [0.05]*18 + [0., 0.] + [0.05]*188
    d_step = np.asarray([0.05]*400) # 移动步长；似乎也可以是矩阵(1, NI)
    
    # 隔离操作
    segregatedXY = [[10, 6], [11, 6], [10, 7], [11, 7], [10, 8], [11, 8], [10, 9], [11, 9], [10, 10], [11, 10]] # 位置，从0开始（单位/个）
    Strategy.assignSegregated(d_step=d_step, P0=P0, segregatedXY=segregatedXY)

    m = Diffusion(N) 
    m.init_pos(dist)                                                # 初始化位置
    m.init_para(D0, P0, P1, W, t_step = t_step, d_step = d_step)    # 模型参数设置
    m.place_source([153, 146, 310])                                 # 放置感染源个体，在153位置(从0开始)，具体位置为(153//20, 153%20) 也是从0开始

    PatientsNumbers = []
    fig = plt.figure()
    plt.ion()

    ims = []
    for i, t in enumerate([1]*100):
        print(i+1)
        m.walk(t)
        ims.append(m.plot())
        PatientsNumbers.append(m.NoP)
        plt.pause(0.1)

    plt.ioff()
    plt.show()

    ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)
    ani.save("test.gif", writer='pillow')