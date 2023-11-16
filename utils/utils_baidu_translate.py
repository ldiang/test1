import hashlib
import time
import requests
from django.http import JsonResponse


class TranslateService:

    @staticmethod
    def baidu_translate(city_en):
        # if request.method == 'POST':
        #     # 从前端获取城市名称
        #     city_name = request.POST.get('city_en', '')

        # 百度翻译API的请求地址
        url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

        # 替换成你自己的百度API信息
        app_id = '20231116001882523'
        secret_key = 'NOCbXeRhmAzEthTsk9jz'

        # 获取当前时间戳
        timestamp = int(time.time())
        # 将时间戳作为salt值
        salt = str(timestamp)

        # 构建请求参数
        params = {
            'q': city_en,
            'from': 'en',
            'to': 'zh',
            'appid': app_id,
            'salt': salt,  # 随机字符串
        }

        # 计算签名
        sign_str = f"{app_id}{city_en}{params['salt']}{secret_key}"
        params['sign'] = hashlib.md5(sign_str.encode()).hexdigest()

        # 发送翻译请求
        response = requests.get(url, params=params)
        translation_result = response.json()

        # 提取翻译结果
        city_cn = translation_result.get('trans_result', [{}])[
            0].get('dst', '')

        return city_cn

    #     # 返回翻译结果给前端
    #     return JsonResponse({'translated_city': city_cn})
    #
    # return JsonResponse({'error': 'Invalid request method'}, status=400)
