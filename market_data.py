import quickfix as fix
import quickfix44 as fix44
import logging
from fix_messages import (
    create_heartbeat, create_test_request, create_logon, create_logout,
    create_resend_request, create_reject, create_business_reject,
    create_sequence_reset, create_market_data_request, create_new_order_single,
    create_order_status_request
)
from datetime import datetime
import time
import cred

# Define constants for SENDER_COMP_ID and TARGET_COMP_ID
SENDER_COMP_ID = cred.SENDER_COMP_ID
TARGET_COMP_ID = cred.MARKET_DATA_TARGET_COMP_ID

# Define constants for USERNAME and PASSWORD
USERNAME = cred.USERNAME
PASSWORD = cred.PASSWORD

def current_time():
    return datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]

class Application(fix.Application):
    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")

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
            session_id = fix.SessionID("FIX.4.4", SENDER_COMP_ID, TARGET_COMP_ID)
            fix.Session.sendToTarget(create_heartbeat(SENDER_COMP_ID, TARGET_COMP_ID), session_id)
            fix.Session.sendToTarget(create_test_request(SENDER_COMP_ID, TARGET_COMP_ID), session_id)
            fix.Session.sendToTarget(create_logon(SENDER_COMP_ID, TARGET_COMP_ID, USERNAME, PASSWORD), session_id)
            fix.Session.sendToTarget(create_logout(SENDER_COMP_ID, TARGET_COMP_ID), session_id)
            fix.Session.sendToTarget(create_resend_request(SENDER_COMP_ID, TARGET_COMP_ID), session_id)
            fix.Session.sendToTarget(create_reject(SENDER_COMP_ID, TARGET_COMP_ID), session_id)
            fix.Session.sendToTarget(create_business_reject(SENDER_COMP_ID, TARGET_COMP_ID), session_id)
            fix.Session.sendToTarget(create_sequence_reset(SENDER_COMP_ID, TARGET_COMP_ID), session_id)

            time.sleep(1)  # Sleep to avoid flooding the server with requests

    except KeyboardInterrupt:
        initiator.stop()

if __name__ == "__main__":
    main()
