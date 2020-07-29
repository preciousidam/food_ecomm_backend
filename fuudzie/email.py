from flask import render_template, current_app
from flask_mail import Message
from threading import Thread

from fuudzie.instances import mail


class NewOrderUserMail():

    def __init__(self, email, name, items, subtotal, delvfee):
        self.name = name
        self.items = items
        self.subtotal = subtotal
        self.delvfee = delvfee
        self.email = email
        self.template = 'new-order-user.html'

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            subject="New Order on Fuudzie.com", 
            recipients=[self.email], 
            html= self.get_template()
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

    def get_template(self):
        return render_template(self.template, fullName=self.name, items=self.items, subtotal=self.subtotal, delvfee=self.delvfee)
        
    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)







class NewOrderVendorMail():

    def __init__(self, email, name, items, total, instruction):
        self.name = name
        self.items = items
        self.total = total
        self.email = email
        self.instruction = instruction
        self.template = 'new-order-vendor.html'

    def create_mail(self):
        app = current_app._get_current_object()
        
        msg = Message(
            subject="New Order on Fuudzie.com", 
            recipients=[self.email], 
            html= self.get_template()
        )
        thr = Thread(target=self.send_mail, args=[app,msg])
        thr.start()

    def get_template(self):
        
        return render_template(self.template, businessName=self.name, items=self.items, total=self.total, instruction=self.instruction)

    def send_mail(self, app, msg):
        with app.app_context():
            mail.send(msg)