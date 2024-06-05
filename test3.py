import quickfix as fix
import quickfix44 as fix44
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Application(fix.Application):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)

        if msg_type.getValue() == fix.MsgType_Logon:
            message.setField(fix.Username(self.username))
            message.setField(fix.Password(self.password))
            logging.info(f"Added username and password to Logon message")

        logging.info(f"To Admin: {message}")

    def toApp(self, message, sessionID):
        logging.info(f"To App: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"From Admin: {message}")

    def fromApp(self, message, sessionID):
        logging.info(f"From App: {message}")
        self.onMessage(message, sessionID)

    def onMessage(self, message, sessionID):
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)

        if msg_type.getValue() == fix.MsgType_MarketDataRequestReject:
            logging.info("Market Data Request Reject received")
        elif msg_type.getValue() == fix.MsgType_MarketDataSnapshotFullRefresh:
            logging.info("Market Data Snapshot Full Refresh received")
        elif msg_type.getValue() == fix.MsgType_ExecutionReport:
            exec_type = fix.ExecType()
            message.getField(exec_type)
            if exec_type.getValue() == fix.ExecType_FILL:
                logging.info("Order Fully Filled")
            elif exec_type.getValue() == fix.ExecType_PARTIAL_FILL:
                logging.info("Order Partially Filled")


def send_market_data_request(sessionID, symbol, mdReqID, is_duplicate=False):
    try:
        message = fix44.MarketDataRequest()
        message.setField(fix.MDReqID(mdReqID))
        message.setField(
            fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT)
        )
        message.setField(fix.MarketDepth(1))

        group = fix44.MarketDataRequest.NoRelatedSym()
        group.setField(fix.Symbol(symbol))
        message.addGroup(group)

        fix.Session.sendToTarget(message, sessionID)
        logging.info(
            f"Market Data Request sent: {symbol}, {mdReqID}, Duplicate: {is_duplicate}"
        )
    except Exception as e:
        logging.error(f"Failed to send Market Data Request: {e}")


def send_new_order_single(
    sessionID, clOrdID, symbol, side, orderQty, price, timeInForce
):
    try:
        message = fix44.NewOrderSingle(
            fix.ClOrdID(clOrdID),
            fix.HandlInst(fix.HandlInst_MANUAL_ORDER),
            fix.Symbol(symbol),
            fix.Side(side),
            fix.TransactTime(),
            fix.OrdType(fix.OrdType_LIMIT),
        )
        message.setField(fix.OrderQty(orderQty))
        message.setField(fix.Price(price))
        message.setField(fix.TimeInForce(timeInForce))

        fix.Session.sendToTarget(message, sessionID)
        logging.info(
            f"New Order Single sent: {clOrdID}, {symbol}, {side}, {orderQty}, {price}, {timeInForce}"
        )
    except Exception as e:
        logging.error(f"Failed to send New Order Single: {e}")


def send_order_cancel_request(sessionID, origClOrdID, clOrdID, symbol, side):
    try:
        message = fix44.OrderCancelRequest(
            fix.OrigClOrdID(origClOrdID),
            fix.ClOrdID(clOrdID),
            fix.Symbol(symbol),
            fix.Side(side),
            fix.TransactTime(),
        )

        fix.Session.sendToTarget(message, sessionID)
        logging.info(
            f"Order Cancel Request sent: {origClOrdID}, {clOrdID}, {symbol}, {side}"
        )
    except Exception as e:
        logging.error(f"Failed to send Order Cancel Request: {e}")


def main():
    try:
        # Username and password for the FIX session
        username = "YourUsername"
        password = "YourPassword"

        # Configure and start the session
        settings = fix.SessionSettings("client_market_data.cfg")
        application = Application(username, password)
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

        initiator.start()

        # Example usage
        sessionID = fix.SessionID("FIX.4.4", "SENDER_COMP_ID", "TARGET_COMP_ID")

        # 1. Market Data Request Reject
        send_market_data_request(
            sessionID, "INVALID_SYMBOL", "DUPLICATE_MDREQID", is_duplicate=True
        )

        # 2. Market Data Snapshot Full Refresh
        send_market_data_request(sessionID, "VALID_SYMBOL", "UNIQUE_MDREQID")

        # 3. Limit IOC/FOK Orders
        send_new_order_single(
            sessionID,
            "ORDER_ID_1",
            "VALID_SYMBOL",
            fix.Side_BUY,
            100,
            50.0,
            fix.TimeInForce_IOC,
        )
        send_new_order_single(
            sessionID,
            "ORDER_ID_2",
            "VALID_SYMBOL",
            fix.Side_BUY,
            100,
            50.0,
            fix.TimeInForce_FOK,
        )

        # 4. Order Cancel Request
        send_order_cancel_request(
            sessionID, "ORIG_ORDER_ID", "CANCEL_ORDER_ID", "VALID_SYMBOL", fix.Side_BUY
        )

        # 5. Fully/Partially Filled Orders
        send_new_order_single(
            sessionID,
            "ORDER_ID_3",
            "VALID_SYMBOL",
            fix.Side_BUY,
            1000,
            50.0,
            fix.TimeInForce_DAY,
        )

        # Run indefinitely to process messages
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Interrupted by user")

        initiator.stop()
    except Exception as e:
        logging.error(f"Failed to start FIX application: {e}")


if __name__ == "__main__":
    main()
