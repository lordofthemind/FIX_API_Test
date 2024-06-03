import quickfix as fix
import logging
from datetime import datetime


class MyApplication(fix.Application):
    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")
        self.sendHeartbeat(sessionID)

    def sendHeartbeat(self, sessionID):
        heartbeat_msg = fix.Message()
        header = heartbeat_msg.getHeader()
        header.setField(fix.BeginString(fix.BeginString_FIX44))
        header.setField(fix.MsgType(fix.MsgType_Heartbeat))
        fix.Session.sendToTarget(heartbeat_msg, sessionID)

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        logging.info(f"ToAdmin: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"FromAdmin: {message}")

    def toApp(self, message, sessionID):
        logging.info(f"ToApp: {message}")

    def fromApp(self, message, sessionID):
        logging.info(f"FromApp: {message}")


def setup_logging():
    logging.basicConfig(
        filename="fix_log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()
    settings = fix.SessionSettings("fix_client.cfg")
    application = MyApplication()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    initiator.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        initiator.stop()


if __name__ == "__main__":
    main()
