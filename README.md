# CDN Guesser

![CDN](https://github.com/rihib/cdn-guesser/assets/76939037/0c547ce2-b650-4360-966d-d88b9b5efe35)

Enter the URL of the site and it will guess what CDN the site is using.
Partially uses data from [Wappalyzer](https://github.com/wappalyzer/wappalyzer).

You can use it locally as follows, and it has been tested with Python 3.11. If you are using older Python, the package may fail to install.
Operation is quite slow, please be patient until the name of the CDN comes up.

```python3
git clone https://github.com/rihib/cdn-detector.git
cd cdn-detector
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 src/main.py
```
