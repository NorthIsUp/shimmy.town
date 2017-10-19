# -*- coding: utf-8 -*-
#!/usr/bin/env bash

echo "proxying to shimmytown/manage.py" 1>&2

cd shimmytown
./manage.py $@
