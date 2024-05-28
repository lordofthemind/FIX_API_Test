import quickfix as fix

def create_heartbeat():
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_Heartbeat))
    header.setField(fix.SenderCompID("SENDER_COMP_ID"))
    header.setField(fix.TargetCompID("TARGET_COMP_ID"))
    header.setField(fix.MsgSeqNum(2))
    header.setField(fix.SendingTime("20240527-15:20:01.123"))
    return msg

def create_test_request():
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_TestRequest))
    header.setField(fix.SenderCompID("ClientCentroid"))
    header.setField(fix.TargetCompID("Broker"))
    header.setField(fix.MsgSeqNum(2))
    header.setField(fix.SendingTime("20240527-10:00:00.000"))
    msg.setField(fix.TestReqID("Test123"))
    return msg

# Define other messages similarly...

def create_market_order():
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.BeginString("FIX.4.4"))
    header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    header.setField(fix.SenderCompID("SENDER_COMP_ID"))
    header.setField(fix.TargetCompID("TARGET_COMP_ID"))
    header.setField(fix.MsgSeqNum(16))
    header.setField(fix.SendingTime("20240527-15:20:01.123"))
    msg.setField(fix.ClOrdID("OrderID1"))
    msg.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
    msg.setField(fix.Symbol("EUR/USD"))
    msg.setField(fix.Side(fix.Side_BUY))
    msg.setField(fix.TransactTime("20240527-15:20:01.123"))
    msg.setField(fix.OrderQty(1000))
    msg.setField(fix.OrdType(fix.OrdType_MARKET))
    msg.setField(fix.TimeInForce(fix.TimeInForce_DAY))
    return msg

# Add more functions for each message type...
