'''
Author: Roberto Pacheco
Date: August, 29, 2018
Modified: Roberto Pacheco
Last Modified: August, 29, 2018

Description:
Run the API REST
'''

from app import app, config

app.debug = config.DEBUG
#context = (config.SSL_CERTIFICATE, config.SSL_KEY)
#app.run(host='0.0.0.0', ssl_context=context)
app.run(host='0.0.0.0', port=config.PORT)