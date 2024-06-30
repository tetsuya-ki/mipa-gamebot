import json, os
from os.path import join, dirname

class Utils:
    def __init__(self):
        # 辞書の読み込み
        self.weather_area = {}
        self.WEATHER_ARE_JSON = 'weather_area.json'
        self.readWeatherAreaJson()

    def readWeatherAreaJson(self):
        # 読み込み
        try:
            file_path = join(dirname(__file__), 'files' + os.sep + self.WEATHER_ARE_JSON)
            with open(file_path, mode='r') as f:
                self.weather_area = json.load(f)
        except FileNotFoundError:
            # 読み込みに失敗したらなにもしない
            pass
        except json.JSONDecodeError:
            # JSON変換失敗したらなにもしない
            pass
        except EOFError:
            # 読み込みに失敗したらなにもしない
            pass

    def getAreaCode(self, in_area_name:str):
        '''
        area_name(場所名:漢字orヘボン式ローマ字)からarea_codeを取得。
        area_name {str}
        '''
        area_name = in_area_name.capitalize()
        area = self.weather_area.get(area_name)
        # 県名で検索して見つからないパターンはkeysを見て、citiesから取得
        if area is None:
            print(f'sitei:{area_name}')
            for key in self.weather_area.keys():
                area = self.weather_area.get(key)
                if area is not None and isinstance(area, dict):
                    cities = area.get('cities')
                    city = cities.get(area_name)
                    if city is not None:
                        return city
        # 県名で検索して見つかったパターン
        else:
            print(f'ken:{area_name}')
            if area is not None and isinstance(area, dict):
                pref_first = list(area.get('cities').values())[0]
            return pref_first
        # それでも見つからないパターン
        return None
