#!/bin/sh

# install_surveyscan.py
echo 
echo Updating Pip
python -m pip install –upgrade pip
echo 
echo Installing Survey Scan...
echo 
echo Installing Kivy Package...
pip install kivy
pip3 install kivy
echo 
echo Installing Pandas Package...
pip install pandas
pip3 install pandas
echo 
echo Installing Textblob Package...
pip install -U textblob
pip3 install -U textblob
python -m textblob.download_corpora
echo Installing Matplotlib and Kivy Garden...
pip install kivy-garden
pip3 install kivy-garden
python -m pip install matplotlib
python3 -m pip3 install matplotlib
garden install matplotlib
echo Installing Numpy...
pip install numpy
echo Installing Scipy...
pip install scipy

echo Installation Successful.
cd Survey\ Scan\ \(Main\ App\)/
python app_main.py
