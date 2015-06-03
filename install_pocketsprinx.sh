#!/bin/sh

sudo wget http://iml.cpe.ku.ac.th/upload/pocket/gstreamer0.10-pocketsphinx_0.8.0+real-0ubuntu6_amd64.deb -O /run/shm/sphinx.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/pocketsphinx-utils_0.8.0+real-0ubuntu6_amd64.deb -O /run/shm/sphinx_1.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/pocketsphinx-lm-wsj_0.8.0+real-0ubuntu6_all.deb -O /run/shm/sphinx_2.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/pocketsphinx-hmm-wsj1_0.8.0+real-0ubuntu6_all.deb -O /run/shm/sphinx_3.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/libpocketsphinx1_0.8.0+real-0ubuntu6_amd64.deb -O /run/shm/sphinx_4.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/libsphinxbase1_0.8-0ubuntu10_amd64.deb -O /run/shm/sphinx_5.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/pocketsphinx-hmm-en-hub4wsj_0.8.0+real-0ubuntu6_all.deb -O /run/shm/sphinx_6.deb
sudo wget http://iml.cpe.ku.ac.th/upload/pocket/pocketsphinx-lm-en-hub4_0.8.0+real-0ubuntu6_all.deb -O /run/shm/sphinx_7.deb
sudo dpkg -i /run/shm/sphinx*.deb