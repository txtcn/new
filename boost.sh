
#!/usr/bin/env bash
_DIR=$(cd "$(dirname "$0")"; pwd)
cd $_DIR



python_version=3.7

set -e

cd /usr/src

wget -c --no-verbose https://dl.bintray.com/boostorg/release/1.73.0/source/boost_1_73_0.tar.gz
tar xzf boost_1_73_0.tar.gz
cd boost_1_73_0

ln -s /root/.asdf/installs/python/3.7.8/include/python3.7m $_DIR/.venv/include/python3.7

./bootstrap.sh --with-python=`which python`
./b2 install
ldconfig
cd / && rm -rf /usr/src/*
