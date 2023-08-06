Client API
===========

# Installation

- Go to the source

```
cd pyquay
python setup.py sdist
pip install dist/pyquay-<VERSION>.tar.gz
```

# Usage

Do the following to instantiate a Client class that will allow you to communicate with a Quay API:

```
from pyquay import Client
c = Client(token)
```

Params:
- token (str): Refers to the token used in the Authorization header

## security
This grabs a json blob of all vulnerabilities associated with an image.

```
tenants = c.security(repo, imageid)
```

# CLI
quaycli.py security get_vulnerability_list --token=token --repo=repo --image=image id
