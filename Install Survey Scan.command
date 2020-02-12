#!/bin/sh

# install_surveyscan.py
for i in {1...5}
do
    echo
done

echo Installing Survey Scan...
for i in {1...5}
do
    echo
done

echo Installing Kivy Package...
pip install kivy
for i in {1...5}
do
    echo
done
echo Installing Pandas Package...
pip install kivy
for i in {1...5}
do
    echo
done
echo Installing Textblob Package...
pip install -U textblob
python -m textblob.download_corpora
echo Installation Successful.
