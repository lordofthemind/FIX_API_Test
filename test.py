import quickfix as fix
import logging
from fix_messages import create_heartbeat
from cred.cred import SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID

class Application(fix.Application):
    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")
        self.send_heartbeat(sessionID)

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
        self.onMessage(message, sessionID)

    def onMessage(self, message, sessionID):
        logging.info(f"Message received: {message}")

    def send_heartbeat(self, sessionID):
        seq_num = 1  # Adjust the sequence number as necessary
        heartbeat_msg = create_heartbeat(SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID, seq_num)
        fix.Session.sendToTarget(heartbeat_msg, sessionID)

def main():
    logging.basicConfig(level=logging.INFO)
    
    settings = fix.SessionSettings("client.cfg")
    application = Application()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
    
    initiator.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        initiator.stop()

if __name__ == "__main__":
    main()
