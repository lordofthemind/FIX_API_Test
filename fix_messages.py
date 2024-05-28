import quickfix as fix
import random
import time

symbols = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF"]

def current_time():
    return time.strftime("%Y%m%d-%H:%M:%S.%f")[:-3]

def create_heartbeat(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_Heartbeat))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(2))
    header.setField(fix.SendingTime(current_time()))
    return msg

def create_test_request(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_TestRequest))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(2))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.TestReqID("Test123"))
    return msg

def create_logon(sender_comp_id, target_comp_id, username, password):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_Logon))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(3))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.EncryptMethod(fix.EncryptMethod_NONE))
    msg.setField(fix.HeartBtInt(30))
    msg.setField(fix.ResetSeqNumFlag(True))
    msg.setField(fix.Username(username))
    msg.setField(fix.Password(password))
    return msg

def create_logout(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_Logout))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(4))
    header.setField(fix.SendingTime(current_time()))
    return msg

def create_resend_request(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_ResendRequest))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(5))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.BeginSeqNo(1))
    msg.setField(fix.EndSeqNo(1))
    return msg

def create_reject(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_Reject))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(6))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.RefSeqNum(1))
    msg.setField(fix.RefTagID(4))
    msg.setField(fix.RefMsgType("D"))
    return msg

def create_business_reject(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_BusinessMessageReject))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(7))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.RefSeqNum(1))
    msg.setField(fix.RefMsgType("D"))
    msg.setField(fix.BusinessRejectReason(fix.BusinessRejectReason_INSUFFICIENT_CREDIT))
    return msg

def create_sequence_reset(sender_comp_id, target_comp_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_SequenceReset))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(8))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.GapFillFlag(True))
    msg.setField(fix.NewSeqNo(1))
    return msg

def create_market_data_request(sender_comp_id, target_comp_id, md_req_id, depth_level):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_MarketDataRequest))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(9))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.MDReqID(md_req_id))
    msg.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))
    msg.setField(fix.MarketDepth(depth_level))
    msg.setField(fix.MDUpdateType(fix.MDUpdateType_FULL_REFRESH))
    msg.setField(fix.NoRelatedSym(1))
    symbol_group = fix.Group(146, 55)
    symbol_group.setField(fix.Symbol(random.choice(symbols)))
    msg.addGroup(symbol_group)
    return msg

def create_new_order_single(sender_comp_id, target_comp_id, cl_ord_id, order_qty, ord_type, price=None, time_in_force=None):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(10))
    header.setField(fix.SendingTime(current_time()))
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
    return msg

def create_order_status_request(sender_comp_id, target_comp_id, cl_ord_id):
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_OrderStatusRequest))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgSeqNum(21))
    header.setField(fix.SendingTime(current_time()))
    msg.setField(fix.ClOrdID(cl_ord_id))
    return msg

# Define other messages as needed...
