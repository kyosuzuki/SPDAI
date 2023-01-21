from search import search
import q_learning_sts
import random, copy, collections
import AI, Battle
from search import search
from card_use import card_play, card_use_h
searching = search()

class AI:#aiの頭脳。敵の名前、エナジー、ハンドの情報から行動を算出する。
    def __init__(self):
        #global #energy, hand
        #self.energy = energy
        #self.hand = hand
        self.age = q_learning_sts.agent()


    def ai_commandor(self,d,i,command, deck, hand, energy, memory):
        """ランダムにaiのbrainを切り替える"""
        usable_list = []#使用するカードの候補をこのリストに入れる。エナジーが足りないカードはここに入れない。
        for i in range (len(hand)):
            if (energy>=int(searching.seek_i(hand[i],2))) and (d*2>=int(searching.seek_i(hand[i],4))):#usable_listに入れる条件は2つ。1つ目はそのカードを使用できるエナジーを持っていること、2つ目は過剰ブロックでないこと。過剰ブロックかどうかはdの2倍との大きさの比較で求める。
                usable_list.append(searching.seek_i(hand[i],0))
        #print(usable_list)
        #number = AI.ai_brain_1(self)
        if len(usable_list) == 0:
            return '-1'
        a = random.random()

        if a>command:#iを無限大に大きくしていくと1に収束していく関数を用いる。iの値が増えれば増える程この条件式がtrueを返す確率は減る。
            number = love.random_ai(hand, usable_list)#即ち、試行回数が少ないうちはランダムな方から選ばれやすく、試行回数が増えてくるとai_brain_2から選ばれる確率が上がる。
        else:
            number = love.ai_brain_2(hand, usable_list, memory)

        return number

    def random_ai(self, hand, usable_list):#使用できるカードの中から完全にランダムにカードを選択するai_brain
        #if len(usable_list) == 0:
        #    return '-1'
        ran = random.randrange(len(usable_list))#usable_listのlenの範囲内のランダムな値を入手
        #print(str(usable_list)+"usable_listだよ")
        #print(ran)
        #print(searching.seek_i(usable_list[ran],0)+"を使用するよ")
        #print(hand)
        #print(usable_list[ran])
        ran = hand.index(usable_list[ran])
        #print(ran)
        return ran+1
    
    def ai_brain_1(self, hand, energy,d):#一つ目のai_brain,人間が指定した特定のカードを持っていたら出来る限り使用する。
        path2 = 'strong_card_data.txt'
        usable_list = []#使用するカードの候補をこのリストに入れる。エナジーが足りないカードはここに入れない。
        for i in range (len(hand)):
            if (energy>=int(searching.seek_i(hand[i],2))) and (d*2>=int(searching.seek_i(hand[i],4))):#usable_listに入れる条件は2つ。1つ目はそのカードを使用できるエナジーを持っていること、2つ目は過剰ブロックでないこと。過剰ブロックかどうかはdの2倍との大きさの比較で求める。
                usable_list.append(searching.seek_i(hand[i],0))
        with open(path2) as f:
            lines2 = f.readlines()
            lines_stripe2 = [line.strip() for line in lines2]
            strong_card = []
            for i in range(len(hand)):
                strong_card+=([s for s in lines_stripe2 if searching.seek_i(hand[i],0) in s])#strong_card_data.txtに最優先で使わせたいカードを記述しておき、ここで読み込ませる。
                #print(strong_card)
                #try:
                #    strong_card.remove([])
                #except:
                #    pass
            try:
                strong_card[0]!=''
                #print(strong_card[0])
                #print(hand)
                num = hand.index(strong_card[0])
                return num
            except:
                #return love.random_ai()
                return -1
            #print(card)
            #card = str(card).split()
            #print(card)
    def ai_brain_2(self, hand, usable_list, memory):#2つ目のai_brain 戦闘結果の良い記録がどのカードを使用していたのかに注目する。
        candidate = []#使用候補を入れる
        for i2 in range (len(usable_list)):#usable_listの中にmemoryと一致するカードがあった場合使用候補に入れる。使用候補からランダムな値を入力する
            #print(usable_list[i2]+"i2はこれ")
            #print(usable_list)
            #print(memory,"memory")
            cand = usable_list[i2]
            if ((cand in memory)):
                candidate.append(cand)#使用可能リストにmemoryに含まれるカードがあったら使用候補candidateに入れる。
        #print(str(candidate)+"candidateだよ")
        if len(candidate)>0:#candidateが0より大きい場合はその中からランダムな値を返す。
            num = candidate[random.randrange(0,len(candidate))]
            #print(str(hand.index(num))+"を使用")
            #print("ai_brain_2を使用")
            #print(hand.index(num))
            return hand.index(num)+1
        return love.random_ai(hand, usable_list)

    def path_gain_2(self, d, hand, energy, t, enemy_hitpoint,count = 5):
        """ハンドから使用できるカードの並び順をランダムに指定された数(count)選出する。初期状態ではcountは30"""
        """attack_amountとblock_amountにそのカード群を並び順通りに使用した際のダメージ量とブロック量を入れる。"""
        """その後そのターン数でのアタック量とd-block_amountについてq値をq_learning_stsより計算させ、最終的にq値が高いものを選択させる"""
        usable_list = []#使用するカードの候補をこのリストに入れる。エナジーが足りないカードはここに入れない。
        #estimate_list = []
        choice_list_list = []
        attack_amount_list = []
        d_list = []
        #choice_np = np.zeros((count,3))
        #print(choice_np.shape)
        for _ in range (count):
            hand_ = copy.copy(hand)
            energy_ = energy
            d_ = d
            choice_list = []
            attack_amount = 0
            block_amount = 0
            while 1:
                for i in range (len(hand_)):
                    if (energy_>=int(searching.seek_i(hand_[i],2))) and (d_*2>=int(searching.seek_i(hand_[i],4))):#usable_listに入れる条件は2つ。1つ目はそのカードを使用できるエナジーを持っていること、2つ目は過剰ブロックでないこと。過剰ブロックかどうかはdの2倍との大きさの比較で求める。
                        usable_list.append(searching.seek_i(hand_[i],0))
                if len(usable_list)==0:
                    break
                """ここでは、usable_listの中からランダムに1枚選択、そのカードのエナジー分エナジーを減らしてまたusable_listを作成・・・・・・を繰り返し、usable_listが0になるまで続ける"""
                #print(usable_list)
                choice = random.choice(usable_list)
                #print(choice)
                choice_list.append(choice)
                hand_.remove(choice)
                energy_-=int(searching.seek_i(choice,2))

                d_-=int(searching.seek_i(choice,4))
                attack_amount+=int(searching.seek_i(choice,3))
                block_amount+=int(searching.seek_i(choice,4))
                usable_list.clear()

            if d_<0:
                    d_ = 0
            choice_list_list.append(choice_list)
            attack_amount_list.append(attack_amount)
            d_list.append(d_)

        way = self.age.choose_action(t, attack_amount_list, d_list, choice_list_list, enemy_hitpoint)
        #print(way)
        return way

    def path_gain(self, d, hand, energy, t, enemy_hitpoint,count = 10):
        """ハンドから使用できるカードの並び順をランダムに指定された数(count)選出する。"""
        """attack_amountとblock_amountにそのカード群を並び順通りに使用した際のダメージ量とブロック量を入れる。"""
        """最終的にestimateという多変数一次多項式で最も適したプレイを決定する。"""
        usable_list = []#使用するカードの候補をこのリストに入れる。エナジーが足りないカードはここに入れない。
        estimate_list = []
        choice_list_list = []
        attack_amount_list, d_list = [],[]
        strong_cardplay_list, s_attack_amount_list, s_d_list = [],[],[]#最終的に選ばれた候補をここに入れてchoose_actionに渡す。
        tact = [(0.8,0.2),(0.2,0.8),(0.5,0.5),(1.5,0),(0,1.5)]
        for tact0,tact1 in tact:
            for _ in range (count):
                hand_ = copy.copy(hand)
                energy_ = energy
                d_ = d
                choice_list = []
                attack_amount = 0
                block_amount = 0
                while 1:
                    for i in range (len(hand_)):
                        if (energy_>=int(searching.seek_i(hand_[i],2))) and (d_*2>=int(searching.seek_i(hand_[i],4))):#usable_listに入れる条件は2つ。1つ目はそのカードを使用できるエナジーを持っていること、2つ目は過剰ブロックでないこと。過剰ブロックかどうかはdの2倍との大きさの比較で求める。
                            usable_list.append(searching.seek_i(hand_[i],0))
                    if len(usable_list)==0:
                        break
                    """ここでは、usable_listの中からランダムに1枚選択、そのカードのエナジー分エナジーを減らしてまたusable_listを作成・・・・・・を繰り返し、usable_listが0になるまで続ける"""
                    #print(usable_list)
                    choice = random.choice(usable_list)
                    #print(choice)
                    choice_list.append(choice)
                    hand_.remove(choice)
                    energy_-=int(searching.seek_i(choice,2))
                    d_-=int(searching.seek_i(choice,4))
                    if d_<0:
                        d_ = 0
                    attack_amount+=int(searching.seek_i(choice,3))
                    
                    block_amount+=int(searching.seek_i(choice,4))
                    
                    usable_list.clear()
                """choice_listにプレイの選択肢をcountの数だけ入れる。それをestimateという多変数一次多項式で評価し、最もestimateの値が高いものを最終的なプレイとして決定する。"""
                #print(_,choice_list)
                choice_list_list.append(choice_list)
                attack_amount_list.append(attack_amount)
                d_list.append(d_)
                #print(attack_amount, block_amount)
          #      print(attack_amount,"×",tact0,"+",block_amount,"×",tact1)
                
                estimate = attack_amount*tact0+block_amount*tact1
         #       print(estimate)
                estimate_list.append(estimate)
            #print(estimate_list)
            new_estimate = sorted(estimate_list, reverse =True)#estimateして求めた値が最も大きいものをnew_estimateに入れる。
            key_to_victory = estimate_list.index(new_estimate[0])
            strong_cardplay_list.append(choice_list_list[key_to_victory])
            s_attack_amount_list.append(attack_amount_list[key_to_victory])
            s_d_list.append(d_list[key_to_victory])
        #print(strong_cardplay_list)
        way = self.age.choose_action(t, s_attack_amount_list, s_d_list, strong_cardplay_list, enemy_hitpoint)
        #print(way)
        #print(hand, "hand")
        return way

    def monte(self, piles_, energy,d, t, enemy_hitpoint, player_hp, block, debuffs, enemy_block, special_status, energyre, enemy_strength, strength, dex, power_stats, e, c = 10,damage = 0):
        """usable_listを求めた後、それぞれについて未来の展開を予測し、最も良い結果をもたらすカードを選択させる。"""
        
        energy_ = energy
        d_ = d
        t_ = t
        enemy_hitpoint_ = enemy_hitpoint
        player_hp_ = player_hp
        block_ = block
        enemy_block_ = enemy_block
        damage_ = damage
        #piles_ = copy.copy(piles)
        enemy_strength_ = enemy_strength
        enemyname = e.name
        usable_list = make_usablelist(piles_, energy_, d_)
        battle = Battle.Battle()
        mean_y_list = []
        metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats

        if len(usable_list) > 0:
            for card_name in usable_list:
                piles = copy.deepcopy(piles_)
                power_stats = metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg
                mean_y = battle.ai_fight_4(piles, energy_,energyre, damage_, block_, enemy_block_, debuffs, enemy_strength_, special_status, enemy_hitpoint_, player_hp_,enemyname, card_name, t_, e, strength, dex, power_stats, c)
                mean_y_list.append(mean_y/c)
            chooseon_card = usable_list[mean_y_list.index(max(mean_y_list))]
        elif len(usable_list) == 0:
            chooseon_card = -1
        return chooseon_card

    def bridge(self, turn,enemy_hp, attack, d_block, r, next_t, next_hp, done):
        env = turn,enemy_hp, attack, d_block, r, next_t,next_hp, done
        return self.age.q_learn(env)
    
    def bridge_2(self):
        return self.age

def make_usablelist(piles, energy, d):
    """usable_listを作成する。ハンド内の使う価値のある、使えるカードのリストである。"""
    hand = piles[2]
    usable_list = []
    hand_ = copy.copy(hand)
    energy_ = energy
    d_ = d
    for i in range (len(hand_)):
        if (energy_>=int(searching.seek_i(hand_[i],2))) and (d_*2>=int(searching.seek_i(hand_[i],4))):#usable_listに入れる条件は2つ。1つ目はそのカードを使用できるエナジーを持っていること、2つ目は過剰ブロックでないこと。過剰ブロックかどうかはdの2倍との大きさの比較で求める。
            usable_list.append(searching.seek_i(hand_[i],0))
            
    return list(set(usable_list))#重複するものを削除し返す
            
def dict_ratio(card_name, deck, deck_count):
    """deck_countから、第1引数に指定されたカードがデッキに占める割合を求める"""
    return deck_count[card_name]/len(deck)


def study(y2, used_card2, I, f3, deck):#aiが学習するための関数。被害を少なかった順に並べたデータy2と、被害データとその時の使用カードが紐づかれたused_card2、試行回数Iを引数にとり、memory.txtに学習内容を記録させる。
    deck_count = collections.Counter(deck)


    S = (I+1)/5#SはIを5で割ったものとする。y2の上位S個のデータから学習を行う。
    lines_good_play = []
    #global memory
    memory = []
    with open('used.txt', 'r') as f4:#used.txtから使用したカードを読み取り、被害の少なかった上位S個のデータをlines_good_playに送る。
        lines = f4.readlines()
        lines_stripe3 = [line.strip() for line in lines]
    #print(lines_stripe3)
    #print(lines_stripe3[0])
    for i3 in range(int(S)):#同じ被害量のデータがあると重複が発生するため変なif文で抑えている。
        if ((i3>0)and(y2[i3] != y2[i3-1])) or (i3 ==0):
            lines_good_play.append([line_s for line_s in lines_stripe3 if str(y2[i3]) in line_s])
            #print(len(lines_good_play))
        else:
            pass
    #print(lines_good_play)
    m = 0#数を数えるための変数。lines_good_playにある使用カードの合計を入れる
    for di in deck_count:
        m +=str(lines_good_play).count(str(di))
        #dict_ratio(deck_count, di)
        #print(di)
    for di in deck_count:
        
        m2 = str(lines_good_play).count(di)/m#m2にlines_good_playでのdiの割合を求める。
        #print(str(di) + ":"+str(m2))
        #print(dict_ratio(di,deck, deck_count), m2, "dict_Ratioとm2")
        if (m2>dict_ratio(di,deck, deck_count)) and ((di!='strike' )and(di!='defend')and(di!='bash')):
            #print(dict_ratio(deck_count,di))
            #print("このカードは強い！"+di)
            #f3.write(di)
            memory.append(di)
    #f2.close()
    #print(memory)
    return memory

def path_gain(d, hand, energy, count = 10, tact=(1,1)):
    """ハンドから使用できるカードの並び順をランダムに指定された数(count)選出する。初期状態ではcountは30"""
    """attack_amountとblock_amountにそのカード群を並び順通りに使用した際のダメージ量とブロック量を入れる。"""
    """最終的にestimateという多変数一次多項式で最も適したプレイを決定する。"""
    usable_list = []#使用するカードの候補をこのリストに入れる。エナジーが足りないカードはここに入れない。
    estimate_list = []
    choice_list_list = []
    for _ in range (count):
        hand_ = copy.copy(hand)
        energy_ = energy
        d_ = d
        choice_list = []
        attack_amount = 0
        block_amount = 0
        while 1:
            for i in range (len(hand_)):
                if (energy_>=int(searching.seek_i(hand_[i],2))) and (d_*2>=int(searching.seek_i(hand_[i],4))):#usable_listに入れる条件は2つ。1つ目はそのカードを使用できるエナジーを持っていること、2つ目は過剰ブロックでないこと。過剰ブロックかどうかはdの2倍との大きさの比較で求める。
                    usable_list.append(searching.seek_i(hand_[i],0))
            if len(usable_list)==0:
                break
            """ここでは、usable_listの中からランダムに1枚選択、そのカードのエナジー分エナジーを減らしてまたusable_listを作成・・・・・・を繰り返し、usable_listが0になるまで続ける"""
            choice = random.choice(usable_list)
            choice_list.append(choice)
            hand_.remove(choice)
            energy_-=int(searching.seek_i(choice,2))
            d_-=int(searching.seek_i(choice,4))
            attack_amount+=int(searching.seek_i(choice,3))
            block_amount+=int(searching.seek_i(choice,4))
            usable_list.clear()
        """choice_listにプレイの選択肢をcountの数だけ入れる。それをestimateという多変数一次多項式で評価し、最もestimateの値が高いものを最終的なプレイとして決定する。"""
        choice_list_list.append(choice_list)
        estimate = attack_amount*tact[0]+block_amount*tact[1]
        estimate_list.append(estimate)
    new_estimate = sorted(estimate_list, reverse =True)
    key_to_victory = estimate_list.index(new_estimate[0])
    way = choice_list_list[key_to_victory]
    return way


if __name__ == "__main__":
    love = AI()
    d = 24
    hand = ["bash","strike","def","strike","impervious"]
    energy = 3
    t = 0
    enemy_hitpoint = 75
    a = AI()
    a.path_gain_2(d,hand,energy,t, enemy_hitpoint)
        
