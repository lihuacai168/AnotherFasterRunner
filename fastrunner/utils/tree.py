def get_tree_max_id(value, list_id=[]):
    """
    得到最大Tree max id
    """
    if not value:
        return 0  # the first node id

    if isinstance(value, list):
        for content in value:  # content -> dict
            children = content.get('children')
            if children:
                get_tree_max_id(children)

            list_id.append(content['id'])

    return max(list_id)


def get_all_ycatid(value, list_id=[]):
    """
    获取所有yapi的分组目录id
    """
    if not value:
        return []  # the first node id

    if isinstance(value, list):
        for content in value:  # content -> dict
            yapi_catid = content.get('yapi_catid')
            if yapi_catid:
                list_id.append(yapi_catid)

            children = content.get('children')
            if children:
                get_all_ycatid(children)
    return list_id


def get_faster_id_by_ycatid(value, yapi_catid):
    """
    通过yapi的catid反向查找faster的api分组id
    """

    if not value:
        return 0

    if isinstance(value, list):
        for content in value:  # content -> dict
            if content.get('yapi_catid') == yapi_catid:
                return content['id']
            children = content.get('children')
            if children:
                get_faster_id_by_ycatid(children, yapi_catid)
    return 0


def get_tree_ycatid_mapping(value, mapping={}):
    """
    获取yapi分组id和faster api分组id的映射关系
    {'yapi_catid': 'node_id'}
    """
    if not value:
        return {}

    if isinstance(value, list):
        for content in value:  # content -> dict
            yapi_catid = content.get('yapi_catid')
            if yapi_catid:
                mapping.update({yapi_catid: content.get('id')})
            children = content.get('children')
            if children:
                get_tree_ycatid_mapping(children, mapping)
    return mapping


def get_file_size(size):
    """计算大小
    """

    if size >= 1048576:
        size = str(round(size / 1048576, 2)) + 'MB'
    elif size >= 1024:
        size = str(round(size / 1024, 2)) + 'KB'
    else:
        size = str(size) + 'Byte'

    return size


# 默认分组的id=1
label_id = 1


def get_tree_label(value, search_label):
    """
    # 根据分组名查找分组的id,默认为1
    :param value:
    :param search_label:
    :return: label_id
    """
    global label_id
    if not value:
        return label_id  # 默认分组

    if isinstance(value, list):
        for content in value:  # content -> dict
            if content['label'] == search_label:
                label_id = content['id']
            children = content.get('children')
            if children:
                get_tree_label(children, search_label)
    return label_id



