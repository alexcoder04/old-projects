def print_msg(msg, thread):
    if type(msg) == "string":
        msg = "[" + thread + "]: " + msg
    else:
        msg = "[" + thread + "]: " + str(msg)
    print(msg)
