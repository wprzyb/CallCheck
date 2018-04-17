#!/bin/bash
mv osec_pzk.txt OLD_osec_pzk.txt
mv osec_kluby.txt OLD_osec_kluby.txt
wget -nd http://pzk.org.pl/osec_pzk.txt
wget -nd http://pzk.org.pl/osec_kluby.txt
rm OLD_osec_pzk.txt
rm OLD_osec_kluby.txt
