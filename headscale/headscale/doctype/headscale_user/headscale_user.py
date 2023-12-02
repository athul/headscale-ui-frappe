# Copyright (c) 2023, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests


class HeadScaleUser(Document):
    def autoname(self):
        self.name = self.headscale_user

    @frappe.whitelist()
    def get_machines(self):
        hds = frappe.get_single("HeadScale Settings")
        uri = hds.headscale_url + "/api/v1/machine"
        print(uri)
        api_key = hds.get_password("headscale_api_key")
        print(api_key)
        req = requests.get(
            uri,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        print("Heeeeeeeeeeeeeeeeere")
        print(req.status_code)
        if req.ok:
            print("Yaaaaaaaaaaaaay")
            jsn = req.json()
            print(str(jsn["machines"][0]))
            # self.js = str(jsn)
            for machine in jsn["machines"]:
                if not frappe.db.exists("HeadScale Machine", machine["givenName"]):
                    new_machine = frappe.get_doc(
                        {
                            "doctype": "HeadScale Machine",
                            "machine_id": machine["id"],
                            "machine_key": machine["machineKey"],
                            "machine_ip": machine["ipAddresses"][
                                len(machine["ipAddresses"]) - 1
                            ],
                            "machine_ipv6": machine["ipAddresses"][0],
                            "machine_hostname": machine["name"],
                            "machine_name": machine["givenName"],
                            "machine_status": "Online"
                            if machine["online"]
                            else "Offline",
                            "machine_user": machine["user"]["name"],
                        }
                    )
                    new_machine.insert()

                    if machine["user"]["name"] == self.headscale_user:
                        self.append(
                            "machines",
                            {
                                "machine": new_machine.name,
                            },
                        )
                        self.save()
                #             "machine_ip": machine["ipAddresses"][1],
                #             "machine_ipv6": machine["ipAddresses"][0],
                #             "machine_hostname": machine["name"],
                #             "machine_name": machine["givenName"],
                #         },
                #     )
                #     self.save()

