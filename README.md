mailchimp-oauth-flask
======================

This app demonstrates basic OAuth connectivity with Mailchimp using flask.

Reference Documentation: [Mailchimp OAuth documentation](https://apidocs.mailchimp.com/oauth2/)

Requires:
---------

* Flask
* requests
* mailchimp

Instructions:
-------------

* Change the `REDIRECT_URI` in `mchimp.py` to the desired one
  according to your requirements. Make sure then you also make the
  corrsponding change in the route of `oauth_redirect` function.
* To run: `python mchimp.py`

LICENSE:
--------

MIT
