Usage
=====

Simple program for testing::

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-

    import time


    if __name__ == '__main__':
        # exit()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            print()

Simple config for supervisor::

    [program:infinity1]
    command = /etc/supervisor/infinity.py
    stdout_logfile = /var/log/supervisor/infinity1-out.log
    autostart = true
    autorestart = true
    redirect_stderr = true

::

    >>> import svdlib.core
    >>> t = svdlib.core.Supervisor()
    >>> t.reread()
    >>> [{'name': 'infinity1', 'status': 'available'}, {'name': 'infinity2', 'status': 'available'}]

    >>> t.add('infinity1')
    >>> {'result': False, 'status': 'ERROR', 'msg': 'process group already active'}

    >>> t.add('infinity2')
    >>> {'name': 'infinity2', 'result': True, 'msg': 'added process group'}
    >>> t.add('infinity2')
    >>> {'msg': 'process group already active', 'status': 'ERROR', 'result': False}

    >>> t.status(process='infinity1')
    >>> {'status': 'RUNNING', 'name': 'infinity1', 'pid': '2013', 'uptime': '0:21:25'}
    >>> t.status()
    >>> [{'uptime': '0:22:14', 'pid': '2013', 'status': 'RUNNING', 'name': 'infinity1'}, {'uptime': '0:00:03', 'pid': '2238', 'status': 'RUNNING', 'name': 'infinity2'}]

    >>> t.stop(process='infinity2')
    >>> {'result': True, 'status': 'stopped', 'name': 'infinity2'}

    >>> t.remove(process='infinity2')
    >>> {'msg': 'removed process group', 'result': True, 'name': 'infinity2'}

    >>> t.remove(process='infinity2')
    >>> {'name': 'infinity2', 'result': False, 'status': 'ERROR', 'msg': 'no such process/group'}


License
=======

Apache License Version 2.0, January 2004
