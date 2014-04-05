#!/usr/bin/python
'''Run updates for Soundcloud Flask Application'''

import storage

print 'starting feed update'
storage.update()
print 'starting favourites updates'
storage.update_favorites()
print 'end'