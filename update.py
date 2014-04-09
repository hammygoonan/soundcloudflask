#!/usr/bin/python
'''Run updates for Soundcloud Flask Application'''

import storage

storate_cl = storage.storage()

print 'starting feed update'
storate_cl.update()
print 'starting favourites updates'
storate_cl.update_favorites()
print 'end'