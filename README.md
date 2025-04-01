# Cookie Clicker Bot

Simple automation script for the ITA Júnior data bootcamp (week 3).

External libraries used:
- Selenium
- BeautifulSoup4

Run locally! `zsh`
```zsh

gh repo clone thalestmm/ccbot
cd ccbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The default duration is set to 5 minutes (300 seconds), but you can change it in the `config.yaml` file.

The final result will be displayed in the `stdout` as an INFO log.

Highest recorded score: **53,042**.
