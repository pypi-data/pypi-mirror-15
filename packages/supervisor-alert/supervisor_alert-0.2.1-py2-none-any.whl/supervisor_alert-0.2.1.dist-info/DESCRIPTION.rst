supervisor-alert
================

Are you using `Supervisor <http://supervisord.org>`__ to manage
processes on a server? With supervisor-alert you can receive messages
when the state of your processes change. Be the first to know when your
services die!

To send messages on Telegram you need to install and set up
`telegram-send <https://github.com/rahiel/telegram-send>`__ first. You
can also use any shell command to send the notifications.

Installation
============

Install supervisor-alert on your system:

.. code:: shell

    sudo pip install supervisor-alert

Then create the file ``/etc/supervisor/conf.d/supervisor_alert.conf`` as
root:

.. code:: shell

    [eventlistener:supervisor_alert]
    command=supervisor-alert --telegram
    events=PROCESS_STATE_RUNNING,PROCESS_STATE_EXITED,PROCESS_STATE_FATAL
    autostart=true
    autorestart=true
    user=supervisor_alert

This will send the notifications over Telegram, to use something else,
for example `ntfy <https://github.com/dschep/ntfy>`__, pass in the
command:

.. code:: shell

    command=supervisor-alert -c 'ntfy send'

This configuration will run the event listener as the user
``supervisor_alert``. It is a good practice to isolate services by
running them as separate users (and avoiding running them as root). Add
the user with:

.. code:: shell

    sudo adduser supervisor_alert --system --no-create-home

Optionally, you can also subscribe to different supervisor events, `look
at the docs <http://supervisord.org/events.html#event-types>`__ to see
on which ones you'd like to be notified.

Finally, load the config and start the event listener:

.. code:: shell

    sudo supervisorctl reread
    sudo supervisorctl update

You should now receive your first alert, notifying you that
``supervisor_alert`` has started running.


