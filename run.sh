#!/bin/bash

echo -n '1n1e' > points.valid
echo -n > points.invalid

rm -f pictures.full/* pictures/* full.png

./crawl.py

cd pictures.full ; for i in *png ; do convert $i -resize 512x512 ../pictures/$i ; done ; cd ../

./concat.py

convert full.png -resize '40%' full_40percent.png