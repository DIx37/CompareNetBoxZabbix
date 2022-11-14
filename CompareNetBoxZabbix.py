#!/usr/bin/python3
# Dmitrii Karnov <dkarnov@gmail.com>


from dcim.models import Device
from extras.scripts import *
from pyzabbix import ZabbixAPI


Z_URL = "http://"
Z_LOGIN = ""
Z_PASS = ""


class GetProviderInfo(Script):
	class Meta:
		name = "Compare NetBox Zabbix"
		description = "Сравнение NetBox и Zabbix"
		commit_default = False
		job_timeout = 120


	def run(self, data, commit):
		try:
			z = ZabbixAPI(Z_URL, user = Z_LOGIN, password = Z_PASS)


			n_devices = Device.objects.all()
			z_devices = z.host.get(output=['name'])


			for n_device in n_devices:
				compare = False
				for z_device in z_devices:
					if n_device.name == z_device['name']:
						compare = True
				if compare == False:
					self.log_info(f"{n_device.name} - Нет в Zabbix")
				else:
					self.log_info(f"{n_device.name} - Есть в Zabbix")



			self.log_success("Скрипт успешно завершён")
			return n_devices, z_devices
		except Exception as err:
			self.log_failure(f"Произошла ошибка:\n{err}")