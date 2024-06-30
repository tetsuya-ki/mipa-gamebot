import random

class YounaMessage:
    def __init__(self, message, cw_message = None):
        self.message = message
        self.cw_message = cw_message

class YounaMember:
    """
    「のような」参加者クラス
    """
    def __init__(self, member):
        self.youna_member = member
        self.point = 0
        self.answered = False
        self.finished = False

    def finish(self, point: 0):
        self.finished = True
        self.point += point

    def add(self, point: 0):
        self.point += point

class YounaAnswer:
    def __init__(self, member: YounaMember, answer_text: str):
        self.member = member # 回答者
        self.answer_text = answer_text

class YounaOdai:
    def __init__(self, odai, source, number, member):
        self.odai = odai
        self.source = source
        self.number = number
        self.house:YounaMember = member
        self.answered = False # いらないかも
        self.answer:YounaAnswer = None # 回答
        self.favorite_answer:YounaAnswer = None # お気に入りの回答

class Youna:
    JOB_PARENT = '0'
    JOB_CHILD = '1'
    STATUS_INIT = '0'
    STATUS_START = '1'
    STATUS_END = '2'
    MIN_MEMBER = 2 # TODO:後で直す
    MAX_MEMBER = 6
    DEFAULT_DECK = [
        ("天使のような悪魔の笑顔", "ミッドナイト・シャッフル　近藤真彦　（作詞：沢ちひろ/作曲：ジョー・リノイエ）")
        , ("季節風のような愛", "Twilight Dream　河合奈保子　（作詞：三浦徳子/作曲：馬飼野康二）")
        , ("綺麗事のような希望", "窓の中から　BUMP OF CHICKEN　（作詞：藤原基央/作曲：藤原基央）")
        , ("アイスクリームのような冷たい記憶の中の君", "アイスクリイムは溶けるから。　文藝天国　（作詞：ko shinonome/作曲：ko shinonome）")
        , ("飴玉のようなひと時", "ぶどうじゅーす　aiko　（作詞：AIKO/作曲：AIKO）")
        , ("太陽のような笑顔", "SHINY DAYS　藤原肇(鈴木みのり)　（作詞：永塚健登/作曲：新田目翔）")
        , ("ボロ雑巾のような僕", "トイプードル　安藤祐輝　（作詞：安藤祐輝/作曲：安藤祐輝）")
        , ("連ドラのような試練", "てっぺんイグニッション　#PEXACOA　（作詞：菊池諒/作曲：斎藤竜介・菊池諒）")
        , ("学校のような気がする夜", "ダーリン・ミシン　TAKESHI UEDA　（作詞：忌野清志郎/作曲：忌野清志郎）")
        , ("枕詞のような毎日", "ブランコ　遊助　（作詞：遊助/作曲：遊助・N.O.B.B）")
        , ("映画のような出会い", "ふぁなれない　YOAKE　（作詞：YOAKE P/作曲：YOAKE P）")
        , ("詐欺師のような唄", "MR.CHANGE feat. かしわ　マイアミパーティ　（作詞：さくらいたかよし・かしわ/作曲：さくらいたかよし・かしわ）")
        # , ('xxxxxx', 'yyyyy')
    ]

    def __init__(self, organizer):
        self.organizer = organizer
        self.members:dict(YounaMember) = {organizer.id: YounaMember(organizer)}
        self.deck = self.DEFAULT_DECK.copy()
        self.answers:dict(YounaAnswer) = {}
        self.answers_list:list(YounaAnswer) = []
        self.discards:list(YounaOdai) = []
        self.turn = 0
        self.status = self.STATUS_INIT
        self.odais:list(YounaOdai) = []
        self.current_odai:YounaOdai = None
        self.current_answer:YounaAnswer = None

    def join(self, join_member) -> YounaMessage:
        # すでに参加しているかチェック
        if self.members.get(join_member.id):
            return YounaMessage(f'{join_member.username}さんはすでに参加されています。')
        # 未参加メンバーの場合だけ追加
        self.members[join_member.id] = YounaMember(join_member)
        # 最大人数の場合、スタートしちゃう
        if self._is_member_max():
            return self.start()
        else:
            return YounaMessage(f'参加を受け付けました(参加人数:{len(self.members)})')

    def leave(self, leave_member):
        removed_member = self.members.pop(leave_member.id, None)
        if removed_member is None:
            return YounaMessage('参加していません。')
        else:
            return YounaMessage(f'{removed_member.username}が離脱しました。')

    def start(self) -> YounaMessage:
        # チェック
        if self._is_startable():
            self.status = self.STATUS_START
            return self._first_turn()

    def child_answer(self, answer_member, answer_text):
        '''子が回答を提出'''
        # 親は提出できない
        if self.current_odai.house.id == answer_member.id:
            return YounaMessage('親は回答を提出できません')

        self.answers[answer_member.id] = YounaAnswer(answer_member, answer_text)

        # 親以外の全員が回答したかチェック
        if len(self.answers) < len(self.members) - 1:
            return YounaMessage(f'回答を受け付けました(未回答者: {len(self.members) - len(self.answers) - 1}人)')
        else:
            self.answers_list = random.shuffle(list(self.answers))
            self.current_answer = self.answers_list.pop()
            return YounaMessage(f'全員の回答が完了しました。\r\n親( @{self.current_odai.home} )は以下の文章からお題を想像してください。$[font.serif {self.current_answer.answer_text}]\r\n`<メンション> 「<お題と思われる文字列(〜〜のような〜〜)>」`で回答してください。')

    def house_answer(self, answer_text):
        '''親が回答を提出'''
        # 成否判定
        if answer_text == self.current_odai.odai:
            # 親の回答が正解の処理
            self.members[self.odai.house.id].finished(50)

            # 子のポイント
            num = len(self.members) - 1 - len(self.answers_list)
            point = 0
            if num < 3:
                point = 10 * num
            else:
                point = 30
            for member in self.members:
                if member.id != self.current_odai.house.id:
                    member.add(point)
            return YounaMessage(f'お題を見事正解しました！ ')

        # 親の回答が不正解
        else:
            pass
        # 全部みたかチェック



# 最終ターンか評価

# 結果出力

###### 内部メソッドちゃん ######
    def _is_startable(self):
        if len(self.members) >= self.MIN_MEMBER:
            return True
        else:
            return False

    def _is_member_max(self):
        if len(self.members) >= self.MAX_MEMBER:
            return True
        else:
            return False

    # 初期ターン
    def _first_turn(self) -> YounaMessage:
        # すべてのお題を決定
        for i, member in enumerate(self.members):
            random.shuffle(self.deck)
            odai = self.deck.pop()
            print(f'{member.youna_member.username}の時に引かれた(意味ないけど): {odai}')
            self.odais.append(YounaOdai(odai[0], odai[1], i, member.youna_member))

        # 今回のターンの処理
        self.turn += 1
        # 投稿させるメッセージを返却
        self.current_odai = self.odais.pop()
        return YounaMessage(f'親は{self.current_odai.house.username}さんです。cwは親以外のメンバーが確認してください', f'お題は「{self.current_odai.odai}」です。\r\n`@メンション answer 「<お題への回答文字列>」`形式 (回答はカギカッコで括ること！）で回答してください！')
