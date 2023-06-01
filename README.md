# LibVLC based Restreamer with Python Flask Dashboard
![Снимок экрана 2023-06-01 001448](https://github.com/bl1nch/pyrestreamer/assets/130155870/66bffb31-f2b8-4fc2-9742-6cb2cdd154b8)

# Installation
1. Export openssl env variables
```
export PYRESTREAMER_OPENSSL_C="EN"
export PYRESTREAMER_OPENSSL_ST="State"
export PYRESTREAMER_OPENSSL_L="City"
export PYRESTREAMER_OPENSSL_O="Company"
export PYRESTREAMER_OPENSSL_OU="Department"
export PYRESTREAMER_OPENSSL_CN="site.com"
```
2. Run setup.sh
```
chmod +X setup.sh
. setup.sh
```
3. Attach tmux session and activate virtualenv
```
tmux ls
tmux attach -t pyrestreamer
source .venv/bin/activate
```
4. Export flask app secret key
```
export SECRET_KEY="SOME SECRET KEY"
```
5. Run app
```
python3 main.py
```
