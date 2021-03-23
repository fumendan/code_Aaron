from .basicplugin import BasicPlugin


class BaseInfo(BasicPlugin):

    def cmd_handler(self, debug=True):
        """
        -s, --kernel-name		输出操作系统名称
        -n, --nodename		输出网络节点上的主机名
        -r, --kernel-release		输出内核发行号
        -v, --kernel-version		输出内核版本
        -m, --machine		输出主机的硬件架构名称
        -p, --processor		输出处理器类型或"unknown"
        -i, --hardware-platform	输出硬件平台或"unknown"
        -o, --operating-system	输出操作系统家族名称
        :param debug:
        :return:
        """
        if debug:
            result = {
                'os_name': 'linux',
                'machine': "i386",
                'os_version': "CentOS Linux release 7.3.1611 (Core)",
                'hostname': 's1.com',
                'kernel': '3.10.0-514.el7.x86_64 #1 SMP Tue Nov 22 16:42:41 UTC 201'
            }
        else:
            result = {
                'os_name': self.run_cmd('uname -s').strip(),
                'machine': self.run_cmd("uname -m").strip(),
                'os_version': self.run_cmd("cat /etc/redhat-release || cat /etc/issue").strip().split('\n')[0],
                'hostname': self.run_cmd("hostname").strip(),
                'kernel': self.run_cmd('uname -rv')
            }
        return result
