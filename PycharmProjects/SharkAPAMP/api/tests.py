from django.test import TestCase

# Create your tests here.

# log_info = "<p>资产 [ {} ] 的 [ {} ] 由 [ {} ] 变更为： [ {} ]</p>"
#
# for i in range(2):
#     a = log_info.format(i,i,i,i)
#     print(a)
# import test2
# b=getattr(test2,'func')
# print(b)

"""
资产 [ s1.com ] 的 [ manufacturer ] 由 [ Parallels Software International Inc. ] 变更为： [  Parallels Software International Inc. ]|
资产 [ s1.com ] 的 [ model ] 由 [ Parallels Virtual Platform ] 变更为： [  Parallels Virtual Platform ]|
资产 [ s1.com ] 的 [ sn ] 由 [ Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30 ] 变更为： [  Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30 ]|资产 [ s1.com ] 的 [ model_name ] 由 [ Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz ] 变更为： [  Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz ]
"""

a =['资产 [ s2.com ] 的 [ manufacturer ] 由 [ Parallels Software International Inc. ] 变更为： [  Parallels Software International Inc. ]', '资产 [ s2.com ] 的 [ model ] 由 [ Parallels Virtual Platform ] 变更为： [  Parallels Virtual Platform ]', '资产 [ s2.com ] 的 [ sn ] 由 [ Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30 ] 变更为： [  Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30 ]', '资产 [ s2.com ] 的 [ model_name ] 由 [ Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz ] 变更为： [  Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz ]']
a[0]