url = 'https://fastprintid.odoo.com',
db = 'fastprintid-sandyhartono-master-1221888',
username = 'prog4.fastprintsby@gmail.com',
password = 'odoo13'

import xmlrpc.client

# Authenticate
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Call the method
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
result = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
print(result)