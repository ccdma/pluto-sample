import abc

class DeviceFlow:
	def on_init(self):
		pass

	def on_before_destroy(self):
		pass

	def on_destroy(self):
		pass

class TxFlow(DeviceFlow):

	def on_send_start(self):
		pass

	def on_send_end(self):
		pass
	
class RxFlow(DeviceFlow):

	def on_read_start(self):
		pass

	def on_read_end(self):
		pass

