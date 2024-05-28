import quickfix as fix
import quickfix44 as fix44
import logging
from fix_messages import create_heartbeat, create_test_request, create_market_order

class Application(fix.Application):
    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")

        # Send a test message
        msg = create_heartbeat()
        fix.Session.sendToTarget(msg, sessionID)

        msg = create_test_request()
        fix.Session.sendToTarget(msg, sessionID)

        msg = create_market_order()
        fix.Session.sendToTarget(msg, sessionID)

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        logging.info(f"Sent to admin: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"Received from admin: {message}")

    def toApp(self, message, sessionID):
        logging.info(f"Sent to app: {message}")

    def fromApp(self, message, sessionID):
        logging.info(f"Received from app: {message}")

def main():
    logging.basicConfig(level=logging.INFO)
    settings = fix.SessionSettings("client.cfg")
    application = Application()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    initiator.start()
    logging.info("FIX client started")
    input("Press <Enter> to stop the client...\n")
    initiator.stop()

if __name__ == "__main__":
    main()
