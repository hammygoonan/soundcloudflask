#!/usr/bin/python
'''Run updates for Soundcloud Flask Application'''

import sc

print 'starting feed update'
sc.update()
print 'starting favourites updates'
sc.update_favorites()
print 'end'