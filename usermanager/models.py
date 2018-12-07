from django.db import models


# Create your models here.

class BaseTable(models.Model):
    """
    公共字段列
    """

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def getDict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            # 特殊处理datetime的数据
            elif isinstance(getattr(self, attr), BaseTable):
                d[attr] = getattr(self, attr).getDict()
            # 递归生成BaseModel类的dict
            elif self.isAttrInstance(attr, int) or self.isAttrInstance(attr, float) \
                    or self.isAttrInstance(attr, str):
                d[attr] = getattr(self, attr)
            # else:
            #     d[attr] = getattr(self, attr)
        mAttr = self.getMtMField()
        if mAttr is not None:
            for m in mAttr:
                if hasattr(self, m):
                    attlist = getattr(self, m).all()
                    l = []
                    for attr in attlist:
                        if isinstance(attr, BaseTable):
                            l.append(attr.getDict())
                        else:
                            dic = attr.__dict__
                            if '_state' in dic:
                                dic.pop('_state')
                            l.append(dic)
                    d[m] = l
        # 由于ManyToMany类不能存在于_meat.fields，因而子类需要在getMtMFiled中返回这些字段
        if 'basemodel_ptr' in d:
            d.pop('basemodel_ptr')
        ignoreList = self.getIgnoreList()
        if ignoreList is not None:
            for m in ignoreList:
                if d.get(m) is not None:
                    d.pop(m)
        # 移除不需要的字段
        return d

    # 返回self._meta.fields中没有的，但是又是需要的字段名的列表
    # 形如['name','type']
    def getMtMField(self):
        pass

    # 返回需要在json中忽略的字段名的列表
    # 形如['password']
    def getIgnoreList(self):
        pass

    def isAttrInstance(self, attr, clazz):
        return isinstance(getattr(self, attr), clazz)

    def toJSON(self):
        import json
        return json.dumps(self.getDict(), ensure_ascii=False).encode('utf-8').decode()


class UserInfo(BaseTable):
    """
    用户注册信息表
    """

    class Meta:
        verbose_name = "用户信息"
        db_table = "UserInfo"

    username = models.CharField('用户名', max_length=20, unique=True, null=False)
    password = models.CharField('登陆密码', max_length=100, null=False)
    email = models.EmailField('用户邮箱', max_length=100, unique=True, null=False)


class TsignUserInfo(BaseTable):
    """
    用户注册信息表
    """

    class Meta:
        verbose_name = "用户信息"
        db_table = "TsignUserInfo"

    userid = models.CharField('用户Id', max_length=50, unique=True, null=False)
    alias = models.CharField('花名', max_length=20)
    username = models.CharField('用户名', max_length=20, unique=True, null=False)
    email = models.EmailField('用户邮箱', max_length=100, unique=True, null=False)


class UserToken(BaseTable):
    """
    用户登陆token
    """

    class Meta:
        verbose_name = "用户登陆token"
        db_table = "UserToken"

    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
    token = models.CharField('token', max_length=50)
