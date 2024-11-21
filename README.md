# industrial-engineer
AI-driven Decision Support System to increase performance in Manufacturing Operations

## Run inventory simulation
To execute the GUI for the inventory simulation, first clone the repo:
```bash
git clone https://github.com/afr2903/industrial-engineer.git
cd industrial-engineer
```

A virtual environment was used for dependency isolation, to create it run:
```bash
python3 -m venv gui-env
source gui-env/bin/activate
```

Install the dependencies with:
```bash
pip install -r gui-requirements.txt
```

And finally execute the script:
```bash
python3 inventory_system_gui.py
```
