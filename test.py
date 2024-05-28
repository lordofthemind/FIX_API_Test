import quickfix as fix
import logging
from fix_messages import create_heartbeat, create_market_data_request
from cred.cred import SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID
import time
import random
from symbols.symbols import SYMBOLS

symbols = SYMBOLS

class Application(fix.Application):
    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")
        self.send_heartbeat(sessionID)
        self.send_market_data_request(sessionID)

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        logging.info(f"ToAdmin: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"FromAdmin: {message}")

    def toApp(self, message, sessionID):
        logging.info(f"ToApp: {message}")

    def fromApp(self, message, sessionID):
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)

        if msg_type.getValue() == fix.MsgType_MarketDataSnapshotFullRefresh:
            # Handle market data snapshot full refresh message
            logging.info("Received market data snapshot full refresh:")
            print(message.toString())  # Print the entire message content

        elif msg_type.getValue() == fix.MsgType_MarketDataIncrementalRefresh:
            # Handle market data incremental refresh message
            logging.info("Received market data incremental refresh:")
            print(message.toString())  # Print the entire message content

        else:
            logging.info(f"Received unknown message type: {msg_type}")

    def onMessage(self, message, sessionID):
        logging.info(f"Message received: {message}")

    def send_market_data_request(self, sessionID):
        seq_num = 1  # Adjust the sequence number as necessary
        md_req_id = "MDREQ001"  # Unique ID for the market data request
        symbol = random.choice(symbols)
        depth_level = 1  # Specify the depth level for the market data
        market_data_request_msg = create_market_data_request(SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID, seq_num, md_req_id, symbol, depth_level)
        fix.Session.sendToTarget(market_data_request_msg, sessionID)

    def send_heartbeat(self, sessionID):
        seq_num = 1  # Adjust the sequence number as necessary
        heartbeat_msg = create_heartbeat(SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID, seq_num)
        fix.Session.sendToTarget(heartbeat_msg, sessionID)

def main():
    logging.basicConfig(level=logging.INFO)
    
    settings = fix.SessionSettings("client_market_data.cfg")
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