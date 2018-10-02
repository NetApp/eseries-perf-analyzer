#!/usr/bin/python

from ansible.module_utils.basic import *

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: grafana_dashboard_cleanup

short_description: Cleanup exported Grafana Dashboards so they can be re-imported.

version_added: "2.4"

description:
    - "Cleanup exported Grafana Dashboards so they can be re-imported."

options:
    dashboard:
        description:
            - A json String representing the dashboard
        required: true

author:
    - Michael Price (@lmprice)
'''

fields = {
    "dashboard": {"required": True, "type": "str"},
}

import json


def main():
    module = AnsibleModule(argument_spec=fields)
    data = module.params['dashboard']
    data = json.loads(data)
    data['dashboard']['id'] = None
    data['dashboard']['refresh'] = "5s"
    data['dashboard']['time'] = {
        "from": "now-5m",
        "to": "now"
    }
    module.exit_json(changed=True, json=data)


if __name__ == '__main__':
    main()
