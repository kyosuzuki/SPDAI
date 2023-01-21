path1 = 'card_data.txt'

class search():
    """カードをtxtファイルから検索し、コスト、タイプ、火力、ブロック、などを抽出する"""
    def __init__(self):
        with open(path1) as f:
            lines = f.readlines()
            self.lines_stripe = [line.strip() for line in lines]
        self.card_table = {("strike",0):"strike"}
    
    def seek(self, name):#カード名から様々な情報を返す関数。主に手札を表示するために使用する
        name = name+' '
        card = [s for s in self.lines_stripe if name in s]
        card = str(card).split()
        return card[0].strip("['"), card[2] #card[5], card[7].strip("']")#card[0]は名前、card[1]はタイプ、card[2]はコスト、card[3]はダメージ、card[4]はブロック、card[5]は廃棄されるか否か、card[6]は特徴、card[7]は廃棄されるかどうか
    
    def seek_i(self, name, num):#カード名と番号から、そのカードの指定した情報を返す関数。
        name = name+' '
        if (name, num) in self.card_table:#処理を早くするために一度読み込んだものをself.card_tableに保管し、次に呼び出された際そこから情報を取得する。
            return self.card_table[(name, num)].strip("['")
        card = [s for s in self.lines_stripe if name in s]
        card = str(card).split()
        self.card_table[(name,num)] = card[num].strip("']")
        card[num].strip("']")
        return card[num].strip("['")#card[0]は名前、card[1]はタイプ、card[2]はコスト、card[3]はダメージ、card[4]はブロック、card[5]はエセリアルか否か、card[6]は特徴