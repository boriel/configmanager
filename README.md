## Simple Config Manager

Simple Config Manager is a very simple Python pure in-app config manager.
It will centralize all your app settings in a unique class which will hold a key-value
setting.

## Features

 * Allow namespace-like definitions
 * Keys can be set and accessed as attributes or dictionary key values
 * Allows strict type-checking of values

## Usage

Let's suppose we want to store settings for our project. We decided to store those settings in 3 areas
, namely `main`, `backend`, `frontend`, 

A simple pattern usage could be:

```python
config = ConfigManager()

# create namespaces
config('main')
config('frontend')
config('backend')
```

Now we can operate with `main`, `backend`, `frontend` as if they were attributes:
```python
# Sets parameters for main area
config.main.config_file = 'config.json'  #  config file
config.main.global_log_file = '/var/log/my_app.log'  #  a log file

# Sets parameters for frontend area
config.frontend.index_file = 'index.html'

# Sets parameters for backend area
config.backend.main_file = 'main.py'
```

We can read or update those values as normal properties:
```python
print('Config file is', config.main.config_file)
config.main.config_file = new_config_file  # Update property
```

#### Defining nested namespaces
It's pretty straightforward. You can do it either with:
```python
config('main.subsection')
```
or with
```python
config('main')('subsection')
```

#### Accessing properties as dict keys
All the above is true also for dict-like accesses. Just replace parenthesis with
square brackets:
```
config['main.subsection.value'] = 1
```
or 
```
config['main']['subsection']['value'] = 1
```
which is equivalent. 

You can even mix modes!
```
config['main.subsection'].value = 1
print(config['main.subsection.value'])  # 1
```


## To do

* Allow defining read only properties
