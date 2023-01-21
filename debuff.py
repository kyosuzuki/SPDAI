def debuff_reduction(debuffs):
    """デバフをターン終了時に1減らす処理を行う。"""
    enemy_vulnerable, vulnerable, enemy_weak, weak, frail = debuffs
    if enemy_vulnerable>=1:
        enemy_vulnerable-=1#敵が弱体状態なら弱体-1
            
    if enemy_weak>=1:
        enemy_weak-=1

    if vulnerable>=1:
        vulnerable-=1
            
    if weak>=1:
        weak-=1
            
    if frail>=1:
        frail-=1
    debuffs = [enemy_vulnerable, vulnerable, enemy_weak, weak, frail]
    return debuffs

def debuf_block_energy(debuffs, block, energy, strength, dex, power_stats, f = 0):
    """自分のデバフとエナジーとパワーとブロック量を表示する関数"""
    metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats
    vulnerable, weak, frail = debuffs[1], debuffs[3], debuffs[4]
    if f == 0:
        if vulnerable>=1:
            print("あなたは弱体"+str(vulnerable))
        if weak>=1:
            print("あなたは脱力"+str(weak))
        if frail>=1:
            print("あなたは脆弱化"+str(frail))
        if block>0:#playerがブロックを持っていたら表示する
            print("block:"+str(block))
        if strength!=0:
            print("あなたの筋力は"+str(strength))
        if dex!=0:
            print("あなたの敏捷性は"+str(dex))
        if metal >0:
            print("金属化:"+str(metal))
        if combust[0] > 0:
            print("燃焼:"+str(combust[0]))
        if dark_emb > 0:
            print("闇の抱擁:"+str(dark_emb))
        if evolve > 0:
            print("進化:"+str(evolve))
        if fnp > 0:
            print("無痛:"+str(fnp))
        if f_bre > 0:
            print("炎の吐息:" + str(f_bre))
        if rupture > 0:
            print("破裂:" + str(rupture))
        if barr > 0:
            print("バリケード")
        if berser > 0:
            print("狂戦士:" + str(berser))
        if bru > 0:
            print("残虐:" + str(bru))
        if corrupt > 0:
            print("堕落")
        if ritual > 0:
            print("儀式:" + str(ritual))
        if jugg > 0:
            print("ジャガーノート:" + str(jugg))
        print("エナジー:"+str(energy))
    else:
        if vulnerable>=1:
            f.write("あなたは弱体"+str(vulnerable)+"\n")
        if weak>=1:
            f.write("あなたは脱力"+str(weak)+"\n")
        if frail>=1:
            f.write("あなたは脆弱化"+str(frail)+"\n")
        if block>0:#playerがブロックを持っていたら表示する
            f.write("block:"+str(block)+"\n")
        if strength!=0:
            f.write("あなたの筋力は"+str(strength)+"\n")
        if dex != 0:
            f.write("あなたの敏捷性は"+str(dex)+"\n")
        if metal >0:
            f.write("金属化:"+str(metal) + "\n")
        if combust[0] > 0:
            f.write("燃焼:"+str(combust[0]) + "\n")
        if dark_emb > 0:
            f.write("闇の抱擁:"+str(dark_emb) + "\n")
        if evolve > 0:
            f.write("進化:"+str(evolve) + "\n")
        if fnp > 0:
            f.write("無痛:"+str(fnp))
        if f_bre > 0:
            f.write("炎の吐息:" + str(f_bre) + "\n")
        if rupture > 0:
            f.write("破裂:" + str(rupture) + "\n")
        if barr > 0:
            f.write("バリケード" + "\n")
        if berser > 0:
            f.write("狂戦士:" + str(berser) + "\n")
        if bru > 0:
            f.write("残虐:" + str(bru) + "\n")
        if corrupt > 0:
            f.write("堕落"+ "\n") 
        if ritual > 0:
            f.write("儀式:" + str(ritual) + "\n")
        if jugg > 0:
            f.write("ジャガーノート:" + str(jugg) + "\n")

        f.write("エナジー:"+str(energy)+"\n")

def turn_end_power(power_stats, block, enemy_hitpoint, enemy_block, player_hp, strength, damage_count):
    #ターンエンド時に発動するパワーの処理をする。金属化、燃焼、破裂
    metal, combust, dark_emb, evolve, fnp, f_bre, rupture, barr, berser, bru, corrupt, ritual, jugg = power_stats
    if metal>0:
        block+=metal
    if combust[0]>0:
        player_hp -=combust[1]
        damage_count+=1
        if rupture>0:
            strength+=rupture
        enemy_block -= combust[0]
        if enemy_block<0:
            enemy_hitpoint += enemy_block
            enemey_block = 0
    return block, enemy_hitpoint, enemy_block, player_hp, strength, damage_count