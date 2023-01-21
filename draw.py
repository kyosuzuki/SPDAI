import random, copy
from search import search

searching = search()
def draw(d, piles):
    """第一変数にドロー枚数を与えて、山札からd枚ドローさせる関数。途中で山札が0になったらdiscard_pileをdraw_pileにする。"""
    discard_pile, exhaust_pile, hand, draw_pile = piles
    for i in range(d):
        if len(hand)==10:#手札が10枚になったらドローしない
            break
        if len(draw_pile) ==0:
            draw_pile = discard_pile
            random.shuffle(draw_pile)
            discard_pile = []
            if len(draw_pile)==0:
                #print("カードが無い！")#山札と捨て札両方とも0の時の処理
                break
        hand.append(draw_pile[0])
        del draw_pile[0]   
    piles = [discard_pile, exhaust_pile, hand, draw_pile]
    return piles   

def etherial(piles, player_hp, block, debuffs, power_stats):
    """手札を捨て札に送る処理。エセリアルや火傷、疑念や羞恥といったターン終了時に手札にある場合に発動する効果を処理する"""
    discard_pile, exhaust_pile, hand, draw_pile = piles
    metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats
    c = len(hand)
    i = 0
    enemy_vulnerable, vulnerable, enemy_weak, weak, frail = debuffs
    count = 0#エセリアルで廃棄された数
    burn_damage = 0#火傷のダメージを保存する
    if "regret" in hand:#後悔の体力減少を最初に処理する
        player_hp-= len(hand)
    
    while i<len(hand):
        cardname = searching.seek_i(hand[i],0) 
        if searching.seek_i(hand[i],5) =="1":
            exhaust_pile.append(hand.pop(i))#エセリアルカードを廃棄する。
            count+=1
        elif searching.seek_i(hand[i],5) =="2":
            if (cardname == "burn") or (cardname == "decay"):#火傷がダメージを与える処理
                burn_damage+=2
            elif cardname == "burn+":
                burn_damage+=4
            elif cardname == "doubt":
                """doubtとshameがデバフ+2となっているのは、ターン終了時のデバフ減少がこの後に挟まれるため。"""
                if weak > 0:
                    weak+=1
                else:
                    weak+=2
            elif cardname == "shame":
                print("shame")
                if frail > 0:
                    frail+=1
                else:
                    frail+=2
        i+=1
    if burn_damage>0:
        block -= burn_damage
        if block < 0:
            player_hp += block
            block = 0
    discard_pile +=hand#handを全て捨て札に送る処理
    hand = []
    if dark_emb>0:#闇の抱擁でエセリアル分ドロー
        draw(dark_emb*count, piles)
    debuffs = [enemy_vulnerable, vulnerable, enemy_weak, weak, frail]
    piles = [discard_pile, exhaust_pile, hand, draw_pile]
    return  piles, player_hp, block, debuffs
if __name__ == "__main__":
    deck = ["Ascendor's_Bane", "bash", "strike","strike","strike","strike+", "defend", "defend","defend","defend","carnage+","ghostly_armor","bludgeon+","impervious","shockwave"]#完成版では初期デッキはAscendor's baneのみにする。
    hand = []#手札
    discard_pile = []#捨て札
    used_card2 = []
    exhaust_pile = []
    draw_pile = copy.copy(deck)
    piles = [discard_pile, exhaust_pile, hand, draw_pile]
    t = 0
    power_stats = [0, [0,0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    debuffs = [0, 0, 0, 0, 0]
    while t < 5:
        piles = draw(5,piles)
        print(piles[2])
        piles, player_hp, block, debuffs = etherial(piles, 0, 0, debuffs, power_stats)
        t+=1