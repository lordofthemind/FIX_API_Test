import quickfix as fix
import logging
from fix_messages import (
    create_heartbeat,
    create_market_data_request,
    create_market_data_request_reject,
    create_market_data_snapshot_full_refresh,
    create_new_order_single,
    create_order_cancel_request,
)
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
        self.send_market_data_request_reject(sessionID)
        self.send_market_data_snapshot_full_refresh(sessionID)
        self.send_new_order_single(sessionID)
        self.send_order_cancel_request(sessionID)

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

        if msg_type.getValue() == fix.MsgType_MarketDataRequestReject:
            logging.info("Received Market Data Request Reject:")
            print(message.toString())
            self.handle_market_data_request_reject(message)

        elif msg_type.getValue() == fix.MsgType_MarketDataSnapshotFullRefresh:
            logging.info("Received Market Data Snapshot Full Refresh:")
            print(message.toString())
            self.handle_market_data_snapshot_full_refresh(message)

        elif msg_type.getValue() == fix.MsgType_ExecutionReport:
            logging.info("Received Execution Report:")
            print(message.toString())
            self.handle_execution_report(message)

        elif msg_type.getValue() == fix.MsgType_OrderCancelReject:
            logging.info("Received Order Cancel Reject:")
            print(message.toString())
            self.handle_order_cancel_reject(message)

        else:
            logging.info(f"Received unknown message type: {msg_type}")

    def onMessage(self, message, sessionID):
        logging.info(f"Message received: {message}")

    def send_market_data_request(self, sessionID):
        seq_num = 1  # Adjust the sequence number as necessary
        md_req_id = "MDREQ001"  # Unique ID for the market data request
        symbol = random.choice(symbols)
        depth_level = 1  # Specify the depth level for the market data
        market_data_request_msg = create_market_data_request(
            SENDER_COMP_ID_FOR_MARKET_DATA,
            TARGET_COMP_ID,
            seq_num,
            md_req_id,
            symbol,
            depth_level,
        )
        fix.Session.sendToTarget(market_data_request_msg, sessionID)

    def send_heartbeat(self, sessionID):
        seq_num = 1  # Adjust the sequence number as necessary
        heartbeat_msg = create_heartbeat(
            SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID, seq_num
        )
        fix.Session.sendToTarget(heartbeat_msg, sessionID)

    def send_market_data_request_reject(self, sessionID):
        seq_num = 2  # Adjust the sequence number as necessary
        md_req_id = "MDREQ002"  # Unique ID for the market data request
        market_data_request_reject_msg = create_market_data_request_reject(
            SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID, seq_num, md_req_id
        )
        fix.Session.sendToTarget(market_data_request_reject_msg, sessionID)

    def send_market_data_snapshot_full_refresh(self, sessionID):
        seq_num = 3  # Adjust the sequence number as necessary
        md_req_id = "MDREQ003"  # Unique ID for the market data request
        market_data_snapshot_full_refresh_msg = (
            create_market_data_snapshot_full_refresh(
                SENDER_COMP_ID_FOR_MARKET_DATA, TARGET_COMP_ID, seq_num, md_req_id
            )
        )
        fix.Session.sendToTarget(market_data_snapshot_full_refresh_msg, sessionID)

    def send_new_order_single(self, sessionID):
        seq_num = 4  # Adjust the sequence number as necessary
        cl_ord_id = "ORD123"  # Unique ID for the order
        order_qty = 100  # Quantity of the order
        ord_type = fix.OrdType_LIMIT  # Order type
        price = 150.0  # Price of the order
        time_in_force = fix.TimeInForce_IOC  # Time in force
        new_order_single_msg = create_new_order_single(
            SENDER_COMP_ID_FOR_MARKET_DATA,
            TARGET_COMP_ID,
            seq_num,
            cl_ord_id,
            order_qty,
            ord_type,
            price,
            time_in_force,
        )
        fix.Session.sendToTarget(new_order_single_msg, sessionID)

    def send_order_cancel_request(self, sessionID):
        seq_num = 5  # Adjust the sequence number as necessary
        cl_ord_id = "ORD124"  # Unique ID for the cancel order
        orig_cl_ord_id = "ORD123"  # Original order ID to cancel
        symbol = random.choice(symbols)  # Symbol for the order
        side = fix.Side_BUY  # Side of the order (buy/sell)
        order_cancel_request_msg = create_order_cancel_request(
            SENDER_COMP_ID_FOR_MARKET_DATA,
            TARGET_COMP_ID,
            seq_num,
            cl_ord_id,
            orig_cl_ord_id,
            symbol,
            side,
        )
        fix.Session.sendToTarget(order_cancel_request_msg, sessionID)

    def handle_market_data_request_reject(self, message):
        # Extract and log relevant fields from the Market Data Request Reject message
        md_req_id = fix.MDReqID()
        message.getField(md_req_id)
        text = fix.Text()
        message.getField(text)
        logging.info(
            f"Market Data Request Reject - MDReqID: {md_req_id.getValue()}, Text: {text.getValue()}"
        )

    def handle_market_data_snapshot_full_refresh(self, message):
        # Extract and log relevant fields from the Market Data Snapshot Full Refresh message
        md_req_id = fix.MDReqID()
        message.getField(md_req_id)
        no_md_entries = fix.NoMDEntries()
        message.getField(no_md_entries)
        logging.info(
            f"Market Data Snapshot Full Refresh - MDReqID: {md_req_id.getValue()}, NoMDEntries: {no_md_entries.getValue()}"
        )
        for i in range(no_md_entries.getValue()):
            group = fix.Group(268, 269)
            message.getGroup(i + 1, group)
            md_entry_type = fix.MDEntryType()
            md_entry_px = fix.MDEntryPx()
            md_entry_size = fix.MDEntrySize()
            group.getField(md_entry_type)
            group.getField(md_entry_px)
            group.getField(md_entry_size)
            logging.info(
                f"Entry {i + 1}: Type: {md_entry_type.getValue()}, Price: {md_entry_px.getValue()}, Size: {md_entry_size.getValue()}"
            )

    def handle_execution_report(self, message):
        # Extract and log relevant fields from the Execution Report message
        cl_ord_id = fix.ClOrdID()
        message.getField(cl_ord_id)
        order_id = fix.OrderID()
        message.getField(order_id)
        exec_id = fix.ExecID()
        message.getField(exec_id)
        exec_type = fix.ExecType()
        message.getField(exec_type)
        ord_status = fix.OrdStatus()
        message.getField(ord_status)
        logging.info(
            f"Execution Report - ClOrdID: {cl_ord_id.getValue()}, OrderID: {order_id.getValue()}, ExecID: {exec_id.getValue()}, ExecType: {exec_type.getValue()}, OrdStatus: {ord_status.getValue()}"
        )

    def handle_order_cancel_reject(self, message):
        # Extract and log relevant fields from the Order Cancel Reject message
        cl_ord_id = fix.ClOrdID()
        message.getField(cl_ord_id)
        orig_cl_ord_id = fix.OrigClOrdID()
        message.getField(orig_cl_ord_id)
        ord_status = fix.OrdStatus()
        message.getField(ord_status)
        cxl_rej_response_to = fix.CxlRejResponseTo()
        message.getField(cxl_rej_response_to)
        logging.info(
            f"Order Cancel Reject - ClOrdID: {cl_ord_id.getValue()}, OrigClOrdID: {orig_cl_ord_id.getValue()}, OrdStatus: {ord_status.getValue()}, CxlRejResponseTo: {cxl_rej_response_to.getValue()}"
        )


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
