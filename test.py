import quickfix as fix
from datetime import datetime
from symbols import SYMBOLS



# Create a new order single message
new_order_msg = create_new_order_single(sender_comp_id, target_comp_id, seq_num, cl_ord_id, order_qty, ord_type, price, time_in_force)

# Send the message
fix.Session.sendToTarget(new_order_msg)


# Sample function to handle incoming execution report messages
def on_execution_report(msg):
    exec_type = fix.ExecType()
    msg.getField(exec_type)

    if exec_type.getValue() == fix.ExecType_NEW:
        # Process new order execution report
        pass
    elif exec_type.getValue() == fix.ExecType_REJECTED:
        # Process rejected order execution report
        pass
    # Add more conditions as per your requirements
