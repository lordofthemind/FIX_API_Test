import quickfix as fix
import logging
import time


class MyApplication(fix.Application):
    def __init__(self):
        self.logged_in = False
        self.heartbeat_sent = False

    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")
        self.sendHeartbeat(sessionID)
        self.logged_in = True

    def sendHeartbeat(self, sessionID):
        heartbeat_msg = fix.Message()
        header = heartbeat_msg.getHeader()
        header.setField(fix.BeginString(fix.BeginString_FIX44))
        header.setField(fix.MsgType(fix.MsgType_Heartbeat))
        fix.Session.sendToTarget(heartbeat_msg, sessionID)
        self.heartbeat_sent = True  # Mark as heartbeat sent

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")
        self.logged_in = False

    def toAdmin(self, message, sessionID):
        logging.info(f"ToAdmin: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"FromAdmin: {message}")
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)
        if msg_type.getValue() == fix.MsgType_Logon:
            self.logged_in = True
        elif msg_type.getValue() == fix.MsgType_Heartbeat:
            self.heartbeat_sent = True

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
    settings = fix.SessionSettings("client_market_data.cfg")
    application = MyApplication()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    initiator.start()

    try:
        while True:
            if application.logged_in:
                if application.heartbeat_sent:
                    logging.info("Heartbeat sent successfully")
                    logging.info("Login successful")
                    break
                else:
                    logging.info("Waiting for heartbeat to be sent...")
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Exiting...")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        initiator.stop()


if __name__ == "__main__":
    main()
