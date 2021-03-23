#!/usr/bin/env python
# coding:utf8


import sys
sys.path.append("../")
from playbook_runner import PlaybookRunner
from pprint import pprint

host_dict = {
    "group1": {
        'hosts': ["172.16.153.130", "172.16.153.131", "172.16.153.132"],
        'vars': {'host': 'var_value'}
    },
    "_meta":{
        "hostvars":{
            "172.16.153.130":{
                "zone_dirs": ["/home/gjobs3","/home/gjobs2"]
                }
            }
        }
}


runner = PlaybookRunner(
    # playbook_path="two_play.yml",
    playbook_path="debug.yml",
    hosts=host_dict,
)


try:
    results = runner.run()
    pprint(results)
except Exception as e:
    print(e)
