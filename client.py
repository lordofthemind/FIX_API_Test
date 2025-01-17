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
        # Send a test message after logon
        self.send_initial_messages(sessionID)

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
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)

        if msg_type.getValue() == fix.MsgType_ExecutionReport:
            self.on_execution_report(message)
        # Handle other message types as necessary

    def send_initial_messages(self, sessionID):
        # Example: send a market data request after logon
        md_req_id = "MDReqID123"
        depth_level = 1
        market_data_request = create_market_data_request(SENDER_COMP_ID, TARGET_COMP_ID, 1, md_req_id, depth_level)
        fix.Session.sendToTarget(market_data_request, sessionID)

    def on_execution_report(self, msg):
        exec_type = fix.ExecType()
        msg.getField(exec_type)

        if exec_type.getValue() == fix.ExecType_NEW:
            logging.info("New order execution report received.")
            # Process new order execution report
        elif exec_type.getValue() == fix.ExecType_REJECTED:
            logging.info("Order rejected execution report received.")
            # Process rejected order execution report
        # Add more conditions as per your requirements

def main():
    logging.basicConfig(level=logging.INFO)
    
    settings = fix.SessionSettings("client.cfg")
    application = Application()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
    
    initiator.start()
    
    try:
        # Perform logon
        session_id = fix.SessionID("FIX.4.4", SENDER_COMP_ID, TARGET_COMP_ID)
        logon_message = create_logon(SENDER_COMP_ID, TARGET_COMP_ID, 1, USERNAME, PASSWORD)
        fix.Session.sendToTarget(logon_message, session_id)
        
        # Keep the application running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        initiator.stop()

if __name__ == "__main__":
    main()
