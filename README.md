# ushiriki-policy-engine-reward-service
Example of a reward webservice exposing the Ushiriki Policy Engine to the API

Using the blueprints to structure the existence of optional environments.

## Dependencies
This code has been tested with Python3, although if previous versions are required, the code content should suffice. It is written in a modular manner so environments can be added at any time. When they are added, the yaml file must be revised to point to the module path of the new objects.

## Installation
Ensure that all the required modules are included into the base version of requirements.txt

(To get all the dependencies you might have to check in your subdirectories
```cat */requirements >> requirements.txt```)

```pip install -r requirements.txt```

## Execution
Selecting the appropriate configuration file defining the environment you'd like to host..

```PORT=8080 python webservice.py config.yaml```

## Citation
[Environment Reward Service]
```lisp
@misc{pending,
  Author = {Sekou L Remy and Oliver E Bent},
  Title = {A Global Health Gym Environment for RL Applications},
  Year = {2020},
  Eprint = {arXiv:pending},
}
```
