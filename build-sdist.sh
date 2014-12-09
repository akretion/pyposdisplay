sudo rm -rf dist
python setup.py sdist
cd dist
tar xvzf *.tar.gz
cd pyposdisplay*
sudo pip uninstall pyposdisplay
sudo python setup.py install
