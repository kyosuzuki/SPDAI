import copy, random
import draw, Enemy, debuff, card_use
from search import search
from card_use import card_play, card_use_h
searching = search()

class Battle(Enemy.Enemy):
    """実際に戦闘を行う"""
    def __init__(self):
        self.notice = 0
        self.c = 0
        self.b = 0
        

    def fight(self, energyre, deck, e, player_hp_):
        """人間の手によって戦闘を行う"""
        enemy_hitpoint = e.life()#敵の体力
        enemy_strength =0
        strength, dex = 0, 0
        debuffs = [0, 0, 0, 0, 0]#敵にかかる弱体脱力とプレイヤーの弱体脱力脆弱化をセットで扱う。
        player_hp = player_hp_
        power_stats = [0, [0,0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]#metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg

        damage_count = 0#血には血を用
        piles = [[],[],[],[]]#discard_pile, exhaust_pile, hand, draw_pile
        piles[3] = copy.copy(deck)
        random.shuffle(piles[3])
        ai = 0
        special_status = [0,0]#Malleable, Painful_stab
        for t in range(99):#tがターン数。99ターン以上をここでは考えない
            enemy_attack = 0
            enemy_count = 0
            enemy_attack, enemy_count, enemy_strength, sp = e.enemyaction(t, enemy_strength)
            special_status= Enemy.spnumber(sp, special_status)
            print(special_status)
            print("-----------------------------------")
            print(str(t+1)+"ターン目")
            print("あなたの体力:"+str(player_hp))
            if power_stats[7] == 0:
                block = 0#ターン開始時にブロックを0にする。バリケードが無ければ
            energy = energyre
            enemy_block = 0
            ew = 0#これが無いと敵にかけた脱力が複数回適応されてしまう
            yv = 0#プレイヤーが受けた弱体も同様
            
            piles = draw.draw(5, piles)
            while 1:#プレイヤーターンの内のプレイヤーが行動する時間。end_turnが押されるまでループする。
                print("--------------------")
                damage = 0
                count = 1
                """この周辺では敵についての処理をまず行う。"""
                enemy_attack, d, yv, ew = Enemy.damage_calculator(enemy_count, enemy_attack, debuffs,yv, ew, 0)

                print(e.name+"の残りHP:"+str(enemy_hitpoint))#相手の残り体力の表示
                Enemy.enemy_debuff(e.name, debuffs, enemy_block, ai)#相手のデバフ状況やブロックを表示
                
                """プレイヤーのターン"""
                """エナジーやデバフの表示"""
                debuff.debuf_block_energy(debuffs, block, energy, strength, dex, power_stats)
                """手札の表示"""
                i = 1
                for _ in piles[2]:
                    print(str(i)+":"+str(searching.seek(_)))
                    i += 1

                """カードを使用！"""
                """endか何も入力しなかったらターンエンド"""
                #num = input("使用するカードの番号を入力してください！")#\n-1と入力するとturn endします。\n-2と入力すると山札を見ます。\n-3と入力すると捨て札を見ます。
                num_ = input("使用するカードの番号を入力してください！")
                num = int(card_use.card_play(num_, piles))
                hand = piles[2]
                if num == -1:#ターンエンド
                    break
                elif num == -2:#山札を見たりした場合の処理
                    pass
                else:
                    if searching.seek_i(hand[num],1) == 'power':
                        """使用カードがパワーだった場合"""
                        
                        energy, piles, debuffs[1], strength, dex, power_stats, turn_end = card_use.power_use(hand[num], energy, piles, debuffs, strength, dex, power_stats)
                    else:
                        energy, piles, block, damage, debuffs, strength, dex, turn_end, count= card_use.card_use_h(searching.seek_i(hand[num],0),energy, piles, block, damage, debuffs, strength, dex, power_stats)

                """カード使用後の敵体力の減少の処理"""
                damage, enemy_block, enemy_hitpoint, special_status = Enemy.damage_deploy(damage, enemy_block, enemy_hitpoint, special_status, count)

                if enemy_hitpoint<=0:#敵の体力が0になった時の処理
                    break

            if enemy_hitpoint<=0:#敵の体力を0以下にしたときの処理 ループを抜ける
                break

            """ターン終了時に発動するパワー(金属化、燃焼）の処理を行う"""
            block, enemy_hitpoint, enemy_block, player_hp, strength, damage_count = debuff.turn_end_power(power_stats, block, enemy_hitpoint, enemy_block, player_hp, strength, damage_count)

            """手札を捨て札に送る処理。エセリアルや火傷、疑念や羞恥といったターン終了時に手札にある場合に発動する効果を処理する"""
            piles, player_hp, block, debuffs = draw.etherial(piles, player_hp, block, debuffs, power_stats)

            """敵の行動の処理"""
            player_hp, debuffs, piles = Enemy.damage_taken(enemy_attack, enemy_count, block, player_hp, debuffs, special_status, piles)

            """脱力弱体脆弱の処理"""
            debuffs = debuff.debuff_reduction(debuffs)

            """負けた時の処理"""
            if player_hp<0:
                print("lose......")
                break
            
            ew = 0#これが無いと敵にかけた脱力が複数回適応されてしまう
            yv = 0#プレイヤーが受けた弱体も同様

            """これを繰り返す"""
        
        print("体力が"+str(player_hp-75)+"変化しました\n残り体力:"+str(player_hp))