try:
    latest_expo_annual_info = ExpoStore.objects.filter(name=expo_instance).order_by('-year').first()
    if latest_expo_annual_info:
        deactivate_all()
        ser = ExpoAnnualInfoSerializer(latest_expo_annual_info, context={'lang': lang})
        print("ser.data:", ser.data)
        return Response({"code": 0,
                         "message": "获取展会年度信息成功！",
                         "data": ser.data})
    else:
        deactivate_all()
        return Response({"code": 1,
                         "message": "没有匹配的展会年度信息",
                         "data": None})  # 或者根据需要返回一个空的数据对象
except ExpoStore.DoesNotExist:
    # 处理对象不存在的情况
    return Response({"code": 2,
                     "message": "ExpoStore对象不存在",
                     "data": None})  # 或者根据需要返回一个空的数据对象



