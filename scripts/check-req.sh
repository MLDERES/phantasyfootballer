#!/bin/bash

current_req=current_req.txt
installed_req=installed_req.txt
$( pip freeze | awk 'BEGIN {FS="=";} {print $1}'> $installed_req)
$(grep -v "^#" ../src/requirements.txt | awk 'BEGIN {FS="=";} {print $1;}' 1> $current_req)
$(grep -v -f $current_req $installed_req)
rm -f (current_req
rm -f $installed_req
echo 'done'