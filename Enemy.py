import random, math
with open('record.txt','w') as f:#デッキの内容を書き込む

    class Enemy:
        """敵の情報を表現するクラス"""
        def __init__(self):
            """name:敵の名前
            hp:敵の体力
            action:敵の行動
            beat:敵の火力
            cha:敵の特性
            notice:敵のダメージ行動予告"""
            self.cha =''
            self.notice = 0
            self.b=0
            self.c = 0
            #ターン数分配列を作成する。この配列にそのターンの敵の行動を入れる
            self.enemyaction_dict = {n: (0,0,0,0) for n in range(99)}
        def name(self, name):
            self.name = name
        def life(self):
            #敵の体力を記述する。randomを使用している。A20基準
            val = {'sandbag':100,'cultist':random.randrange(50,56),'snakeplant':random.randrange(78,82),'book_of_stabbing':random.randrange(168,172)}
            return val[self.name]

        def enemyaction(self, t, enemy_strength):

            """敵の行動をこの場で記述する。コードが長くなるので別のところに記述した方がいいかもしれない。"""
            """2つの物をreturnする。1つ目は敵の1発の攻撃で、2つ目は攻撃回数である。仮に敵が攻撃以外の行動をとる場合、1つ目に特殊な文字列を返し、2つ目で-1を返す。"""
            
            #いろいろと便利な変数としてself.bを使用する。
            if self.enemyaction_dict[t] == (0,0,0,0):
                if self.name=='cultist':#狂信者　一番最初に作ったため一番犠牲になっただろう
                
                    if t==0:
                        self.notice = 'cultist'
                        count = -1
                        special = 0
                    else:
                        enemy_strength +=5
                        self.notice = 1+enemy_strength
                        count = 1
                        special = 0
                if self.name=='sandbag':#デバッグ用のサンドバッグ
                    self.notice = 'sandbag'
                    count = -1
                    special = 0
                if self.name =='snakeplant':#スネークプラント　3を法とする合同式の考え方を使用して記述する。
                    a = random.random()#65%の確率で8×3、残りの確率でデバフを使用する。
                    #cはデバフを1度も使用せず8×3を3連続で使用させない為に使用する。
                    #a20以上ではデバフ使用後と使用前で行動が異なる。b = 0だとデバフ使用前、b=1だとデバフ使用後を表す。
                    special  = 1
                    if (a<=0.65) and (self.b==0) and (self.c<2):#65%の確率かつbが0の時8×3
                        self.notice=8
                        count=3
                        self.c+=1
                    elif (a>0.65 and (self.b==0))or((self.b>1)and(self.b%3==0))or (self.c==2):#35%かつbが0の時か、デバフを1度使った3t後
                        self.b +=1
                        self.c+=3
                        count = -1
                        self.notice = "Enfeebling Spores"
                    elif (self.b%3==1)or(self.b%3==2):
                        self.notice=8
                        count=3
                        self.b+=1
                if self.name == 'book_of_stabbing':#刺創の本
                    special = 2
                    a = random.random()#85%で連撃、それ以外は単発、それぞれ3連続、2連続で同一の行動をしない。
                    if ((a<=0.85) or (self.b == 1)) and (self.c<2):
                        self.notice = 7
                        count = 2 + t
                        self.b = 0#self.bは単発を連続で行わせない為の物
                        self.c += 1
                    else:
                        self.notice = 24
                        count = 1
                        self.b = 1
                        self.c = 0#連撃を3連続で行わせない為の物

                self.enemyaction_dict = {**self.enemyaction_dict,t:(self.notice, count, enemy_strength, special)}

            return self.enemyaction_dict[t]
        
        def char(self, enemy_name):
            """敵の名前を受け取り特徴を返す"""
            if enemy_name == 'snakeplant':
                return 1
            else:
                return 0



    def enemy_special_action(special, vulnerable, weak, frail):#敵の特殊な行動を記述する関数。特に脱力弱体脆弱化
        if special =='cultist':
            #print("cawcaw!")
            return vulnerable, weak, frail, 0
        if special =='sandbag':
            #print("test")
            return vulnerable, weak, frail, 0
        if special =='Enfeebling Spores':
            #print("脆弱化、脱力+2!")
            if frail == 0:
                frail +=1
            frail+=2
            if weak == 0:
                weak += 1
            weak+=2
            return 0, frail, weak, 0

    def spnumber(sp, special_status):#敵の特殊な行動の弱体脱力脆弱化以外を表す物
        Malleable, Painful_stab = special_status
        if sp ==1:#スネークプラント
            Malleable=3   
        if sp ==2:#本
            Painful_stab = 1

       
        special_status = [Malleable, Painful_stab]
        return special_status

    def damage_calculator(enemy_count, enemy_attack, debuffs, yv, ew,f = 0):
        """敵の攻撃についての計算を行う。 aiにプレイさせるか否かでprintするかどうか変化する"""
        if enemy_count>=1: #敵の行動予告
            if debuffs[1]>0 and yv==0:
                enemy_attack*=1.5
                yv = 1#yvやewが1だと、そのターンはもう自分の弱体と相手の脱力の計算を終了したことを示している。
            if debuffs[2]>0 and ew ==0:
                enemy_attack*=0.75
                ew = 1
            enemy_attack = math.floor(enemy_attack)
            d = enemy_attack*enemy_count
            if enemy_count>1:
                if f == 0:
                    print(str(enemy_attack)+"×"+str(enemy_count)+"の攻撃予告")
                else:
                    f.write(str(enemy_attack)+"×"+str(enemy_count)+"の攻撃予告\n")
            else:
                if f == 0:
                    print(str(enemy_attack)+"の攻撃予告")
                else:
                    f.write(str(enemy_attack)+"の攻撃予告\n")
        elif enemy_count==-1:
            d = 0
            if f == 0:
                print("何かをやってくる・・・")
            else:
                f.write("何かをやってくる・・・\n")
        return enemy_attack, d, yv, ew

    def enemy_debuff(name, debuffs, enemy_block, f = 0):
        """敵がデバフを持っていることを伝える関数"""
        if f == 0:
            if debuffs[0]>=1:
                print(name+"は弱体:"+str(debuffs[0]))
            if debuffs[2]>=1:
                print(name+"は脱力:"+str(debuffs[2]))
            if int(enemy_block)>=1:
                print(name+"は"+str(enemy_block)+"ブロック持っている")
        else:
            if debuffs[0]>=1:
                f.write(name+"は弱体:"+str(debuffs[0])+"\n")
            if debuffs[1]>=1:
                f.write(name+"は脱力:"+str(debuffs[2])+"\n")
            if int(enemy_block)>=1:
                f.write(name+"は"+str(enemy_block)+"ブロック\n")

    def damage_deploy(damage, enemy_block, enemy_hitpoint, special_status, count):
        Malleable, Painful_stab = special_status
        Malleable_count = 0#ツインストライクが鍛錬を2回発動させる処理のため
        for i in range(count):
            if damage>0:
                d = enemy_block - damage#敵がブロックを持っている場合の計算を行う。
                if (d>=0):
                    enemy_block = d
                else:
                    enemy_block = 0
                    enemy_hitpoint +=d
                    if Malleable>0:#snakeplant等が持っている、ダメージを受けるとブロックを積むあれの処理
                        Malleable_count +=1
        """鍛錬でのブロック増加"""
        for i in range(Malleable_count):
            enemy_block+=Malleable+i
        Malleable = Malleable_count + special_status[0]
        special_status = [Malleable, Painful_stab]
        return damage, enemy_block, enemy_hitpoint, special_status
    def damage_taken(enemy_attack, enemy_count, block, player_hp, debuffs, special_status, piles, f = 0):
        """f == 0の場合人がcuiで6を入力している場合である。つまり人が操作している。"""
        enemy_vulnerable, vulnerable, enemy_weak, weak, frail = debuffs
        discard_pile, exhaust_pile, hand, draw_pile = piles
        if f == 0:
            """enemy_countは攻撃してくる場合1以上で、デバフなどの特殊な行動時には-1が代入されている。"""
            if enemy_count !=-1:
                for _ in range(enemy_count):
                    enemy_damage = enemy_attack - block
                    if enemy_damage<=0:
                        block -= enemy_attack
                        enemy_damage =0
                    else:
                        block = 0
                        print(str(enemy_damage)+"のダメージを受けた")
                        player_hp-=enemy_damage
                        if special_status[1] == 1:
                            discard_pile.append("wound")
            else:
                print(enemy_attack)
                vulnerable, weak, frail, sp = enemy_special_action(enemy_attack, vulnerable, weak, frail)#敵が特殊な行動をしてくるならこっち
                enemy_damage=0
        else:
            """こちらはAI向け。fにテキストファイルのパスが代入されており、そこに履歴を書き込む"""
            if enemy_count != -1:
                for _ in range(enemy_count):
                    enemy_damage = enemy_attack - block
                    if enemy_damage<=0:
                        block -= enemy_attack
                        enemy_damage =0
                    else:
                        block = 0
                        f.write(str(enemy_damage)+"のダメージを受けた")
                        player_hp-=enemy_damage
                        if special_status[1] == 1:
                            discard_pile.append("wound")
            else:
                f.write(enemy_attack+"\n")
                vulnerable, weak, frail, sp = enemy_special_action(enemy_attack, vulnerable, weak, frail)#敵が特殊な行動をしてくるならこっち
                enemy_damage=0
           
        debuffs = [enemy_vulnerable, vulnerable, enemy_weak, weak, frail]
        piles = [discard_pile, exhaust_pile, hand, draw_pile]
        return player_hp, debuffs, piles

        