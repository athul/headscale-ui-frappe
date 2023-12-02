# Copyright (c) 2023, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import requests


class HeadScaleMachine(Document):
    @frappe.whitelist()
    def rename_machine(self, new_name):
        hds = frappe.get_single("Headscale Settings")
        uri = hds.headscale_url + \
            f"/api/v1/machine/{self.machine_id}/rename/{new_name}"
        api_key = hds.get_password("headscale_api_key")
        req = requests.post(
            uri,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        if req.ok:
            machine = req.json()["machine"]
            self.machine_name = machine["givenName"]
            self.save()
            frappe.rename_doc("Headscale Machine",
                              self.name, self.machine_name)


@frappe.whitelist()
def update_machine_details():
    hds = frappe.get_single("Headscale Settings")
    uri = hds.headscale_url + f"/api/v1/machine"
    api_key = hds.get_password("headscale_api_key")
    req = requests.get(
        uri,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    print(req.status_code)

    if req.ok:
        machines = req.json()["machines"]
        for machine in machines:
            mdoc = frappe.get_doc("Headscale Machine", machine["givenName"])
            # mdoc.machine_ip = machine["ipAddresses"][len(
            #     machine["ipAddresses"]) - 1]
            # mdoc.machine_ipv6 = machine["ipAddresses"][0]
            # mdoc.machine_hostname = machine["name"]
            # mdoc.machine_name = machine["givenName"]
            mdoc.machine_status = "Online" if machine["online"] else "Offline"
            # mdoc.machine_user = machine["user"]["name"]
            mdoc.save()

