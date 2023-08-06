<p align="center"><img src="https://cloud.githubusercontent.com/assets/564725/13137893/1b8eced2-d624-11e5-9264-3416ff821657.png" width="280" alt="SwiftyBeaver"><br/><b>Colorful</b>, extensible, <b>lightweight</b> logging for Swift 2 & 3 as well as Python 2 & 3.<br/>Great for <b>servers</b> with support for cloud platforms.
<br><br>
<a href="https://github.com/SwiftyBeaver/SwiftyBeaver">Swift Version</a> |
<a href="http://docs.swiftybeaver.com">Docs</a> |
<a href="https://swiftybeaver.com">Website</a> |
<a href="https://slack.swiftybeaver.com">Slack</a> |
<a href="https://twitter.com/SwiftyBeaver">Twitter</a> |
<a href="https://github.com/SwiftyBeaver/SwiftyBeaver/blob/master/LICENSE">License</a>
<br/>
</p>

<p align="center">
[![Language Swift 2](https://img.shields.io/badge/Language-Python%202%20&%203-orange.svg)](https://www.python.org) [![Slack Status](https://slack.swiftybeaver.com/badge.svg)](https://slack.swiftybeaver.com)
<p>
----

Conveniently log to the SwiftyBeaver Platform using the built-in Python logging library.

## Installation

Simply install SwiftyBeaver using `pip`:

```sh
$ pip install swiftybeaver
```

Or use `setup.py` after downloading it manually:

```sh
$ python setup.py install
```

## Usage

SwiftyBeaver can be used just as any other Python logging handler:

```python
import logging
from swiftybeaver import SwiftyBeaverHandler

sb_handler = SwiftyBeaverHandler('hThdK', 'sdfa...s3mx', 'dsgb...ghdX')
log = logging.Logger(__name__)
log.addHandler(sb_handler)

log.verbose("not so important")  // prio 1, VERBOSE in silver
log.debug("something to debug")  // prio 2, DEBUG in green
log.info("a nice information")   // prio 3, INFO in blue
log.warning("oh no, that won’t be good")  // prio 4, WARNING in yellow
log.error("ouch, an error did occur!")  // prio 5, ERROR in red
```

This logging handler sends logging events to the SwiftyBeaver Platform, which allows for viewing logs in it's OS X app and consuming via API. To learn more about SwiftyBeaver, visit the [main repository](https://github.com/SwiftyBeaver/SwiftyBeaver) and the [website](https://swiftybeaver.com).

```python
 SwiftyBeaverHandler(app_id, app_secret, encryption_key, device=device)
```

In order to successfully authenticate with the API, `app_id` and `app_secret` have to be provided during initialization. Additionally, `encryption_key` - the key used to encrypt the log entries - is required. `device` is an optional `dict` that should conform to the specification at http://docs.swiftybeaver.com/article/18-sending-logs-via-api. If it is omitted, a mock device will be used.

Please note that logs are transferred AES256CBC-encrypted and, unless configured otherwise, not after every log event. Each log record is associated with a certain number of points, depending on the log level. Log records will then be sent if the collected points are at least `minimum_threshold`. This system is in playe in order to prevent to many API calls during a short time.

## Testing

Run SwiftyBeaver unit tests using `setup.py`:

```sh
$ python setup.py test
```

## General Documentation

**Getting Started:**

- [Features](http://docs.swiftybeaver.com/article/7-introduction)
- [Installation](http://docs.swiftybeaver.com/article/5-installation)
- [Basic Setup](http://docs.swiftybeaver.com/article/6-basic-setup)
​

**Logging Destinations:**

- [Colored Logging to Xcode Console](http://docs.swiftybeaver.com/article/9-log-to-xcode-console)
- [Colored Logging to File](http://docs.swiftybeaver.com/article/10-log-to-file)
- [Encrypted Logging & Analytics to SwiftyBeaver Platform](http://docs.swiftybeaver.com/article/11-log-to-swiftybeaver-platform)


**Stay Informed:**

- [Official Website](https://swiftybeaver.com)
- [Medium Blog](https://medium.com/swiftybeaver-blog)
- [On Twitter](https://twitter.com/SwiftyBeaver)

More destination & system documentation is coming soon!  
Get support via Github Issues, email and [public Slack channel](https://slack.swiftybeaver.com).

## License

SwiftyBeaver for Python is released under the [MIT License](https://github.com/SwiftyBeaver/SwiftyBeaver/blob/master/LICENSE).


