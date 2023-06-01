#!/usr/bin/env bash
# shellcheck disable=SC2046

activate(){
    . ./.venv/bin/activate
    pip3 install -y -r requirements.txt
}

sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y vlc python3-pip tmux openssl
openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -out certificate.pem -keyout privatekey.pem \
    -subj "/C=$PYRESTREAMER_OPENSSL_C/ST=$PYRESTREAMER_OPENSSL_ST/L=$PYRESTREAMER_OPENSSL_L/O=$PYRESTREAMER_OPENSSL_O/OU=$PYRESTREAMER_OPENSSL_OU/CN=$PYRESTREAMER_OPENSSL_CN"
python3 -m venv .venv
tmux new -d -s pyrestreamer
activate