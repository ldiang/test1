from utils.db_general_models.serializer import CountrySerializer, CitySerializer
from utils.db_general_models.models import UtilCity
from utils.utils_baidu_translate import TranslateService


class CityService:
    @staticmethod
    def create_new_city(city_en, country_cn):
        # 检查数据库中是否已经存在相同的城市
        if not UtilCity.objects.filter(city_en=city_en).exists():
            # 如果不存在，则创建新的城市数据
            city_data = {'city_en': city_en, 'country': country_cn}

            ser = CitySerializer(data=city_data)
            if ser.is_valid():
                ser.save()
                new_city_id = ser.instance.id
                new_translate = TranslateService()
                city_cn = new_translate.baidu_translate(city_en)
                CityService.update_city_name_cn(new_city_id, city_cn)
                #创建新的城市数据时确实返回了ser，即序列化器的实例
                return ser.instance
            else:
                print(ser.errors)
        return False  # 表示城市已经存在或者创建失败

    @staticmethod
    def update_city_name_cn(city_id, city_cn):
        # 检查数据库中是否已经存在相同的城市
        if not UtilCity.objects.filter(city_cn=city_cn).exists():
            # 如果不存在，则创建新的城市数据
            city_instance = UtilCity.objects.get(id=city_id)
            city_data = {'city_cn': city_cn}
            print(city_instance.id)
            ser = CitySerializer(city_instance, data=city_data)
            if ser.is_valid():
                ser.save()
                #创建新的城市数据时确实返回了ser，即序列化器的实例
                return ser
            else:
                print("城市序列化器的错误: " + str(ser.errors))
        return False  # 表示城市已经存在或者创建失败
