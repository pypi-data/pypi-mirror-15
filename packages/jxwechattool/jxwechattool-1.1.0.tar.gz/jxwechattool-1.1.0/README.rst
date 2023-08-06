jxwechattool
======

基于redis对wechat中access_token、qr_code、jsapi_ticket的cache

.. sourcecode:: bash
    
    $ pip install jxwechattool


Version update
------

- 0.1.0 添加WJSTicket
- 0.0.1 添加WAccessToken, WQRCode


Getting Started
------

.. sourcecode:: python
    #!/bin/python2
    # coding=utf-8

    import logging
    import WAccessToken, WQRCode, WJSTicket

    logging.basicConfig(level=logging.DEBUG)

    access_token_handler = WAccessToken(
        app_id=APP_ID,
        app_secret=APP_SECRET)

    logging.warn(("access_token", access_token_handler.get_access_token()))

    qr_handler = WQRCode(access_token_handler)

    logging.warn(("qr ur", qr_handler.get_qrcode_url_by_m("c-8")))
    logging.warn(("info ", qr_handler.get_qrcode_info_by_scene_id(80)))

    jsapi_ticket_handler = WJSTicket(access_token_handler)

    logging.warn(("jsapi_ticket", jsapi_ticket_handler.get_jsapi_ticket()))
