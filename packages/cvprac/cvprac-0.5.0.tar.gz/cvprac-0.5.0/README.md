# Arista Cloudvision&reg; Portal RESTful API Client

#### Table of Contents

1. [Overview] (#overview)
    * [Requirements] (#requirements)
2. [Installation] (#installation)
    * [Development: Run from Source] (#development-run-from-source)
3. [Getting Started] (#getting-started)
    * [Example] (#example)
4. [Testing] (#testing)
5. [License] (#license)

# Overview
This module provides a RESTful API client for Cloudvision&reg; Portal (CVP)
which can be used for building applications that work with Arista CVP.

When the class is instantiated the logging is configured.  Either syslog,
file logging, both, or none can be enabled.  If neither syslog nor filename is
specified then no logging will be performed.

This class supports creating a connection to a CVP node and then issuing
subsequent GET and POST requests to CVP.  A GET or POST request will be
automatically retried on the same node if the request receives a
requests.exceptions.Timeout error.  A GET or POST request will be automatically
retried on the same node if the request receives a CvpSessionLogOutError.  For
this case a login will be performed before the request is retried.  For either
case, the maximum number of times a request will be retried on the same node
is specified by the class attribute NUM_RETRY_REQUESTS.

If more than one CVP node is specified when creating a connection, and a GET
or POST request that receives a requests.exceptions.ConnectionError,
requests.exceptions.HTTPError, or a requests.exceptions.TooManyRedirects will
be retried on the next CVP node in the list.  If a GET or POST request that
receives a requests.exceptions.Timeout or CvpSessionLogOutError and the retries
on the same node exceed NUM_RETRY_REQUESTS, then the request will be retried
on the next node on the list.

If any of the errors persists across all nodes then the GET or POST request
will fail and the last error that occurred will be raised.

The class provides connect, get, and post methods that allow the user to make
RESTful API calls to CVP.  The class does not provide any wrapper functions
around the specific RESTful API operations (ex: /cvpInfo/getCvpInfo.do,
/aaa/saveAAADetails.do, ...).  To do so would require creating methods that
take the appropriate dictionary as method parameters for the operation or
flatten out the dictionary and pass them as parameters to the operation method.
Either approach adds no value.  The value provided by this class is in
automatically handling the CVP session logout and retrying requests across all
CVP nodes in the face of failures.

## Requirements

* Python 2.7 or later
* Python logging module
* Python requests module version 1.0.0 or later

# Installation

The source code for cvprac is provided on Github at
https://github.com/aristanetworks/cvprac.  All current development is done in
the develop branch.  Stable released versions are tagged in the master branch
and uploaded to https://pypi.python.org.

If your platform has internet access you can use the Python Package manager to
install cvprac.

```
admin:~ admin$ sudo pip install cvprac
```

You can upgrade cvprac 

```
admin:~ admin$ sudo pip install --upgrade cvprac
```

## Development: Run from Source

We recommend running cvprac in a virtual environment. For more information,
read this: http://docs.python-guide.org/en/latest/dev/virtualenvs/

These instructions will help you install and run cvprac from source. This is
useful if you plan on contributing or if you would always like to see the latest
code in the develop branch. Note that these steps require the pip and git
commands.

### Step 1: Clone the cvprac Github repo

```
# Go to a directory where you'd like to keep the source
admin:~ admin$ cd ~/projects
admin:~ admin$ git clone https://github.com/aristanetworks/cvprac
admin:~ admin$ cd cvprac
```

### Step 2: Check out the desired version or branch

```
# Go to a directory where you'd like to keep the source
admin:~ admin$ cd ~/projects/cvprac

# To see a list of available versions or branches
admin:~ admin$ git tag
admin:~ admin$ git branch

# Checkout the desired version of code
admin:~ admin$ git checkout v0.3.3
```

### Step 3: Install cvprac using Pip with -e switch

```
# Go to a directory where you'd like to keep the source
admin:~ admin$ cd ~/projects/cvprac

# Install
admin:~ admin$ sudo pip install -e ~/projects/cvprac
```

### Step 4: Install cvprac development requirements

```
# Go to a directory where you'd like to keep the source
admin:~ admin$ pip install -r dev-requirements.txt
```

# Getting Started

Once the package has been installed you can run the following example to verify that everything has been installed properly.

## Example

Example:

```
>>> from cvprac.cvp_client import CvpClient
>>> clnt = CvpClient()
>>> clnt.connect(['cvp1', 'cvp2', 'cvp3'], 'cvp_user', 'cvp_word')
>>> result = clnt.get('/cvpInfo/getCvpInfo.do')
>>> print result
{u'version': u'2016.1.0'}
>>>
```

# Testing

The cvprac module provides system tests. To run the system tests, you will need
to update the ``cvp_nodes.yaml`` file found in test/fixtures. At least one
running CVP node needs to be specified.

* To run the system tests, run ``make tests`` from the root of the cvprac
  source folder.

# Contributing

Contributing pull requests are gladly welcomed for this repository.  Please
note that all contributions that modify the library behavior require
corresponding test cases otherwise the pull request will be rejected.  

# License

Copyright (c) 2016, Arista Networks, Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of Arista Networks nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
