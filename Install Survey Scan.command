#!/bin/sh

# install_surveyscan.py
echo 
echo Installing Survey Scan...
echo 
echo Installing Kivy Package...
pip install kivy
echo 
echo Installing Pandas Package...
pip install kivy
echo 
echo Installing Textblob Package...
pip install -U textblob
python -m textblob.download_corpora
echo Installation Successful.
