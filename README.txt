　プログラムの目的
　デッキの強さを測るために、AIに複数回戦闘を行わせ被害量を測る事です。
　
　動作環境
　windows10
　python ver 3.10.9
　仮想環境作成に必要なpip installは
　tqdm 4.64.1
　numpy 1.24.1
　です。このreadmeファイルを作成している時点で、この2つのモジュールは全て最新verでした。
　また、この2つをinstallした場合colorama 0.4.6が付随します。
　
　使い方
　他のpyファイルがexeファイルと同じディレクトリにある事を確認した上でmain_ver0.96.pyを実行してください。
　すると、「Slay_the_Spire攻略アシスタントです！何をしますか？」と質問をされるため、選択肢の前にある数字を入力してください。例えばデッキを見たい場合は半角の4を入力します。
　前述のAIに戦闘させる目的を達成したい場合、8を入力し、敵を選択し、戦闘回数を入力すればokです。初期状態のプレイヤーの戦力は2のsnakeplantと戦闘することを想定されたデッキですので、まずはそれと戦闘させてみることを推奨します。
　戦闘後、同じディレクトリにrecord.txtファイルが生成されます。このファイルには戦闘の様子が書き込まれています。
　また、6を入力すると人間の手で敵と戦闘することも可能です。
　基本的な使い方は以上です。これ以上の説明はhelpと入力し、ご覧ください。
　
　各ファイルの説明
　explorer上で種類でソートし上からファイルの説明を行います。申し訳ないのですが、過去のverで使用され、現在は使用されていない物も全て削除せず残している為に、理解が困難である可能性があります。
　また、多くのファイルにてif f == 0や if f == -1といった書き方がされていますが、f == 0だと人がプレイしている時、 -1だとAIがプレイしている時の処理を記述しています。違いはprintするか、writeするかです。
　relic.csvは現在のverでは使用されていません。
　AI.pyはAIについて書かれています。使用しているのは205行目のmonteで、モンテカルロ法の記述を行っています。また、300行目のpath_gainでは、1手後以降の計算をモンテカルロ法より計算量の少ない手法で計算させています。
　Battle.pyはAIの戦闘について書かれています。全体的なAIの戦闘の流れがここに記述されています。ai_fight_4はモンテカルロ法のためにAIに未来を予測させるためのもので、AI_fight_3は予測を受けて現時点での戦闘を行います。
　card_use.pyはカードを使用する処理が描かれています。5行目のcard_playは人やAIから与えられた数字がカード使用に関する物か、ターンエンドや山札の表示を求める物かを判断します。card_use_hとpower_use、special_cardはカードの効果を実際に発動させるためのものです。
　debuff.pyはバフデバフの処理を行います。
　draw.pyはカードのドローとターン終了時にカードを捨て札に送る処理が書かれています。
　Enemy.pyは敵について書かれています。120行目までは敵の体力や行動が書かれており、それ以降は敵の攻撃を予告するために計算を行う関数(damage_calculator)、敵のデバフを表示する関数、実際に相手にダメージを与える処理(damage_deploy)、プレイヤーがダメージを受ける処理(damage_taken)が描かれています。
　graph_plot.pyは戦闘データの統計処理を行うための物ですが、強化学習を採用していた時代は戦闘回数を重ねるごとに行動を変えていたため、戦闘回数の増加と被害データをグラフで表示することが重要でした。現在は戦闘回数を重ねて学習するといった要素はないため、statistics_for_monteにある通り、95%信頼区間を求めるために使用しています。
　human_battle.pyは人間が戦闘する際の物です。
　main_ver0.96.pyはmain関数です。
　q_learning_sts.pyは、q学習時代の名残で、現在は使用していません。参考書に掲載されていたq学習のためのコードを一部流用しています。
　relic.pyは使用していません。
　search.pyはカード名からカードの情報を入手するための物です。seekは手札を表示する為の物で、seek_iはカードを使用する際にカードのコストや攻撃力の情報を入手するための関数です。
　
　.txtは使用していません。
　card_data.txtに入っているデータをsearch.pyから読み込んでいます。現在はキャラクターの一人のアイアンクラッドのカードが半分ほど+αが入っています。
　enemy_data,memory,q_tableは全て使用していません。
　record.txtには、AIに行わせた戦闘の履歴が入っています。
　record_2.txtにはAIに予測をさせた戦闘の履歴が入っています。recordは実際にAIが経験した戦闘で、record_2は予測した戦闘です。
　strong_card_data,used,used_2は全て使用していません。
