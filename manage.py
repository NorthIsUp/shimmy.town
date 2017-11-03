# -*- coding: utf-8 -*-
#!/usr/bin/env bash
''''echo "bash proxy to shimmytown/manage.py" 1>&2

cd shimmytown
exec ./manage.py $@
exit # just in case
'''

import os, sys
print('python proxy')

os.system('./manage.py ' + ' '.join(sys.argv[1:]))
