sudo cd /tmp
sudo wget --quiet https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
sudo tar -xzf Python-3.10.12.tgz
cd Python-3.10.12
./configure --enable-optimizations --with-ssl-default-suites=openssl --prefix=/usr/local
make -j 2
sudo make altinstall
curl --silent https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3
echo "Python: $(python --version)" >>$HOME/chegou_ao_fim.txt
echo "Python 3.10 $(python3.10 --version)" >>$HOME/chegou_ao_fim.txt
python3.10 get-pip.py
echo \"fim do script de python\" >>$HOME/chegou_ao_fim.txt
