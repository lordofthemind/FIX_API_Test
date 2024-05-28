import quickfix as fix
import quickfix44 as fix44
import logging
from fix_messages import (
    create_heartbeat, create_test_request, create_logon, create_logout,
    create_resend_request, create_reject, create_business_reject,
    create_sequence_reset, create_market_data_request, create_new_order_single,
    create_order_status_request
)

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
            time.sleep(1)
            session_id = fix.SessionID("FIX.4.4", "CLIENT", "MARKET")
            fix.Session.sendToTarget(create_heartbeat("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_test_request("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_logon("CLIENT", "MARKET", "Username", "Password"), session_id)
            fix.Session.sendToTarget(create_logout("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_resend_request("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_reject("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_business_reject("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_sequence_reset("CLIENT", "MARKET"), session_id)
            fix.Session.sendToTarget(create_market_data_request("CLIENT", "MARKET", "MDReqID1", 1), session_id)
            fix.Session.sendToTarget(create_new_order_single("CLIENT", "MARKET", "OrderID1", 1000, fix.OrdType_MARKET), session_id)
            fix.Session.sendToTarget(create_order_status_request("CLIENT", "MARKET", "OrderID1"), session_id)
            # Add additional messages as needed

    except KeyboardInterrupt:
        initiator.stop()

if __name__ == "__main__":
    main()
