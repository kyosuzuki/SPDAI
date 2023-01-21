class Relic:
    """レリックについての処理を記述するクラス"""
    def __init__(self, relics_list):
        """initではレリックリストを受け取りself.reric_listに代入する。"""
        self.rerlics_list = relics_list

    def battle_start_relics(self, something):
        player_hp, hand, draw_pile, discard_pile, energy, strength, dex, block, enemy_vulnerable,  = something
        """戦闘開始時に起動するレリックの処理を記述する。"""
        if "lantern" in self.rerlics_list:#ランタン
            energy+=1
            return energy

    def turn_start_relics(self):
        """ターン開始時に起動するレリックの処理を記述する。"""
        pass
    
    def after_card_played_relics(self):
        """カード使用後に条件を満たすと起動するレリックの処理を記述する。"""
    
    def turn_end_relics(self):
        """ターンエンド時に起動するレリックの処理を記述する。"""

    def end_battle_relics(self):
        """戦闘終了時に起動するレリックの処理を記述する。"""