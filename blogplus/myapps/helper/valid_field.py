def valid_required(field: str,
                   field_cn: str,
                   value: str,
                   errors: dict,
                   min_length=1,
                   max_length=50):
    '''
    验证 field字段是否为必填项
    :param max_length:  最大长度
    :param min_length:  最小长度
    :param field_cn: 中文字段名
    :param field:  字段名
    :param value:  字段值
    :param errors:  如果验证有错误，则存放errors中
    :return:
    '''
    value = value.strip()
    if not value:
        errors[field] = '%s 不能为空!' % field_cn
    elif len(value) < min_length:
        errors[field] = '%s 不能少于 %d 位!' %(field_cn, min_length)
    elif len(value) > max_length:
        errors[field] = '%s 不能超出 %d 位!' % (field_cn, max_length)