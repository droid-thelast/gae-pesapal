from datetime import datetime, date, tzinfo, timedelta
from google.appengine.ext import ndb
from google.appengine.ext import deferred


from lib import pesapal, BasePesapalPayment

PESAPAL_CLIENT = pesapal.PesaPal('--key--', '--secret--', True)


class Payment(BasePesapalPayment):

    def check_status(self, client):

        super(Payment, self).check_status(client)

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