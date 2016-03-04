import os
import yaml
from datetime import datetime, date, tzinfo, timedelta
from google.appengine.ext import ndb
from google.appengine.ext import deferred
from lib import pesapal, BasePesapalPayment

with open('conf.yml', 'r') as f:
    conf = yaml.load(f)
    print conf
    pesapal.consumer_key = conf['PESAPAL_KEY']
    pesapal.consumer_secret = conf['PESAPAL_SECRET']
    pesapal.testing = True


class Payment(BasePesapalPayment):

    def check_status(self):

        super(Payment, self).check_status()

        status = self.get_status_string()

        if status == 'pending':
            pass
        elif status == 'completed':
            pass
        elif status == 'failed':
            pass
        elif status == 'invalid':
            pass
        elif status == 'refunded':
            pass
        elif status == 'overdue':
            pass
        else:
            raise