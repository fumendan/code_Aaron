#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from django.forms import widgets
from db.models import ModuleInfo, ConnectionInfo


"""
在这个页面的所有代码和数据均是静态字段，只在程序启动时运行一次，之后把获取到的
数据放在内存中，以后就不会再修改。
"""


class OctopusForm(forms.Form):
    """
    模块
    """
    # 只包含 字母/数组/下划线/连字符(-)
    module_name = forms.SlugField(min_length=5,
                                  max_length=64,
                                  label="模块名",
                                  error_messages={
                                      'required': '模块名称不能为空',  # 自定义错误信息
                                      'min_length': '模块名不能小于5个字符',
                                      'max_lenght': '模块名不能大于64个字符',
                                      'invalid': '模块名无效，只能包含字母/数组/下划线/连字符(-)',
                                  },
                                  widget=widgets.TextInput(
                                      attrs={
                                          "class": "validate[required,maxSize[8]]  form-control shark_form",
                                          "placeholder": "模块名仅支持英文/数组/下划线和段横杠的组合，且不能以开头"
                                      }),
                                  )
    module_type = forms.IntegerField(
        error_messages={
            'required': '请选择一个模块类型',
        },
        label="模块类型",
        widget=widgets.Select(
            choices=ModuleInfo.type_chioces,
            attrs={'class': 'form-control shark_form'}
        ),
    )
    module_lang = forms.IntegerField(
        error_messages={
            'required': '请选择一种开发语言',
        },
        label="开发语言",
        widget=widgets.Select(
            choices=ModuleInfo.lang_chioces,
            attrs={'class': 'form-control shark_form', }
        ),

    )

    module_info = forms.CharField(
        min_length=5,
        error_messages={
            'required': '对于此模块的功能或其它描述信息是必须的',
            'min_length': '描述的信息不可少于 10 个字符',
        },
        widget=widgets.Textarea(
            attrs={"class": "form-control shark_form", "rows": "10", "placeholder": "模块描述信息"})
    )

    module_file = forms.FileField(
        required=False,
        widget=widgets.ClearableFileInput(
            attrs={"multiple": True, "class": "file shark_form", "data-preview-file-type": "any"}
        ),
    )

    # module_path = forms.FilePathField(
    #     # 设置为 False 用意在于，这个字段只用于展示
    #     required=False,
    #     path="/Users/yanshunjun/PycharmProjects/SKCMDB/SharkAPAMP/octopus/modules/",
    #
    #     # 默认 Fasle 只用直接位于 path 路径下的目录或文件作为选择的路径，否则递归 path 的路径
    #     # recursive=True,
    #     match=r'^(?!__).*$',  # 排除以'__'开头的文件，比如 '__init__', '__pycache__'
    #     widget=widgets.Select(attrs={'hidden': True})
    # )


def choices_handler(modle_obj, field_id, field_name):
    choices_list = list(modle_obj.objects.all().values_list(field_id, field_name))
    choices_list.append((0, '--------'))
    return choices_list


class TaskForm(forms.Form):
    """任务"""
    module_name = forms.IntegerField(
        error_messages={
            'required': '模块名是必选的',
        },
        label="模块名称",
        widget=widgets.Select(
            # choices 的值是支持函数的
            choices=choices_handler(ModuleInfo, 'id', 'module_name'),
            attrs={'class': 'form-control'}
        ),
        initial=0,
    )

    remote_user = forms.IntegerField(
        error_messages={
            'required': '远程用户名不存在，请联系管理员，先在连接信息表里创建此用户',
        },
        widget=widgets.Select(
            choices=choices_handler(ConnectionInfo, 'id', 'remote_user'),
            attrs={'class': 'form-control'},
        ),
        initial=0,

    )

    module_type = forms.IntegerField(
        error_messages={
            'required': '请选择一个模块类型',
        },
        label="模块类型",
        widget=widgets.Select(
            choices=ModuleInfo.type_chioces,
            attrs={'class': 'form-control shark_form'}
        ),
        # initial=1,
    )

    exec_args = forms.CharField(
        error_messages={
            'required': "命令参数无效"
        },
        widget=widgets.TextInput(
            attrs={

                "class": "form-control",
                "style": "width: 90%",
                "placeholder": "填写执行 命令/模块 的参数，必填项"
            }),
    )
