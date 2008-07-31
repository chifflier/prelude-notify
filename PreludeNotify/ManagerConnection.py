from PreludeEasy import ClientEasy, Connection

import gobject

class Session:
	def __init__(self, env, hbmonitor):
		self.con = 0
		self.env = env
		self.hbmonitor = hbmonitor

	def doConnect(self):
        	#try:
	        self.con.Connect(self.env.client, ClientEasy.IDMEF_READ)
	        #except:
	        #       ProfileRegister.CreateProfile(c, ClientEasy.IDMEF_READ, env.config.get("idmef", "profile"))
	        #       sys.exit(1)
        	self.env.notify.run(None, None, "Manager Connection successfull", "With Prelude-Manager <b>%s</b>" % self.con.GetPeerAddr())

	def handleDisconnect(self, err=None):
		self.env.notify.run("high", None, "Manager Connection interrupted", "With Prelude-Manager <b>%s</b>" % self.con.GetPeerAddr())
		gobject.timeout_add(10000, self.doConnect)

	def ConnectAdresses(self, manager_addresses):
		manager_addresses = manager_addresses.split(',')
		for addr in manager_addresses:
		        self.con = Connection(addr)
		        self.doConnect()
		        gobject.io_add_watch(self.con.GetFd(), gobject.IO_IN|gobject.IO_PRI|gobject.IO_HUP|gobject.IO_NVAL|gobject.IO_ERR, self.io_cb, self.con)

	def io_cb(self, fd, cond, con):
		if cond & gobject.IO_IN:
			try:
				idmef = con.RecvIDMEF()
			except PreludeEasy.PreludeError, err:
				if err.GetErrorCode() == -8388614:
					self.handleDisconnect(con)
					return False

			if idmef.Get("heartbeat.create_time"):
				self.hbmonitor.heartbeat(idmef)

			elif (not self.env.criteria) or (self.env.criteria.match(idmef)):
				self.env.thresholding.thresholdMessage(idmef)

		if cond & gobject.IO_ERR or cond & gobject.IO_HUP:
			self.handleDisconnect(con)
			return False

		return True

