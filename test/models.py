from datetime import datetime, date, tzinfo, timedelta
from google.appengine.ext import ndb
from google.appengine.ext import deferred

from lib import pesapal, BasePesapalPayment


pesapal.consumer_key = 'H7jjIYLsuYGWZEJnuO8mIEMMPa4K15O6'
pesapal.consumer_secret = 'C0hFRtwKY+rKfol3usK8ejhgL+s='
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