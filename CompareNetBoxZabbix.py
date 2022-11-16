#!/usr/bin/python3
# Dmitrii Karnov <dkarnov@gmail.com>


from dcim.models import Device, DeviceType, Region, Site, Location
from extras.scripts import *
from pyzabbix import ZabbixAPI


Z_URL = "http://172.16.2.107"
Z_LOGIN = "admin"
Z_PASS = "Gjyzirb37"


class GetProviderInfo(Script):
	class Meta:
		name = "Compare NetBox Zabbix"
		description = "Сравнение NetBox и Zabbix"
		commit_default = False
		job_timeout = 120


	region = ObjectVar(
		model = Region,
		description = "Выберите Регион",
		required = False
	)


	site = ObjectVar(
		model = Site,
		description = "Выберите Объект",
		required = False
	)


	location = ObjectVar(
		model = Location,
		description = "Выберите Локацию",
		required = False
	)


	device_type = ObjectVar(
		model = DeviceType,
		description = "Выберите Тип Устройства",
		required = False
	)


	def run(self, data, commit):
		try:
			z = ZabbixAPI(Z_URL, user = Z_LOGIN, password = Z_PASS)


			n_devices = Device.objects.all()
			z_devices = z.host.get(output=['name'])


			log_info = "<b>Нет в Zabbix</b><p>"
			for n_device in n_devices:
				compare = False
				for z_device in z_devices:
					if n_device.name == z_device['name']:
						compare = True
				if compare == False:
					log_info += f"&nbsp;&nbsp;&nbsp;- {n_device.name}<p>"
			self.log_info(log_info)


			self.log_success("Скрипт успешно завершён")
		except Exception as err:
			self.log_failure(f"Произошла ошибка:\n{err}")