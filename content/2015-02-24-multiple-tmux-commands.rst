Executing snmpwalk on multiple devices simultaneously
#####################################################

:date: 2015-02-24 16:22:45
:tags: tmux
:category: programming

I tend to run the same SNMP probes on multiple devices quite often. The devices
are always the same, the OIDs change. To simplify this I created a small Python
script running the commands in a ``tmux`` session.

However, there seems to be a small bug/annoyance in tmux which makes it nearly
impossible to run a command with special characters in it's parameters directly
via tmux. Instead, "injecting" the keystrokes into the running session works
fine.

I started off writing this in ``bash``, but due to the issue mentioned above, I
ended up writing it in Pythong, making the code a lot cleaner. Albeit
unnecessary:

.. code:: python
    :class: highlight

    #!/usr/bin/python3
    '''
    Run "snmpwalk" on multiple devices simultaneously in separate tmux tabs.
    '''

    from collections import namedtuple
    from os import environ
    from subprocess import check_call as run
    import sys

    environ['TERM'] = 'xterm-256color'  # Hint for tmux to enable 256 colours.

    Connection = namedtuple('Connection', 'ip, community, name')


    TMUX_NAME = 'snmpt-probe'
    TARGET_DEVICES = [
        Connection('1.2.3.4', 'helloworld', 'Device 1'),
        Connection('1.2.3.5', 'helloworld', 'Device 2'),
        Connection('1.2.3.6', 'helloworld', 'Device 3'),
        Connection('1.2.3.7', 'helloworld', 'Device 4'),
    ]


    def exec_(ip, oid, community):
        '''
        Run a command using ``tmux send-keys``.

        This is a workaround. Executing the command directly does not work if a
        parameter contains special characters.
        '''
        run(['tmux', 'send', '-t', TMUX_NAME, ' snmpwalk -v2c -c "'])
        run(['tmux', 'send', '-t', TMUX_NAME, community])
        run(['tmux', 'send', '-t', TMUX_NAME, '" %s %s | less' % (ip, oid)])
        run(['tmux', 'send', '-t', TMUX_NAME, 'ENTER'])


    def main():

        # Ask the user to enter the OID
        oid = input('OID: ').strip()
        if not oid:
            print('OID cannot be empty!', file=sys.stderr)
            return 1


        # Create a new, empty tmux session
        run(['tmux', 'new', '-s', TMUX_NAME, '-d'])

        # give the first window it's proper name
        run(['tmux', 'rename-window', '-t', '0', TARGET_DEVICES[0].name])

        # create the remaining tabs with appropriate names
        for _, _, name in TARGET_DEVICES[1:]:
            run(['tmux', 'new-window', '-n', name])

        # run the snmpwalk commands
        for ip, community, name in TARGET_DEVICES:
            run(['tmux', 'select-window', '-t', name])
            exec_(ip, oid, community)

        # Attach the tmux session
        run(['tmux', 'attach', '-t', TMUX_NAME])
        return 0


    if __name__ == '__main__':
        sys.exit(main())
