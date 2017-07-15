import numpy as np
# coding:UTF-8
class SMOTE(object):
    '''
    少数派データの数＊N個数分の距離が近いサンプルを生成する。
    '''
    def __init__(self, N):
        #  サンプル生成を何回繰り返すか
        self.N = N
        self.T = 0
        self.nnk = 0
    def oversampling(self, smp, cv, label):
        '''
        @param smp : 全データ
        @param cv  : 目的変数
        '''
        # indexes indicate to　minoryty data
        mino_idx = np.where(cv==label)[0]
        # minoryty data
        mino_smp = smp[mino_idx,:]
        # num of neighbor
        self.nnk = 3

        # kNNの実施(K近傍方)
        mino_nn = []

        for idx in mino_idx:
            near_dist = np.array([])
            # nnk -> 対象とするデータの幾つの近所を選ぶか。
            # ２クラスの時、nnkを奇数にすると多数決で一意に決まる
            near_idx = np.zeros( self.nnk )
            for i in range(len(smp)):
                if idx != i:
                    dist = self.dist(smp[idx,:], smp[i,:])

                    if len(near_dist)<self.nnk: # 想定ご近所さん数(nnk)まで到達していなければ問答無用でlistに追加
                        tmp = near_dist.tolist()
                        tmp.append(dist)
                        near_dist = np.array(tmp)
                    elif sum(near_dist[near_dist > dist])>0:    # 近いものがあればそっち選ぼう
                        near_dist[near_dist==near_dist.max()] = dist
                        near_idx[near_dist==near_dist.max()] = i
            mino_nn.append(near_idx)
        return self.create_synth( smp, mino_smp, np.array(mino_nn, dtype=np.int) )

    def dist(self, smp_1, smp_2):
        return np.sqrt( np.sum((smp_1 - smp_2)**2) )

    '''
    @param mino_nn   : nnk*少数派のデータ数の行列
    @param smp       : 全てのデータ
    @param mino_smp  : 少数派のデータ
    '''
    def create_synth(self, smp, mino_smp, mino_nn):
        self.T = len(mino_smp)
        if self.N < 100:
            self.T = int(self.N*0.01*len(mino_smp))
            self.N = 100
        self.N = int(self.N*0.01)
        # random.unifom -> 一様分布に従う乱数の生成
        # T個の0以上mino_samp以下の乱数を生成
        # 0以上mino_smp数以下の整数型乱数をT個(少数派データの個数)作る
        rs = np.floor( np.random.uniform(size=self.T)*len(mino_smp) )
        synth = []
        for n in range(self.N):
            for i in rs:
                # 0以上self.nnk以下の整数
                nn = int(np.random.uniform(size=1)[0]*self.nnk)
                # 　全データの中でi列目のデータにnnk番以内に近かったデータと少数派データi列のデータの差
                dif = smp[mino_nn[i,nn],:] - mino_smp[i,:]
                # gap: メトリクス数の０以上１以下の乱数
                gap = np.random.uniform(size=len(mino_smp[0]))
                tmp = mino_smp[i,:] + np.floor(gap*dif)
                # tmpの中で、0以下のものを全て0にする
                tmp[tmp<0]=0
                synth.append(tmp)
        return synth
