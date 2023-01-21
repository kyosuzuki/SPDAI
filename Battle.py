import random, copy, tqdm
import draw, Enemy, debuff, card_use, AI, graph_plot, q_learning_sts
from search import search
from card_use import card_play, card_use_h
from statistics import stdev, variance, median, mean

class Battle(Enemy.Enemy):
    """実際に戦闘を行う"""
    def __init__(self):
        self.notice = 0
        self.c = 0
        self.b = 0
    def ai_fight_3(self, energyre, deck, e, player_hp_, c):
                """モンテカルロ木の考え方を使用する。こちらでは本番のプレイを実行する。ai_fight_4でモンテカルロ木のために敵を倒すところまで未来の計算を行っている"""
                ai = 1#aiが0だと人力用の関数になる。
                """グラフ作成用に変数などを作成。"""
                y=[]#戦闘終了後の体力を入れる
                used_card2 = []
                f2 = open("used.txt", 'w+')
                love = AI.AI()

                with open('record.txt','w') as f:#戦闘の内容を書き込む
                    for I in tqdm.tqdm(range(c)):
                        player_hp = player_hp_
                        enemy_hitpoint = e.life()#敵の体力
                        enemy_strength =0
                        debuffs = [0, 0, 0, 0, 0]#enemy_vulnerable, vulnerable, enemy_weak, weak, frai
                        piles = [[],[],[],[]]#discard_pile, exhaust_pile, hand, draw_pile
                        piles[3] = copy.copy(deck)
                        random.shuffle(piles[3])
                        used_card2 = []

                        special_status = [0,0]#Malleable, Painful_stab
                        #回数分Enemyインスタンスを初期化して敵が毎回同じ行動をとることを防ぐ。
                        e2 = Enemy.Enemy()
                        e2.name = e.name
                        strength, dex = 0, 0
                        power_stats = [0, [0,0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]#metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg

                        for t in range(99):
                            #enemy_attack = 0
                            #enemy_count = 0
                            enemy_attack, enemy_count, enemy_strength, sp = e2.enemyaction(t, enemy_strength)
                            used_card = []
                            L = 0

                            special_status = Enemy.spnumber(sp, special_status)#敵の特殊性を記述する(弱体や脱力といった行動ではなく、本の負傷を与える行動など

                            f.write("\n"+str(t+1)+"ターン目\n")
                            f.write("あなたの体力:"+str(player_hp)+"\n")
                            block = 0#ターン開始時にブロックを0にする
                            energy = energyre
                            enemy_block = 0

                            ew = 0#これが無いと敵にかけた脱力が複数回適応されてしまう
                            yv = 0#プレイヤーが受けた弱体も同様


                            piles = draw.draw(5, piles)
                            while 1:#プレイヤーターンの内のプレイヤーが行動する時間。end_turnが押されるまでループする。
                                damage = 0
                                count = 1
                                """この周辺では敵についての処理をまず行う。"""
                                enemy_attack, d, yv, ew = Enemy.damage_calculator(enemy_count, enemy_attack, debuffs, yv, ew, f)

                                f.write(e2.name+"の残りHP:"+str(enemy_hitpoint)+"\n")#相手の残り体力の表示
                                Enemy.enemy_debuff(e2.name, debuffs, enemy_block, f)#相手のデバフ状況やブロックを表示

                                """プレイヤーのターン"""
                                """エナジーの表示"""
                                debuff.debuf_block_energy(debuffs, block, energy, strength, dex, power_stats, f)

                                """手札の表示"""
                                f.write("hand:"+str(piles[2])+"\n")

                                """カードを使用！"""
                                """endか何も入力しなかったらターンエンド"""
                                #piles_ = copy.deepcopy(piles)
                                cardname = love.monte(piles, energy, d, t, enemy_hitpoint, player_hp, block, debuffs, enemy_block, special_status, energyre, enemy_strength, strength, dex, power_stats, e2)#モンテカルロ木の探索を行う。
                                if cardname==-1:
                                    """ターンエンド"""
                                    break
                                else:
                                    used_card.append(cardname)

                                    if searching.seek_i(cardname,1) == 'power':
                                        """使用カードがパワーだった場合"""
                                        energy, piles, debuffs[1], strength, dex, power_stats, turn_end = card_use.power_use(cardname, energy, piles, debuffs, strength, dex, power_stats)
                                    else:
                                        energy, piles, block, damage, debuffs, strength, dex, turn_end, count= card_use.card_use_h(cardname,energy, piles, block, damage, debuffs, strength, dex, power_stats)

                                """カード使用後の敵体力の減少の処理"""
                                damage, enemy_block, enemy_hitpoint, special_status = Enemy.damage_deploy(damage, enemy_block, enemy_hitpoint, special_status, count)

                                if turn_end == True:
                                    print("turn_end == Trueのエラー")
                                    break
                                if enemy_hitpoint<=0:#敵の体力が0になった時の処理
                                    break
                            
                            f.write("\n使用したカード:"+str(used_card)+"\n----------\n")

                            if enemy_hitpoint<=0:#敵の体力を0以下にしたときの処理 ループを抜ける
                                break
                            """手札を捨て札に送る処理。エセリアルや火傷、疑念や羞恥といったターン終了時に手札にある場合に発動する効果を処理する"""
                            piles, player_hp, block, debuffs = draw.etherial(piles, player_hp, block, debuffs, power_stats)

                            """敵の行動の処理"""
                            player_hp, debuffs, piles= Enemy.damage_taken(enemy_attack, enemy_count, block, player_hp, debuffs, special_status, piles, f)

                            """脱力弱体脆弱の処理"""
                            debuffs = debuff.debuff_reduction(debuffs)
                            """負けた時の処理"""
                            if player_hp<=0:
                                f.write("lose......\n")
                                break
                            
                            ew = 0#これが無いと敵にかけた脱力が複数回適応されてしまう
                            yv = 0#プレイヤーが受けた弱体も同様

                            """これを繰り返す"""

                        f.write("\n体力が"+str(player_hp-player_hp_)+"変化しました\n残り体力:"+str(player_hp)+"\n--------------------------------\n")
                        """統計処理用に被害量をyに入れておく"""
                        y.append(player_hp-75)
                        f2.write(str(y[I])+":"+str(used_card2)+"\n")#(被害量):(used_card2)という形

                    f2.close()
                    graph_plot.statistics_for_monte(f, y)
    def ai_fight_4(self, piles_, energy,energyre,  damage, block, enemy_block, debuffs_,enemy_strength, special_status_, enemy_hitpoint_, player_hp_, enemyname, cardname_, t_, e, strength_, dex_, power_stats, c):
            """モンテカルロ木の探索のために仮想戦闘を行う"""
            """c回戦闘を行いその平均被害を算出する"""
            used_card = []
            y  =[]#グラフを書いたりはしないが、平均被害を求めるために必要
            f2 = open("used_2.txt", 'a')
            metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats
            with open('record_2.txt','a') as f:#デッキの内容を書き込む
                for I in range(c):
                    enemy_hitpoint = enemy_hitpoint_
                    player_hp = player_hp_
                    piles = copy.deepcopy(piles_)
                    debuffs = debuffs_
                    strength, dex = strength_, dex_
                    power_stats = metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg
                    way = []
                    random.shuffle(piles[3])
                    used_card2 = []
                    L2 = 0
                    special_status = special_status_
                    t = t_
                    while t<99:#tがターン数。99ターン以上をここでは考えない
                        count = 1
                        energy = energyre
                        L = 0
                        used_card = []
                        ew = 0#これが無いと敵にかけた脱力が複数回適応されてしまう
                        yv = 0#プレイヤーが受けた弱体も同様
                        if L2 == 0:
                            """最初に指定されたカードを使用し:どのような結果になるのか観測し、そこから戦闘を始める。"""
                            enemy_attack, enemy_count, enemy_strength, sp = e.enemyaction(t, enemy_strength)
                            cardname = cardname_
                            f.write(str(cardname)+"を使用した場合\n")
                            if searching.seek_i(cardname,1) == 'power':
                                """使用カードがパワーだった場合"""
                                energy, piles, debuffs[1], strength, dex, power_stats, turn_end = card_use.power_use(cardname, piles, debuffs,strength, dex, power_stats)
                            else:
                                energy, piles, block, damage, debuffs, strength, dex, turn_end, count= card_use.card_use_h(cardname, energy, piles, block, damage, debuffs, strength, dex, power_stats)
                            """カード使用後の敵体力の減少の処理"""
                            damage, enemy_block, enemy_hitpoint, special_status= Enemy.damage_deploy(damage, enemy_block, enemy_hitpoint, special_status, count)
                            L2+=1
                        else:
                            t +=1
                            enemy_attack, enemy_count, enemy_strength, sp = e.enemyaction(t, enemy_strength)
                            special_status = Enemy.spnumber(sp, special_status)#敵の特殊性を記述する
                            f.write(str(t+1)+"ターン目\n")
                            f.write("あなたの体力:"+str(player_hp)+"\n")
                            block = 0#ターン開始時にブロックを0にする
                            energy = energyre
                            enemy_block = 0
                            draw.draw(5,piles)

                        if enemy_hitpoint<=0:#敵の体力が0になった時の処理
                            break
                        
                        while 1:#プレイヤーターンの内のプレイヤーが行動する時間。end_turnが押されるまでループする。
                            #f.write("--------------------")
                            damage = 0
                            """この周辺では敵についての処理をまず行う。"""
                            enemy_attack, d, yv, ew = Enemy.damage_calculator(enemy_count, enemy_attack, debuffs, yv, ew, f)
                            f.write(e.name+"の残りHP:"+str(enemy_hitpoint)+"\n")#相手の残り体力の表示
                            Enemy.enemy_debuff(e.name, debuffs, enemy_block, f)#相手のデバフ状況やブロックを表示
                            """プレイヤーのターン"""
                            """バフデバフやエナジーの表示"""
                            debuff.debuf_block_energy(debuffs, block, energy, strength, dex, power_stats, f)
                            """手札の表示"""
                            f.write("hand:"+str(piles[2])+"\n")
                            """カードを使用！"""
                            if L == 0:#そのターンのはじめだけwayの導出を行う。リストwayには使用カードが入っておりそれに従って行動する
                                way = AI.path_gain(d, piles[2], energy)
                                f.write(str(way))
                                L=1
                            
                            if (len(way) == 0):
                                """ターンエンド"""
                                break
                            elif len(way)>0:
                                cardname = way[0]
                                used_card.append(cardname)
                                f.write(searching.seek_i(way[0],0)+"を使用\n")#使用カードを記述
                                if searching.seek_i(cardname,1) == 'power':
                                        """使用カードがパワーだった場合"""
                                        energy, piles, debuffs[1], strength, dex, power_stats, turn_end = card_use.power_use(cardname, energy, piles, debuffs, strength, dex, power_stats)
                                else:
                                    energy, piles, block, damage, debuffs, strength, dex, turn_end, count= card_use.card_use_h(cardname, energy, piles, block, damage, debuffs, strength, dex, power_stats)
                                way.pop(0)
                                """カード使用後の敵体力の減少の処理"""
                                damage, enemy_block, enemy_hitpoint, special_status = Enemy.damage_deploy(damage, enemy_block, enemy_hitpoint, special_status, count)
                            if turn_end:
                                break
                            if enemy_hitpoint<=0:#敵の体力が0になった時の処理
                                break
                        f.write("\n"+str(used_card)+"\n")
                        used_card2.append(used_card)#used_card2にused_cardを記録する。
                        """手札を捨て札に送る処理。エセリアルや火傷、疑念や羞恥といったターン終了時に手札にある場合に発動する効果を処理する"""
                        piles, player_hp, block, debuffs = draw.etherial(piles, player_hp, block, debuffs, power_stats)
                        """敵の行動の処理"""
                        player_hp, debuffs, piles= Enemy.damage_taken(enemy_attack, enemy_count, block, player_hp, debuffs, special_status, piles, f)

                        """脱力弱体脆弱の処理"""
                        debuffs = debuff.debuff_reduction(debuffs)
                        
                        """負けた時の処理"""
                        if player_hp<0:
                            f.write("lose......\n")
                            break
                        
                        ew = 0#これが無いと敵にかけた脱力が複数回適応されてしまう
                        yv = 0#プレイヤーが受けた弱体も同様

                        """これを繰り返す"""

                    f.write("体力が"+str(player_hp-75)+"変化しました\n")
                    y.append(player_hp-75)
                f2.close()
                return mean(y)

searching = search()
