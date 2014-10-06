Automatically Sync Files on WIFI Connect
########################################

:date: 2014-10-06 19:56:49
:tags: linux, lifheack
:category: automation

I recently discovered wicd_ (thanks to Gefoo_). It is a really nifty network
manager. And it supports running scripts on each connection stage for a
network. This immediately gave me an idea:

.. _wicd: http://wicd.sourceforge.net/
.. _Gefoo: https://gefoo.org/

I like taking photos, and sometimes I unload them from my camera to my laptop
for immediate housekeeping. I keep them on an in-house NAS for safe-keeping.
Being able to run scripts once the laptop connects, lets me sync the files
automagically to my NAS. This is awesome, and this article summarises how I've
implemented it.

It is actually quite straight-forward. The wicd documentation mentions that you
should modify one the following settings (depending on what you need):

* ``afterscript``
* ``postdisconnectscript``
* ``beforescript``
* ``predisconnectscript``

However, this did not work for me. After editing the file, the values reverted
to their original value (``None``). I assume that you need to stop the wicd
service before editing it. I did not do that, and I assume that the file is
written when wicd ends. This would explain this issue. But there is also
another way, which I followed fo the rest of this.

As an alternative, you can just drop executable scripts into one of the
``/etc/wicd/scripts`` subfolders. For my task, I chose ``postconnect``. I use
this script as an "orchestration" script which launches other scripts as
needed. For now it only contains one script, and looks like this:


.. code:: bash
    :class: highlight

    #!/bin/bash
    conntype="$1"
    essid="$2"
    bssid="$3"

    if [ "$conntype" == "wireless" ]; then
        if [ "$essid" == "MichTik" ]; then
            /opt/wicd/scripts/filedrop
        fi
    fi


This says, that as soon as a wireless connection is established on the SSID
"MichTik", the script ``/opt/wicd/scripts/filedrop`` should be executed.

That script in turn looks like this:

.. code:: bash
    :class: highlight

     #!/bin/bash
     LOGFILE=/var/log/filedropper.log

     # SSH Private Key for fully unattended operation. This key must be
     # passwordless, so the containing directory should have the proper access
     # rights.
     IDENTITY=/opt/wicd/scripts/sshkeys/filedrop

     # Any file created by this script (the logfile) should be secured.
     umask 0077

     echo "$(date +"%F %T") dropping new files..." >> $LOGFILE

     ##
     # drop(src, dest)
     #
     # Moved files from "src" to "dest".
     #
     # WARNING
     # This uses rsync with --remove-source-files, so you should make sure that
     # files are not modified *while* this is running! Read the according
     # section of the rsync man-page for details!
     ##
     function drop() {
         src=$1
         dst=$2
         rsync -a \
             --partial \
             --remove-source-files \
             -e "ssh -l exhuma -i ${IDENTITY}" \
             ${src} \
             ${dst} >> ${LOGFILE}
     }

     drop /home/exhuma/photos \
          192.168.1.1:/mnt/media/incoming/filedrop/

     echo "$(date +"%F %T") DONE." >> $LOGFILE

And that's it!

.. note::
    Security of this could be improved. For example, I am using my own user on
    the filedrop target. Which means that if my laptop is compromised, and
    someone would get their hands on this passwordless key, that person could
    wreak all kinds of havoc. After I finish this article, I will set up a
    dedicated user on the NAS for this purpose. And you should do so too :P
