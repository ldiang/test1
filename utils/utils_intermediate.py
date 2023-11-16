# 用于多对多模型，中间表的写入
# 适用范围，前端传来的数据为关联ID的列表
# 范例 [1,3,5,11]
# 需要在调用前设置field_name='sector'
class IntermediateService:
    @staticmethod
    def intermediate_table_save(data,
                                model_master,
                                model_detail,
                                field_master,
                                field_detail,
                                ser_instance,
                                serializer_intermediate):
        # 第1步：将data['sector']和data['theme']从data中提取出来
        field_data = data.pop(field_detail, [])

        # 第2步：用list(map(int, sectors_data.split(',')))将data['sector']和data['theme']转为真正的数组
        # 如果前端发送的是真实的数组，就不需要这一步
        # field_ids = list(map(int, field_data[0].split(',')))

        # 第3步：利用数组对UtilSector和UtilTheme进行查询，组成由对象组成的新的data['sector']和data['theme']
        # instances_detail = model_detail.objects.filter(id__in=field_ids)
        # 如果是真实的数组，跳过第2步后，这里需要修改
        instances_detail = model_detail.objects.filter(id__in=field_data)

        # 第4步：将新的data['sector']和data['theme']更新到data中然后传入序列化器
        data[field_detail] = instances_detail

        # import pdb;
        # pdb.set_trace()

        # 第6步：构建新的中间表实例，先找刚保存的主数据的对象
        instances_master = model_master.objects.get(id=ser_instance.instance.id)

        # 第7步：根据之前获取的分类对象列表构建新实例，并进行验证
        for instance in instances_detail:
            #注意为了配合下面的唯一性检查，这里用数组 而不用列表。
            new_intermediate = {field_master: instances_master,
                                field_detail: instance}
            # new_res = serializer_intermediate(
            #     data=new_intermediate, many=True)

            # 唯一性检查 使用 get_or_create 查询对象
            #防止IntegrityError异常
            intermediate_instance, created = serializer_intermediate.Meta.model.objects.get_or_create(
                **new_intermediate
            )

            if created:
                # 如果对象是新创建的，可以在这里添加一些额外的逻辑
                pass
            else:
                # 如果对象已存在，可以在这里添加一些额外的逻辑
                print('数据已存在！')
                pass

            # if new_res.is_valid():
            #     new_res.save()
            # else:
            #     print(new_res.errors)
