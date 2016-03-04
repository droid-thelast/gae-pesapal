import os

from google.appengine.dist import use_library
use_library('django', '1.2')
os.environ['DJANGO_SETTINGS_MODULE'] = '__init__'

import webapp2 as webapp
from webapp2_extras import sessions
from google.appengine.ext.webapp import template

from lib import pesapal
from models import *


sessions.default_config['secret_key'] = '-- secret key --'


class PayView(webapp.RequestHandler):


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
                'payment_sucessfull': True
            }

        else:

            amount = '2000'
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
                'amount': amount,
            }

        path = os.path.join(
                os.path.dirname(__file__), 'template.html'
            )
        self.response.out.write(template.render(path, template_values))

# template.html
#
# <style>
#     body{
#       font-size: 15px;
#       padding: 50px;
#     }
#     iframe{
#       width: 100%;
#       height: 550px;
#       border: 0px none;
#     }
#   </style>
# 
# <iframe src="{{src}}" scrolling="yes"></iframe>

urls = [
    ('/', PayView),
]

app = webapp.WSGIApplication(urls, debug=True)
