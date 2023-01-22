import time, random, copy, collections
import Enemy, Battle, human_battle
#完成版では初期デッキはAscendor's baneのみにする。なお、エラーが起きるのでAscendor's_baneではなくAscendors_baneである。
#deck = ['bash',"strike","strike","strike","strike+"]
#deck = ["strike","strike","strike","strike","strike","def","def","def","def","carnage"]
#deck = ["Ascendors_Bane","carnage+","ghostly_armor","impervious","bludgeon+","carnage","impervious","bludgeon","uppercut+","clothesline","ghostly_armor","strike","strike","defend","defend","strike","strike","defend","defend","shockwave"]

#デッキにあるカードごとの枚数を辞書型で用意しておく
t = 0
damage = 0
block = 0
#エナジーの毎ターン補充量
relic = []
enemy_strength = 0
enemy_dict = {0:'sandbag',1:'cultist', 2:'snakeplant',3:'book_of_stabbing'}
Malleable = 0
flag = ''#デッキがシャッフルされるとフラッグに文字が代入される。aiの学習に使用される。
memory = []
count1 = 0#デバッグ用
count2 = 0
I = 0
C = 0
command = 1
deck = ["Ascendor's_Bane", "bash", "strike","strike","strike","strike+", "defend", "defend","defend","defend","carnage+","ghostly_armor","bludgeon+","impervious","shockwave"]
    
class assistant:
    def __init__(self, deck):
        self.deck = deck
        self.a = ""
    
    def remove(self,a):
        
        try:
            p = deck.index(a)
            deck.pop(p)
        except:
            pass

    def review(self):
        print(deck)

    def add(self, a):
        deck.append(a)

    def shuffle(self, b):
        random.shuffle(deck)
        if b== 0:#bが0の時シャッフル後のデッキを見せる。bが0以外なら見せない
            print(deck)

    def upgrade(self, a):
        p = deck.index(a)
        deck.pop(p)
        data.add(a+'+')


def cui():
    "charcter user interface"
    print("Slay_the_Spire攻略アシスタントです！何をしますか？")
    true =1
    strength = 0#筋力
    dex = 0
    energy = 4
    energyre = energy
    player_hp = 75
    while true ==1:
        print("--------------------\nhelp:ヘルプを見る\n0:アシスタントプログラムを終了する\n1:デッキを入力する\n2:カードを削除する\n3:デッキをシャッフルする\n4:デッキを見る\n5:カードをアップグレードする\n6:敵と戦闘する\n7:ステータスを変更する\n8:AIに戦闘させる\n9:上級者向け設定\n--------------------")
        n = input("入力してください!:")
        if n=="1":
            true = 1
            while true ==1:
                t = input("カードを入力してください!何も入力せずenterすると次に進みます:")
                if t=="icset":
                    data.add("st")
                    data.add("st")
                    data.add("st")
                    data.add("st")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("bash")
                    t = "st"
                elif t=="icset_1":
                    data.add("st")
                    data.add("st")
                    data.add("st")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("bash")
                    t = "st"
                elif t=="icset_2":
                        data.add("st")
                        data.add("st")
                        data.add("def")
                        data.add("def")
                        data.add("def")
                        data.add("def")
                        data.add("bash")
                        t = "st"
                elif t=="icset_3":
                    data.add("st")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("bash")
                    t = "st"
                elif t=="icset_4":
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("bash")
                    t = "st"
                elif t=="icset_5":
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    data.add("def")
                    t = "bash"
                elif t=="":
                    break
                    
                data.add(t)
            data.remove("")
        elif n=="2":
            while true:
                data.review()
                t = input("削除するカードを入力してください。何も入力せずenterを押せば終わります。:")
                if t =='':
                    break
                data.remove(t)
        elif n=="3":
            data.shuffle(0)
        elif n=="4":
            deck_count = collections.Counter(deck)
            print(deck_count)
        elif n=="5":
            while true:
                data.review()
                t = input("アップグレードするカードを入力してください。何も入力せずenterを押せば終わります。:")
                if t =='':
                    break
                data.upgrade(t)            
        elif n=="6":
            data.shuffle(1)
            draw_pile = copy.copy(deck)#参照値渡しを警戒してcopyを使用。

            floar2 = human_battle.Battle()

            e = Enemy.Enemy()#eを使って敵を選択
            
            print(enemy_dict)
            namenumber =input("敵を選択してください")
            e.name = enemy_dict[int(namenumber)]
            print(e.name+"との戦闘を始めます")
            floar2.fight(energyre, deck, e, player_hp)
        elif n=="7":
            word = True
            while word:
                print("何を変えますか？\n1:プレイヤーの初期HP\n2:毎ターン回復するエナジーの量")
                print("現在の初期HP:"+str(player_hp)+"\n現在のエナジーの量:"+str(energyre))
                word = input("選択してください:")
                if word == "1":
                    player_hp = int(input("プレイヤーの初期体力を入力してください:"))
                elif word == "2":
                    energyre = int(input("エナジーの量を入力してください:"))
        elif n=="8":#aiに戦闘を行わせる！
            """記録用テキストファイルの初期化"""
            f2 = open("used_2.txt", 'a+')
            f2.truncate(0)
            f2.close()

            f = open("record_2.txt","a")
            f.truncate(0)
            f.close()

            floar = Battle.Battle()
            e = Enemy.Enemy()
            print(enemy_dict)
            namenumber =input("敵を選択してください")
            e.name = enemy_dict[int(namenumber)]
            print("戦闘回数を入力してください")
            c = int(input())
            print("敵:"+e.name+"\n回数:"+str(c)+"\ndeck"+str(collections.Counter(deck))+"\nエナジー:"+str(energyre)+"プレイヤー初期HP:"+str(player_hp))
            time1 = time.time()
            floar.ai_fight_3(energyre, deck, e, player_hp, c)
            sec = round((time.time()-time1),1)
            hour = sec//3600
            min = sec%3600
            min, sec = divmod(min,60)
            print("処理時間:",str(hour)+"時間"+str(min)+"分"+str(sec)+"秒")
        elif n=="9":
            pass

        elif n=="0":
            true = 2
            print("役に立ったのかな？")
        elif n=="help":
            print("\n私はSlay the Spire攻略アシスタントプログラムです！私にできることを紹介させて頂きますね。\n\n0 を入力するとこのプログラムを終了します。\n\n1 を入力するとデッキにカードを追加することができます。現在はアイアンクラッドの英語の正式名称を入力して頂ければそのカードがデッキに入ります。例えば strike と入力したらストライクが1枚デッキに入ります。dark_embrace+と入力すると闇の抱擁+が入ります。正式名称に半角スペースが入る場合、それをアンダーバーに変えてご入力ください。\n入力を楽にするため、icsetと入力して頂ければストライク5枚、強打1枚、防御4枚が一度に入ります。icset_1と入力すると、そこからストライクを1枚削除した物、icset_2だと2枚削除した物、icset_3だと3枚削除した物・・・・・・を一度にデッキに入れます。icset_5まで用意しました。\n注意!私はA20前提で造られているので、Ascendor's_Baneは最初から入っています。\n\n2 を入力するとデッキからカードを削除することが出来ます。削除したいカードの名前を入力してください。Ascendor's_Baneを削除したい場合もこちらをご利用ください。\n\n3 を入力するとデッキをシャッフルして表示します。\n\n4 を入力すると今のデッキを表示します。 \n\n5 を入力するとカードをアップグレードします。正式名称を入力してください。火力16、火力21、火力27・・・・・・の灼熱の一撃を用意したい場合はアプグレ前の灼熱の一撃を入れてから複数回アプグレするのではなく、直接searing_blow+10等と入力してください。+15まで存在します。\n\n6 を入力し、戦いたい敵の番号を入力すれば、現在のデッキを使った戦闘が始まります！戦闘では、カードを番号で指定することでカードを使用します。その際、-2と入力すると山札、-3で捨て札、-4で廃棄したカードをそれぞれ見ることが可能です。-1と入力するか、何も入力せずenterキーを押すとturn endします。\n\n注意！敵の強さはA20です。A17未満の敵を現在用意していません。\n\n7 を入力すると毎ターン補充するエナジーの量と初期体力を変更できます。初期状態は4エナ、HP75です。\n\n8 を入力すると私が指定された敵と指定された回数戦闘を行い、被害データなどを表示します。現状はモンテカルロ法で行動を決定しており、その戦闘の様子はカレントディレクトリに生成されるrecord.txtをご覧ください。\nrecord2.txtはモンテカルロ法の処理の過程を追う為の物で、通常は気にしなくても構いません。\n\n9 を入力すると・・・・・・現在は何も起きませんが、いずれ何かを実装する予定です。なお、今のverではレリックが存在せず、複数戦のシミュレーションもできません\n\n以上です。")

if __name__ == "__main__":#これを実行した際に起動する。

    data = assistant(deck)
    cui()

