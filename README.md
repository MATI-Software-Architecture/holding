# holding

Install Python greater than 3.6 and mongodb

from the following links

- https://www.python.org/downloads/
- https://www.mongodb.com/docs/manual/installation/

1. Create Virtual Env

```bash
python -m venv venv
```

2. Activate Virtual Env

Windows
```bash
venv/Scripts/activate
```

Linux
```bash
source venv/bin/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

4. Run the app 

on development mode
```bash
flask --debug run
```
