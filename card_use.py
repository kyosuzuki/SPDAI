from search import search
import math, copy
import draw
searching = search()
def card_play(num, piles, f = 0):
    """カードを使用する際にプレイヤーに数字を入力させる時の処理を考える。プレイヤーが操作する場合のみ考える。AIの場合は全く別の関数を使用する"""
    discard_pile, exhaust_pile, hand, draw_pile = piles
    if f == 0:
        if (num == '-1')or(num == ''):
            print("end turn")
            return -1
        elif num == '-2':
            print("山札は以下の通りです。\n"+str(draw_pile))
            return -2
        elif num == '-3':
            print("捨て札は以下の通りです。\n"+str(discard_pile))
            return -2
        elif num == '-4':
            print("廃棄したカードは以下の通りです\n"+str(exhaust_pile))
            return -2
        else:
            try:#全く別の番号を入力されてもエラーが起きないようにする
                num = int(num) - 1
                print(searching.seek_i(hand[num],0))
                return num
            except:
                return -2
    else:
        if num == '-1':
            f.write("turn end\n")
            return -1
        else:
            num = int(num) - 1
            f.write(searching.seek_i(hand[num],0)+"\n")
            return num

def card_use_h(card_name, 
energy, 
piles,
block, 
damage, 
debuffs,
strength, dex,
power_stats,
used_card = []):#カードを使用する時の処理を書く   
    metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats
    enemy_vulnerable, vulnerable, enemy_weak, weak, frail = debuffs
    damage = 0
    count = 1
    done = False
    #print(str(card_name)+"を使用します")
    discard_pile, exhaust_pile, hand, draw_pile = piles
    energy -= int(searching.seek_i(card_name,2))
    if energy<0:
        energy+= int(searching.seek_i(card_name,2))
        print("エナジーが足りない！")
        return energy, piles, block, damage, debuffs, strength, dex, True, count
    copycat = copy.copy(card_name)#リスト回りの面倒な仕様を警戒
    used_card.append(copycat)#used_cardに使用したカードを追加する。
    if searching.seek_i(card_name,6) == str(12):#ボディスラム
        damage = block
    elif "twin_strike" in card_name:
        count = 2
    elif card_name == "sword_boomerang":
        count = 3
    elif (card_name == "sword_boomerang+") or (card_name == "pummel"):
        count = 4
    elif card_name == "pummel+":
        count= 5
    elif "entrench" in card_name:
        block *= 2
    elif "limit_break" in card_name:
        strength *= 2
    elif "heavy_blade" in card_name:#ヘビーブレードの処理
        heavy = 3
        if "+" in card_name:
            heavy = 5
        damage += int(searching.seek_i(card_name,3)) + strength*heavy
        if enemy_vulnerable>0:
            damage = (damage*1.5)#敵が弱体を持っていた場合のダメージ増加処理をこちらで行う。脱力も同様
        if weak>0:
            damage = damage*0.75
        damage = math.floor(damage)
        done = True
    elif "perfected_strike" in card_name:
        strike_count = 0
        for _ in discard_pile:
            if "strike" in _:
                strike_count +=1 
        for _ in hand:
            if "strike" in _:
                strike_count +=1 
        for _ in draw_pile:
            if "strike" in _:
                strike_count += 1
        if card_name == "perfected_strike+":
            damage = 6 + 3*strike_count + strength
        else:
            damage = 6 + 2*strike_count + strength
        if enemy_vulnerable>0:
            damage = (damage*1.5)#敵が弱体を持っていた場合のダメージ増加処理をこちらで行う。脱力も同様
        if weak>0:
            damage = damage*0.75
        damage = math.floor(damage)
        done = True
    elif searching.seek_i(card_name,6) == str(15):#霊魂切断、セカンドウインド
        take_away = card_name#swが自分自身を廃棄してしまう為避難させる
        hand.remove(card_name)
        p_exhaust = []
        for _ in hand:
            if (searching.seek_i(_,1) != "attack"):
                count+=1
                p_exhaust.append(_)
        exhaust_pile.append(p_exhaust)
        for x in range(len(p_exhaust)):
            hand.remove(p_exhaust[x])
        if dark_emb>0:#闇の抱擁でドロー
            draw.draw(dark_emb*len(p_exhaust), piles)
        hand.append(take_away)
        if card_name == "second_wind":
            block, damage, done = special_card("sw",  block, damage, enemy_vulnerable, enemy_weak, weak, frail, strength, dex, count)
        elif card_name == "second_wind+":
            block, damage, done = special_card("sw",  block, damage, enemy_vulnerable, enemy_weak, weak, frail, strength, dex, count)
    elif "dropkick" in card_name:
        if enemy_vulnerable>0:
            energy+=1
            draw.draw(1,piles)

    if done == False:#special_cardで処理した場合ここはすべてスキップする
        if searching.seek_i(card_name,1) == "attack":
            damage += int(searching.seek_i(card_name,3)) + strength
        if enemy_vulnerable>0:
            damage = (damage*1.5)#敵が弱体を持っていた場合のダメージ増加処理をこちらで行う。脱力も同様
        if weak>0:
            damage = damage*0.75
        damage = math.floor(damage)
        if frail>=1 and int(searching.seek_i(card_name,4))>0:
            block += math.floor((int(searching.seek_i(card_name,4))+dex)*0.75)
        else:
            block += int(searching.seek_i(card_name,4))+dex
        #print(searching.seek_i(card_name,6))
        #これは改善が必要だと思うが、弱体や脱力などの特殊効果をどのように処理していいのか分からなかったため雑に記述している。card_nameの6番目の情が1だと弱体2（強打)、2だと弱体3(強打+)、3だと脱力2(ラリアット)・・・・・・と続いていく
        if searching.seek_i(card_name,6) ==str(1):#強打、サンダークラップ
            if card_name == "bash":
                enemy_vulnerable+=2
            elif card_name == "bash+":
                enemy_vulnerable+=3
            elif "thunderclap" in card_name:
                enemy_vulnerable += 1
        elif searching.seek_i(card_name,6) ==str(2):
            pass
        elif searching.seek_i(card_name,6) ==str(3):#ラリアット
            enemy_weak+=2
        elif searching.seek_i(card_name,6) ==str(4):#ラリアット+
            enemy_weak+=3
        elif searching.seek_i(card_name,6) ==str(5):#アッパーカット
            enemy_vulnerable +=1
            enemy_weak +=1
        elif searching.seek_i(card_name,6) ==str(6):#アッパーカット+
            enemy_vulnerable +=2
            enemy_weak +=2
        elif searching.seek_i(card_name,6) ==str(7):#衝撃波
            enemy_vulnerable +=3
            enemy_weak +=3
        elif searching.seek_i(card_name,6) ==str(8):#衝撃波+
            enemy_vulnerable +=5
            enemy_weak +=5
        elif searching.seek_i(card_name,6) == str(9):#キャントリップ 1ドロー
            draw.draw(1, piles)
        elif searching.seek_i(card_name,6) == str(10):#2ドロー
            draw.draw(2, piles)
        elif searching.seek_i(card_name,6) == str(11):#怒り, 焼身
            if "anger" in card_name:
                discard_pile.append(card_name)
            elif "immolate" in card_name:
                discard_pile.append('burn')
        elif searching.seek_i(card_name,6) == str(13):#ワイルドストライク, 無謀なる突進
            if "wild_strike" in card_name:
                draw_pile.append('wound')
            elif "reckless_charge" in card_name:
                draw_pile.append('dazed')
        elif searching.seek_i(card_name,6) == str(14):#やせ我慢
            hand.append('wound')
            hand.append('wound')
    ex = searching.seek_i(card_name,7)
    if "exhaust" in ex:#使用後に廃棄される処理
        exhaust_pile.append(card_name)
        if dark_emb>0:#闇の抱擁でドロー
            draw.draw(dark_emb, piles)
    else:
        discard_pile.append(card_name)
    try:
        hand.remove(card_name)
    except:
        pass
    debuffs = [enemy_vulnerable, vulnerable, enemy_weak, weak, frail
    ]
    piles = [discard_pile, exhaust_pile, hand, draw_pile]
    return energy, piles, block, damage, debuffs, strength, dex, False, count

def power_use(card_name, 
    energy, 
    piles, 
    debuffs,
    strength, dex,
    power_stats,
    used_card = []):
    
    """パワーを使用する際に使う関数、card_use_hと異なる点として、使用したカードを消滅させる。また、引数に特殊な値を取る。"""
    metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats
    count = 0
    vulnerable  =debuffs[1]
    discard_pile, exhaust_pile, hand, draw_pile = piles
    energy -= int(searching.seek_i(card_name,2))
    if energy<0:
        energy+= int(searching.seek_i(card_name,2))
        #print("エナジーが足りない！")
        return energy, piles, vulnerable, strength, dex, power_stats, True
    
    if card_name == "inflame":#発火
        strength+=2
    elif card_name == "inflame+":
        strength+=3
    elif card_name == "metallicize":
        metal+=3
    elif card_name == "metallicize+":
        metal+=4
    elif card_name == "combust":
        combust[0]+=5#combust[0]は攻撃力、combust[1]は自傷の量
        combust[1]+=1
    elif card_name == "combust+":
        combust[0]+=7
        combust[1]+=1
    elif "dark_embrace" in card_name:
        dark_emb+=1
    elif "barricade" in card_name:
        print("barricade")
        barr = 1
    power_stats = [metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg]
    hand.remove(card_name)
    piles = [discard_pile, exhaust_pile, hand, draw_pile]
    return energy, piles, vulnerable, strength, dex, power_stats, False

def special_card(card_name, block, damage, enemy_vulnerable, enemy_weak, weak, frail, strength, dex, count):
    """セカンドウインドなどをこちらで処理する"""
    if int(searching.seek_i(card_name,4))>0:
        if (frail > 0):
            block += math.floor((int(searching.seek_i(card_name,4))+dex)*0.75)*count
        else:
            block += (int(searching.seek_i(card_name,4))+dex)*count
    
    if int(searching.seek_i(card_name,3)) >0:
        damage += int(searching.seek_i(card_name,3)) + strength
        if enemy_vulnerable>0:
            damage = (damage*1.5)#敵が弱体を持っていた場合のダメージ増加処理をこちらで行う。脱力も同様
        if weak>0:
            damage = damage*0.75
        damage = math.floor(damage)*count

    return  block, damage, True
    

