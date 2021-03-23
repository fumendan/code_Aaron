

class ClsMethod(object):
    clsk ='clsv'

    def __init__(self):
        self.key1 = 1

    @staticmethod
    def s_method():
        """
        静态方法不能访问实例属性和方法
        :return:
        """
        print('static method')
        print(ClsMethod.clsk)
        # print('key1', self.key1)


    @classmethod
    def cls_method(cls):
        """
        类方法也不能访问实例属性和方法
        :return:
        """
        print(ClsMethod.clsk)
        # print('key1', self.key1)

    def f_method(self):
        print(ClsMethod.clsk)
        print(self.key1)


#
# cm = ClsMethod()
# print('-' * 15)
# cm.s_method()
# print('-' * 15)
# cm.cls_method()
# print('-' * 15)
# cm.f_method()
# print('-' * 15)

# li = [{'manage_ip': '172.16.153.130','hostname':'gjzfapp1','port': 22, 'remote_user': 'root'},
#          {'manage_ip': '172.16.153.131','hostname':'gjzfapp2','port': 22, 'remote_user': 'root'},]
# play_list = []
# for item in li:
#     play_list.append(item.get('manage_ip'))
#
# li.append({'all_host_list': play_list})
# # print(li)
# [{'manage_ip': '172.16.153.130', 'hostname': 'gjzfapp1', 'port': 22, 'remote_user': 'root'},
#  {'manage_ip': '172.16.153.131', 'hostname': 'gjzfapp2', 'port': 22, 'remote_user': 'root'},
#  {'all_host_list': ['172.16.153.130', '172.16.153.131']}]
# for item in li:
#     if 'all_host_list' in item.keys():
#         print(item.get('all_host_list'))

class A():
    def __init__(self):
        self.a ='a'


class B():
    def __init__(self):
        self.b = 'b'

class C(B,A):
    def __init__(self):
        super().__init__()
        print(self.b)
        print(C.mro())

c = C()
