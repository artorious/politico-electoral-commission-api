[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Build Status](https://travis-ci.org/artorious/politico-electoral-commission-api.svg?branch=ft-create-party-163682027)](https://travis-ci.org/artorious/politico-electoral-commission-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/cf4f856dfec0ad0004aa/maintainability)](https://codeclimate.com/github/artorious/politico-electoral-commission-api/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/artorious/speedy_chakula_app/badge.svg?branch=develop)](https://coveralls.io/github/artorious/speedy_chakula_app?branch=develop)

# politico-electoral-commission-api
A web application platform which both the politicians and citizens can use. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## Endpoints - Features

**Endpoint** | **Request**| **Description**
--- | --- | ---
`/api/v2/parties` | `POST` | Create a political party
`/api/v2/parties` | `GET`| Fetch all political parties
`/api/v2/parties/<int:id>` | `GET` |   Fetch a specific political party
`/api/v2/parties/<int:id>` | `DELETE` |   Delete a specific political party
`/api/v2/<int:id>/name` | `PATCH` | Edit a political party
`/app/api/v1/offices` | `POST`| Create Political office
`/api/v2/offices` | `GET` | Fetch all political offices
`/api/v2/offices/<int:id>` | `GET` | Fetch a specific offices
`/api/v2/auth/signup`|`POST`| User signup
`/api/v2/auth/login`|`POST`| User Login with Auth
`/api/v2/office/<int:id/register`|`POST`| Candidate registration
`/api/v2/office/open` | `GET` | List all open positions
`/api/v2/votes/` | `POST` | vote for a candidate
`/api/v2/office/<int:id>/result` | `GET` | Collate and display resuls
`/api/v2/petitions` | `POST` | Make a petition to challenge election results
`/api/v2/auth/reset`| `POST` | Make a request for a password change

## Usage
* Read and interact with the [API Documentation](https://documenter.getpostman.com/view/3796196/RztspSTt)
### Testing
* On Postaman App:
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/016419570361ff8cce12)

On a  terminal (Linux):
* Install and set up git, python3 and a virtual environment

* In a virtual environment;
  * Clone the repository `git clone https://github.com/artorious/politico-electoral-commission-api.git`

  * Run `git checkout develop`
  * Run `cd politico-electoral-commission-api`
  * Run `pip3 install -r requirements.txt` to install dependancies
  * Run `python3 run.py` to interact with the app.
