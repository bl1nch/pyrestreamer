# LibVLC based Restreamer with Python Flask Dashboard
![Снимок экрана 2023-06-01 001448](https://github.com/bl1nch/pyrestreamer/assets/130155870/66bffb31-f2b8-4fc2-9742-6cb2cdd154b8)

# Installation
1. Run setup.sh
```
. setup.sh
```
2. Attach tmux session
```
tmux attach -t pyrestreamer
```
3. Activate virtualenv
```
source .venv/bin/activate
```
4. Export flask app secret key
```
export SECRET_KEY="!secret"
```
5. Run app
```
python3 main.py
```
