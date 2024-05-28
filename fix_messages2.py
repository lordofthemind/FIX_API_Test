import quickfix as fix
import random
from datetime import datetime
from symbols.symbols import SYMBOLS

symbols = SYMBOLS

def current_time():
    return datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]

# Standard messages
def create_standard_header(msg, msg_type, sender_comp_id, target_comp_id, seq_num):
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(msg_type))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(seq_num))
    header.setField(fix.SendingTime(current_time()))

def create_standard_trailer(msg):
    trailer = msg.getTrailer()
    trailer.setField(fix.CheckSum("000"))

# Session messages
def create_heartbeat(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_Heartbeat, sender_comp_id, target_comp_id, seq_num)
    create_standard_trailer(msg)
    return msg

def create_test_request(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_TestRequest, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.TestReqID("Test123"))
    create_standard_trailer(msg)
    return msg

def create_logon(sender_comp_id, target_comp_id, seq_num, username, password):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_Logon, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.EncryptMethod(fix.EncryptMethod_NONE))
    msg.setField(fix.HeartBtInt(30))
    msg.setField(fix.ResetSeqNumFlag(True))
    msg.setField(fix.Username(username))
    msg.setField(fix.Password(password))
    create_standard_trailer(msg)
    return msg

def create_logout(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_Logout, sender_comp_id, target_comp_id, seq_num)
    create_standard_trailer(msg)
    return msg

def create_resend_request(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_ResendRequest, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.BeginSeqNo(1))
    msg.setField(fix.EndSeqNo(0))  # Set to 0 for infinite
    create_standard_trailer(msg)
    return msg

def create_reject(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_Reject, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.RefSeqNum(1))
    msg.setField(fix.RefTagID(4))
    msg.setField(fix.RefMsgType("D"))
    msg.setField(fix.Text("Reject message"))
    create_standard_trailer(msg)
    return msg

def create_business_reject(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_BusinessMessageReject, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.RefSeqNum(1))
    msg.setField(fix.RefMsgType("D"))
    msg.setField(fix.BusinessRejectReason(fix.BusinessRejectReason_OTHER))
    msg.setField(fix.Text("Business reject message"))
    create_standard_trailer(msg)
    return msg

def create_sequence_reset(sender_comp_id, target_comp_id, seq_num):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_SequenceReset, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.GapFillFlag(True))
    msg.setField(fix.NewSeqNo(seq_num + 1))
    create_standard_trailer(msg)
    return msg

# Application messages: Market Data Session
def create_market_data_request(sender_comp_id, target_comp_id, seq_num, md_req_id, depth_level):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_MarketDataRequest, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.MDReqID(md_req_id))
    msg.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))
    msg.setField(fix.MarketDepth(depth_level))
    msg.setField(fix.MDUpdateType(fix.MDUpdateType_FULL_REFRESH))
    msg.setField(fix.NoRelatedSym(1))
    symbol_group = fix.Group(146, 55)
    symbol_group.setField(fix.Symbol(random.choice(symbols)))
    msg.addGroup(symbol_group)
    create_standard_trailer(msg)
    return msg

def create_market_data_request_reject(sender_comp_id, target_comp_id, seq_num, md_req_id):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_MarketDataRequestReject, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.MDReqID(md_req_id))
    msg.setField(fix.Text("Market data request reject"))
    create_standard_trailer(msg)
    return msg

def create_market_data_snapshot_full_refresh(sender_comp_id, target_comp_id, seq_num, md_req_id):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_MarketDataSnapshotFullRefresh, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.MDReqID(md_req_id))
    msg.setField(fix.NoMDEntries(1))
    md_entry_group = fix.Group(268, 269)
    md_entry_group.setField(fix.MDEntryType(fix.MDEntryType_BID))
    md_entry_group.setField(fix.MDEntryPx(1.2345))
    md_entry_group.setField(fix.MDEntrySize(1000))
    msg.addGroup(md_entry_group)
    create_standard_trailer(msg)
    return msg

# Application messages: Trading Session
def create_new_order_single(sender_comp_id, target_comp_id, seq_num, cl_ord_id, order_qty, ord_type, price=None, time_in_force=None):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_NewOrderSingle, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.ClOrdID(cl_ord_id))
    msg.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
    msg.setField(fix.Symbol(random.choice(symbols)))
    msg.setField(fix.Side(fix.Side_BUY))
    msg.setField(fix.TransactTime(current_time()))
    msg.setField(fix.OrderQty(order_qty))
    msg.setField(fix.OrdType(ord_type))
    if price:
        msg.setField(fix.Price(price))
    if time_in_force:
        msg.setField(fix.TimeInForce(time_in_force))
    create_standard_trailer(msg)
    return msg

def create_order_cancel_request(sender_comp_id, target_comp_id, seq_num, cl_ord_id, orig_cl_ord_id, symbol, side):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_OrderCancelRequest, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.ClOrdID(cl_ord_id))
    msg.setField(fix.OrigClOrdID(orig_cl_ord_id))
    msg.setField(fix.Symbol(symbol))
    msg.setField(fix.Side(side))
    msg.setField(fix.TransactTime(current_time()))
    create_standard_trailer(msg)
    return msg

def create_order_cancel_replace_request(sender_comp_id, target_comp_id, seq_num, cl_ord_id, orig_cl_ord_id, order_qty, price):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_OrderCancelReplaceRequest, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.ClOrdID(cl_ord_id))
    msg.setField(fix.OrigClOrdID(orig_cl_ord_id))
    msg.setField(fix.Symbol(random.choice(symbols)))
    msg.setField(fix.Side(fix.Side_BUY))
    msg.setField(fix.TransactTime(current_time()))
    msg.setField(fix.OrderQty(order_qty))
    msg.setField(fix.Price(price))
    msg.setField(fix.OrdType(fix.OrdType_LIMIT))
    create_standard_trailer(msg)
    return msg

def create_order_cancel_reject(sender_comp_id, target_comp_id, seq_num, orig_cl_ord_id, cl_ord_id):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_OrderCancelReject, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.OrderID("Order123"))
    msg.setField(fix.ClOrdID(cl_ord_id))
    msg.setField(fix.OrigClOrdID(orig_cl_ord_id))
    msg.setField(fix.OrdStatus(fix.OrdStatus_REJECTED))
    msg.setField(fix.CxlRejResponseTo(fix.CxlRejResponseTo_ORDER_CANCEL_REQUEST))
    msg.setField(fix.Text("Order cancel reject"))
    create_standard_trailer(msg)
    return msg

def create_order_status_request(sender_comp_id, target_comp_id, seq_num, cl_ord_id):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_OrderStatusRequest, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.ClOrdID(cl_ord_id))
    create_standard_trailer(msg)
    return msg

def create_execution_report(sender_comp_id, target_comp_id, seq_num, order_id, cl_ord_id, exec_id, exec_type, ord_status, symbol, side, leaves_qty, cum_qty, avg_px):
    msg = fix.Message()
    create_standard_header(msg, fix.MsgType_ExecutionReport, sender_comp_id, target_comp_id, seq_num)
    msg.setField(fix.OrderID(order_id))
    msg.setField(fix.ClOrdID(cl_ord_id))
    msg.setField(fix.ExecID(exec_id))
    msg.setField(fix.ExecType(exec_type))
    msg.setField(fix.OrdStatus(ord_status))
    msg.setField(fix.Symbol(symbol))
    msg.setField(fix.Side(side))
    msg.setField(fix.LeavesQty(leaves_qty))
    msg.setField(fix.CumQty(cum_qty))
    msg.setField(fix.AvgPx(avg_px))
    create_standard_trailer(msg)
    return msg