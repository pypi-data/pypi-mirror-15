# Logs-analyzer

Logs-analyzer is a library containing functions that can help you extract usable data from logs.

## How to install
using pip : `pip install logs-analyzer`

## Settings

Contains the default settings for the supported logs.

### NGINX Settings
```python
DEFAULT_NGINX = {
    'dir_path': '/var/log/nginx/',
    'accesslog_filename': 'access.log',
    'errorlog_filename': 'error.log',
    'dateminutes_format': '[%d/%b/%Y:%H:%M',
    'datehours_format': '[%d/%b/%Y:%H',
    'datedays_format': '[%d/%b/%Y',
    'request_model': (r''
                      '(\d+.\d+.\d+.\d+)\s-\s-\s'
                      '\[(.+)\]\s'
                      '(?i)"?(GET|POST|PUT|HEAD|DELETE|OPTIONS|CONNECT|PATCH)\s(.+)\s\w+/.+"'
                      '\s(\d+)\s'
                      '\d+\s"(.+)"\s'
                      '"(.+)"'),
    'date_pattern': (r''
                     '(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+)'),
    'date_keys': {'day': 0, 'month': 1, 'year': 2, 'hour': 3, 'minute': 4, 'second': 5}
}
```

### Apache2 Settings
```python
DEFAULT_APACHE2 = {
    'dir_path': '/var/log/apache2/',
    'accesslog_filename': 'access.log',
    'errorlog_filename': 'error.log',
    'dateminutes_format': '[%d/%b/%Y:%H:%M',
    'datehours_format': '[%d/%b/%Y:%H',
    'datedays_format': '[%d/%b/%Y',
    'request_model': (r''
                      '(\d+.\d+.\d+.\d+)\s-\s-\s'
                      '\[(.+)\]\s'
                      '(?i)"?(\w+)\s(.+)\s\w+/.+"'
                      '\s(\d+)\s'
                      '\d+\s"(.+)"\s'
                      '"(.+)"'),
    'date_pattern': (r''
                     '(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+)'),
    'date_keys': {'day': 0, 'month': 1, 'year': 2, 'hour': 3, 'minute': 4, 'second': 5}
}
```
### Auth Settings
```python
DEFAULT_AUTH = {
    'dir_path': '/var/log/',
    'accesslog_filename': 'auth.log',
    'dateminutes_format': '%b %e %H:%M:',
    'datehours_format': '%b %e %H:',
    'datedays_format': '%b %e ',
    'request_model': (r''
                      '(\w+\s\s\d+\s\d+:\d+:\d+)\s'
                      '\w+\s(\w+)\[\d+\]:\s'
                      '(.+)'),
    'date_pattern': (r''
                     '(\w+)\s(\s\d+|\d+)\s(\d+):(\d+):(\d+)'),
    'date_keys': {'month': 0, 'day': 1, 'hour': 2, 'minute': 3, 'second': 4}
}
```

## Main functions

### Function get_service_settings
Get default settings for the said service from the settings file, three type
of logs are supported right now: `nginx`, `apache2` and `auth`.
#### Parameters
**service_name:** service name  (e.g. nginx, apache2...).
#### Return
Returns a dictionary containing the chosen service settings or `None` if the
service doesn't exists.
#### Sample
`nginx_settings = get_service_settings('nginx')`

### Function get_date_filter
Get the date pattern that can be used to filter data from
logs based on the parameters.
#### Parameters
**settings:** the target logs settings.

**minute:** default now, minutes or * to ignore.

**hour:** default now, hours or * to ignore.

**day:** default now, day of month.

**month:** default now, month number.

**year:** default now, year.
#### Return
Returns date pattern (String).
#### Sample
```python
nginx_settings = get_service_settings('nginx')
date_pattern = get_date_filter(nginx_settings, 13, 13, 16, 1, 1989)
print(date_pattern)
```
Prints `[16/Jan/1989:13:13`

### Function filter_data
Filter received data/file content and return the results.
#### Parameters
**log_filter:** string that will be used to filter data

**data:** data to be filtered (String) or None if the data will
be loaded from a file.

**filepath:** filepath from where data will be loaded or None if
the data has been passed as a parameter.

**is_casesensitive:** if the filter has to be case sensitive
(default True).

**is_regex:** if the filter string is a regular expression
(default False).
#### Return
Returns filtered data (String).
#### Sample
```python
nginx_settings = get_service_settings('nginx')
date_filter = get_date_filter(nginx_settings, '*', '*', 27, 4, 2016)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(base_dir, 'logs-samples/nginx1.sample')
data = filter_data('192.168.5', filepath=file_name)
data = filter_data(date_filter, data=data)
```

### Function get_web_requests
Analyze the web logs (Nginx & Apache2 for now) data and return list of requests
formatted as the model (pattern) defined.
#### Parameters
**data:** (String) data to analyzed.

**pattern:** (Regular expression) used to extract requests.

**date_pattern:** (Regular expression or None) used to extract date elements
to have ISO formatted dates.

**date_keys:** (List or None) list of extracted date elements placements.
#### Return
Returns a List of requests as dictionaries.
#### Sample
```python
apache2_settings = get_service_settings('apache2')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(base_dir, 'logs-samples/apache1.sample')
data = filter_data('127.0.1.1', filepath=file_name)
requests = get_web_requests(data, apache2_settings['request_model'],
                            nginx_settings['date_pattern'], nginx_settings['date_keys'])
```

### Function get_auth_requests
Analyze the Auth logs data and return list of requests
formatted as the model (pattern) defined.
#### Parameters
**data:** (String) data to analyzed.

**pattern:** (Regular expression) used to extract requests.

**date_pattern:** (Regular expression or None) used to extract date elements
to have ISO formatted dates.

**date_keys:** (List or None) list of extracted date elements placements.
#### Return
Returns a List of requests as dictionaries.
#### Sample
```python
auth_settings = get_service_settings('auth')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
date_filter = get_date_filter(auth_settings, '*', 22, 4, 5)
file_name = os.path.join(base_dir, 'logs-samples/auth.sample')
data = filter_data('120.25.229.167', filepath=file_name)
data = filter_data(date_filter, data=data)
requests = get_auth_requests(data, auth_settings['request_model'],
                                     auth_settings['date_pattern'], auth_settings['date_keys'])
```