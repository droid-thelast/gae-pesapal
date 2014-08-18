GAE Pesapal
---

This library is meant to automatically kick-off payment status checks once a payment is made.

Install
---

    $ pip install gae-pesapal

Use
---

```python

import os
from datetime import datetime, date, tzinfo, timedelta

from google.appengine.dist import use_library
use_library('django', '1.2')
os.environ['DJANGO_SETTINGS_MODULE'] = '__init__'

import webapp2 as webapp
from webapp2_extras import sessions
from google.appengine.ext import ndb
from google.appengine.ext import deferred
from google.appengine.ext.webapp import template

from gae_pesapal import pesapal
from gae_pesapal.models import BasePesapalPayment

sessions.default_config['secret_key'] = '-- secret key --'
pesapal.consumer_key = '-- --'
pesapal.consumer_secret = '-- --'
pesapal.testing = False


class Payment(BasePesapalPayment):

    MAX_STATUS_CHECKS = 5 # fails payment after 5 retries

    DEFER_STATUS_CHECK_BY_MINUTES = 30 # checks payment status every half hour

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


class PayView(webapp.RequestHandler):

    """ View that allows users to pay via pesapal. """

    def dispatch(self):

        self.session_store = sessions.get_store(
            request=self.request
        )

        try:
            webapp.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):

        transaction_tracking_id = self.request.get(
            'pesapal_transaction_tracking_id'
        )
        merchant_reference = self.request.get(
            'pesapal_merchant_reference'
        )

        if transaction_tracking_id and merchant_reference:

            # store payment details in a model

            ref = self.session.get('pesapal_ref')
            amount = int(self.session.get('pesapal_amount'))

            payment = Payment(
                ref=ref,
                amount=amount,
                transaction_tracking_id=transaction_tracking_id,
                merchant_reference=merchant_reference
            )
            payment.put()

            payment.check_status()

            del self.session['pesapal_ref']
            del self.session['pesapal_amount']
            
            template_values = {
            }

        else:

            # build payment url and render it to user in an iframe

            amount = '200000'
            desc = 'Xbox purchase'
            ref = Payment.get_ref()
            email = 'me@example.com'

            self.session['pesapal_ref'] = ref
            self.session['pesapal_amount'] = amount

            request_data = {
              'Amount': amount,
              'Description': desc,
              'Reference': ref,
              'Email': email
            }

            oauth_callback = 'http://%s/' % (
                self.request.headers['host'],
            )

            post_params = {
              'oauth_callback': oauth_callback
            }

            src = pesapal.postDirectOrder(
                post_params,
                request_data
            )

            template_values = {
                'src': src,
            }

        path = os.path.join(
                os.path.dirname(__file__), 'template.html'
            )
        self.response.out.write(template.render(path, template_values))


urls = [
    ('/', PayView),
]

app = webapp.WSGIApplication(urls, debug=True)

```

Example
---

    $ make deps example

Test
---

    $ make deps test