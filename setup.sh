#!/usr/bin/env bash
# shellcheck disable=SC2046

activate() {
    . .venv/bin/activate
    pip install -r requirements.txt
    deactivate
}

mkdir logs
pysondb create db.json
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y vlc python3-virtualenv python3-pip tmux openssl
openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -out certificate.pem -keyout key.pem
virtualenv .venv
tmux new -d -s pyrestreamer
activate
