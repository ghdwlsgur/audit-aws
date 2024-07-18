### 1. Copy code & Paste lambda

### 2. Create layer

```bash
# create workspace to exec python script in local
$ python3.11 -m venv .
$ source ./bin/activate
$ python3.11 -m pip install requests

# create requirements.txt file
$ pip3 freeze > requirements.txt
# or
$ pip3 install -r requirements.txt

# create lambda layer
$ cp -r ./lib python/
$ zip -r layer_requests.zip python
```

### How to execute

```bash
$ py ./test_lambda_function.py
```
