country = UtilCountry.objects.get(country_cn=data['country'])

if not UtilCity.objects.filter(city_en=data['city']).exists():
    # 注意 引用的类需要实例化后在使用
    city_service = CityService()
    city_ser = city_service.create_new_city(data['city'],
                                            country.country_cn)
    if city_ser:
        # .instance获取返回的序列化器对象的实例
        city = city_ser.instance
else:
    city = UtilCity.objects.get(city_en=data['city'])