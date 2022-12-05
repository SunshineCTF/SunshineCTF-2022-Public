#!/bin/bash

export CF_Token=CHANGEME

~/.acme.sh/acme.sh --issue \
    -d sun-look-there-its-in-the-logs-endflag.sunshinectf.org \
    --dns dns_cf
