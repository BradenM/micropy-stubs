from m5stack import btn

def Button(port):
    btnClass =  btn.attach(port[1])
    return btnClass