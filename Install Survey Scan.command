#!/bin/sh

# install_surveyscan.py
echo 
echo Updating Pip
pip install –-upgrade pip
pip3 install --upgrade pip3
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
python3 -m textblob.download_corpora
echo Installing Matplotlib and Kivy Garden...
pip install kivy-garden
pip3 install kivy-garden
python -m pip install matplotlib
python3 -m pip3 install matplotlib
garden install matplotlib
python -m pip install matplotlib
python3 -m pip3 install matplotlib
python3 -m pip install matplotlib
echo Installing Numpy...
pip install numpy
echo Installing Scipy...
pip install scipy
echo Reinstalling Everything to be safe...
cd "$(dirname "$BASH_SOURCE")" || {
    echo "Error getting script directory" >&2
    exit 1
}
pip install -r requirements.txt
pip3 install -r requirements.txt
echo Installation Successful. Opening Application...
cd Survey\ Scan\ \(Main\ App\)/
python app_main.py
echo Opening Window in Python 3....
python3 app_main.py
