#!/usr/bin/python
'''Run updates for Soundcloud Flask Application'''

import storage

storage_client = storage.storage()

print 'starting feed update'
storage_client.update()
print 'starting favourites updates'
storage_client.update_favorites()
print 'end'