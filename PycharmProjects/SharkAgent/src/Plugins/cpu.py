#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from .basicplugin import BasicPlugin

# 继承 BasicPlugin
class Cpu(BasicPlugin):
    def cmd_handler(self, debug=True):
        """
        model_name    型号
        physical_count   物理个数
        physical_cores     每颗物理 CPU 的核心数
        processor_cores_count     逻辑核心数
        :return:
        """
        if debug:
            import glob
            f = glob.glob('./files/cpu*')[0]
            cpu_info = {
                'model_name': self.run_cmd("grep 'model name' {} | uniq |cut -d: -f2 |sed s'/[[:space:]][[:space:]]*/ /'".format(f)),
                'cpu_type': "x86_64",
                'physical_count': int(self.run_cmd("grep 'physical id' {} | sort -u | wc -l".format(f))),
                'physical_cores': int(self.run_cmd("grep 'cpu cores' {} | uniq | cut -d: -f2".format(f))),
                'processor_cores_count': int(self.run_cmd("grep 'processor'  {}  | wc -l".format(f)))
            }

        else:
            cpu_info = {
                'model_name': self.run_cmd("grep 'model name' /proc/cpuinfo | uniq |cut -d: -f2"),
                'cpu_type': self.run_cmd('uname -p'),
                'physical_count': int(self.run_cmd("grep 'physical id' /proc/cpuinfo | sort -u | wc -l").strip()),
                'physical_cores': int(self.run_cmd("grep 'cpu cores' /proc/cpuinfo | uniq |cut -d: -f2").strip()),
                'processor_cores_count': int(self.run_cmd("grep 'processor'  /proc/cpuinfo  | wc -l").strip())
            }
            cpu_info['model_name'] = ' '.join(cpu_info['model_name'].split())
        return cpu_info

###############
#  Ansible code 
###############
    #  def get_file_content(slef, path, default=None, strip=True):
    #     data = default
    #     if os.path.exists(path) and os.access(path, os.R_OK):
    #         try:
    #             try:
    #                 datafile = open(path)
    #                 data = datafile.read()
    #                 if strip:
    #                     data = data.strip()
    #                 if len(data) == 0:
    #                     data = default
    #             finally:
    #                 datafile.close()
    #         except:
    #             # ignore errors as some jails/containers might have readable permissions but not allow reads to proc
    #             # done in 2 blocks for 2.4 compat
    #             pass
    #     return data
    #
    # def get_file_lines(slef, path, strip=True):
    #     '''get list of lines from file'''
    #     data = slef.get_file_content(path, strip=strip)
    #     if data:
    #         ret = data.splitlines()
    #     else:
    #         ret = []
    #     return ret
    #
    # def cmd_handler(slef, collected_facts=None):
    #     cpu_facts = {}
    #     collected_facts = collected_facts or {}
    #
    #     i = 0
    #     vendor_id_occurrence = 0
    #     model_name_occurrence = 0
    #     physid = 0
    #     coreid = 0
    #     sockets = {}
    #     cores = {}
    #
    #     xen = False
    #     xen_paravirt = False
    #     try:
    #         if os.path.exists('/proc/xen'):
    #             xen = True
    #         else:
    #             for line in slef.get_file_lines('/sys/hypervisor/type'):
    #                 if line.strip() == 'xen':
    #                     xen = True
    #                 # Only interested in the first line
    #                 break
    #     except IOError:
    #         pass
    #
    #     if not os.access("/proc/cpuinfo", os.R_OK):
    #         return cpu_facts
    #
    #     cpu_facts['processor'] = []
    #     for line in slef.get_file_lines('/proc/cpuinfo'):
    #         data = line.split(":", 1)
    #         key = data[0].strip()
    #         print('===>',key)
    #         if xen:
    #             if key == 'flags':
    #                 # Check fors vme cpu flag, Xen paravirt does not expose this.
    #                 #   Need to detect Xen paravirt because it exposes cpuinfo
    #                 #   differently than Xen HVM or KVM and causes reporting of
    #                 #   only a single cpu core.
    #                 if 'vme' not in data:
    #                     xen_paravirt = True
    #
    #         # model name is for Intel arch, Processor (mind the uppercase P)
    #         # works for some ARM devices, like the Sheevaplug.
    #         # 'ncpus active' is SPARC attribute
    #         if key in ['model name', 'Processor', 'vendor_id', 'cpu', 'Vendor', 'processor']:
    #             if 'processor' not in cpu_facts:
    #                 cpu_facts['processor'] = []
    #             cpu_facts['processor'].append(data[1].strip())
    #             if key == 'vendor_id':
    #                 vendor_id_occurrence += 1
    #             if key == 'model name':
    #                 model_name_occurrence += 1
    #             i += 1
    #         elif key == 'physical id':
    #             physid = data[1].strip()
    #             if physid not in sockets:
    #                 sockets[physid] = 1
    #         elif key == 'core id':
    #             coreid = data[1].strip()
    #             if coreid not in sockets:
    #                 cores[coreid] = 1
    #         elif key == 'cpu cores':
    #             sockets[physid] = int(data[1].strip())
    #         elif key == 'siblings':
    #             cores[coreid] = int(data[1].strip())
    #         elif key == '# processors':
    #             cpu_facts['processor_cores'] = int(data[1].strip())
    #         elif key == 'ncpus active':
    #             i = int(data[1].strip())
    #
    #     # Skip for platforms without vendor_id/model_name in cpuinfo (e.g ppc64le)
    #     if vendor_id_occurrence > 0:
    #         if vendor_id_occurrence == model_name_occurrence:
    #             i = vendor_id_occurrence
    #
    #     # FIXME
    #     if collected_facts.get('ansible_architecture') != 's390x':
    #         if xen_paravirt:
    #             cpu_facts['processor_count'] = i
    #             cpu_facts['processor_cores'] = i
    #             cpu_facts['processor_threads_per_core'] = 1
    #             cpu_facts['processor_vcpus'] = i
    #         else:
    #             if sockets:
    #                 cpu_facts['processor_count'] = len(sockets)
    #             else:
    #                 cpu_facts['processor_count'] = i
    #
    #             socket_values = list(sockets.values())
    #             if socket_values and socket_values[0]:
    #                 cpu_facts['processor_cores'] = socket_values[0]
    #             else:
    #                 cpu_facts['processor_cores'] = 1
    #
    #             core_values = list(cores.values())
    #             if core_values:
    #                 cpu_facts['processor_threads_per_core'] = core_values[0] // cpu_facts['processor_cores']
    #             else:
    #                 cpu_facts['processor_threads_per_core'] = 1 // cpu_facts['processor_cores']
    #
    #             cpu_facts['processor_vcpus'] = (cpu_facts['processor_threads_per_core'] *
    #                                             cpu_facts['processor_count'] * cpu_facts['processor_cores'])
    #
    #     return cpu_facts

