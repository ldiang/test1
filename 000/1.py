from django.utils.translation import activate
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def your_api_view(request):
    requested_language = request.GET.get('language', None)

    if requested_language and requested_language in ['de', 'en']:
        activate(requested_language)
    else:
        activate('zh-Hans')  # 默认语言

    # 处理视图逻辑，获取数据并返回给前端

    # ...

    # 返回翻译后的数据
    translated_data = {
        'key1': _('Translated value 1'),
        'key2': _('Translated value 2'),
        # ...
    }

    return Response(translated_data)
