from .utils import Utils
import aiohttp,datetime

class Weather:
    def __init__(self):
        self.utils = Utils()
        self.WEATHER_URL = 'https://weather.tsukumijima.net/api/forecast/city/'

    async def getWeather(self, area_name:str):
        res = {'text':'', 'sub':''}
        area_code = self.utils.getAreaCode(area_name)
        if area_code is None:
            print(area_name)
            res['text'] = '有効な地名を入力してください(都道府県or都市名(漢字orローマ字))'
            return res
        weather_url = self.WEATHER_URL+area_code
        print(f'area_code: {area_code}\nweather_url: {weather_url}')
        async with aiohttp.ClientSession() as session:
            async with session.get(weather_url) as r:
                if r.status == 200:
                    response = await r.json()
                    description = response.get('description')
                    if description:
                        text:str = description.get('text')
                        if text:
                            res['text'] = text.replace('\n\n','\n')
                    link = response.get('link')
                    if link:
                        res['text'] += f'\n[天気予報へのリンク]({link})'
                    forecasts = response.get('forecasts')
                    for forecast in forecasts:
                        sub = ''
                        if forecast.get('date') is not None:
                            dt = datetime.datetime.strptime(forecast.get('date'), '%Y-%m-%d')
                            sub += dt.strftime('%m/%d(%a)')
                            if forecast.get('telop'):
                                sub += ': ' + forecast.get('telop') + '\n'
                            temperature = forecast.get('temperature')
                            if temperature is not None and temperature.get('min'):
                                min_celsius = temperature.get('min').get('celsius')
                                if min_celsius and min_celsius != 'null':
                                    sub += f'- 最低気温: {min_celsius}℃\n'
                            if temperature is not None and temperature.get('max'):
                                max_celsius = temperature.get('max').get('celsius')
                                if max_celsius and max_celsius != 'null':
                                    sub += f'- 最高気温: {max_celsius}℃\n'
                            # 降水確率
                            chance_of_rain = '- 降水確率: \n'
                            target_list:str = ['T00_06', 'T06_12', 'T12_18', 'T18_24']
                            for target in target_list:
                                result = self._getChanceOfRain(forecast.get('chanceOfRain'), target)
                                if result != '':
                                    chance_of_rain += f'    - {target[1:6].replace('_','-')}時:{result}\n'
                            if chance_of_rain != '- 降水確率: \n':
                                sub += chance_of_rain
                        if sub:
                            res['sub'] += sub
                else:
                    res['text'] = 'API取得処理でエラーが発生しました。'
        return res

    def _getChanceOfRain(self, chanceOfRainDict:dict, target:str):
        result = ''
        if chanceOfRainDict is None:
            pass
        elif len(target) == 0:
            pass
        else:
            if chanceOfRainDict.get(target) and chanceOfRainDict.get(target) != '--%':
                result = chanceOfRainDict.get(target)
        return result
