import numpy as np
from collections import defaultdict
import random

class agent():
    """q値の計算を行うためのプログラム。envにturn数、与えるダメージ、d-blockを入れておく。"""
    def __init__(self, 
            done = False,
            learning_rate=0.01,
            discount_factor=0.9,
            epsilon_greedy=0.9,
            epsilon_min=0.1,
            epsilon_decay=0.95):
        #self.env = env
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon_greedy
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.f = open("q_table.txt","w")
        

        # Define the q_table
        #self.q_table = np.zeros((20,75, 45))#ターン数、与えるダメージ、d-blockを記録する配列を作成する。
        self.q_table = np.zeros((90,75))#敵の体力、与えるダメージを記録する配列を作成する。

    def q_learn(self, env):
        """ターン数、敵の体力(ターン開始時)"""
        turn,enemy_hp, attack, d_block, r, next_t,next_hp, done = env
        #print(turn,enemy_hp, attack, d_block, r, next_t,next_hp, done,"turn,enemy_hp, attack, d_block, r, next_t,next_hp, done")
        q_val = 0
        #for i in range(4):
        #    q_val += self.q_table[turn][enemy_hp+i][attack+i][d_block+i]/4
        #q_val = self.q_table[turn][attack][d_block]
        q_val = self.q_table[enemy_hp][attack]

        #print(r,'r')
        #print(q_val,'q_val')
        if done:
            q_target = r
        else:
            #q_target = r + self.gamma*np.max(self.q_table[turn,:,:])
            q_target = r + self.gamma*np.max(self.q_table[next_hp,:])
        #print(q_target, "q_target")
        # Update the q_table
        #self.q_table[turn][attack][d_block] += self.lr * (q_target - q_val)
        self.q_table[enemy_hp][attack] += self.lr * (q_target - q_val)
       #return self.q_table[turn][enemy_hp][attack][d_block]
    
    def choose_action(self, t, attack_amount_list, d_list, choice_list_list, enemy_hitpoint):
        num_list = np.array([])
        if np.random.uniform() < self.epsilon:
            """self.epsilonよりもランダムに取ってきた値が小さかった場合、行動をランダムに選択する"""
            ran = random.randrange(len(choice_list_list))
            if self.epsilon>self.epsilon_min:
                self.epsilon = self.epsilon*self.epsilon_decay
        else:
            #perm_actions = random.choice(choice_list_list)
            """用意された選択肢についてそれぞれq値を求める"""
            for attack_amount, d_ in zip(attack_amount_list, d_list):
                #print(1+self.q_table[t][enemy_hitpoint][attack_amount][d_],"1+q_table")
                #if self.q_table[t][attack_amount][d_]<=0:
                if self.q_table[enemy_hitpoint][attack_amount]<=0:
                    num_list = np.append(num_list,0)
                else:
                    #num_list = np.append(num_list,self.q_table[t][attack_amount][d_])
                    num_list = np.append(num_list,self.q_table[enemy_hitpoint][attack_amount])
            if sum(num_list)>0:
                num_list = num_list/sum(num_list)
                ran = np.random.choice(range(len(choice_list_list)),p=num_list)
            else:
                """q値の最大値が高い行動程高い確率で選ばれるような仕組み"""
                ran = random.choice(range(len(choice_list_list)))

            self.f.write(str(num_list)+"num_list"+str(t)+"turn""\n")
            """その行動を返す"""
        return choice_list_list[ran], attack_amount_list[ran], d_list[ran]
    
    def q_fwrite(self):
        #self.f = open("q_table.txt","w+")
        #np.set_printoptions(threshold = 600000000)
        #self.f.write(str(self.q_table))
        #self.f.close()
        pass

if __name__ == '__main__':
    age = agent()
    age.q_fwrite()