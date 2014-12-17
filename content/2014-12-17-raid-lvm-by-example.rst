Linux LVM and RAID recovery
===========================

:date: 2014-12-17 15:16:47
:tags: linux, raid, lvm
:category: sysadmin

.. contents::
    :depth: 2
    :backlinks: top

This little tutorial will first create a RAID array, and one LVM volume using
dummy files. Next it will simulate the case where you would like to recover
from just one device, and finally reassemble the complete array again.


Creating the Software RAID Array
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required packages
-----------------

::

    sudo aptitude install \
        lvm2 \
        mdadm


Creating files for testing
--------------------------

::

    dd if=/dev/zero of=disk1 bs=1M count=30
    dd if=/dev/zero of=disk2 bs=1M count=30


Create devices for these files
------------------------------

``mdadm`` only accepts valid block devices for raid members. We use the
loopback device for this::

    sudo losetup /dev/loop0 disk1
    sudo losetup /dev/loop1 disk2


Create the RAID array
---------------------

::

    sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/loop0 /dev/loop1


Verify integrity
----------------

Running ``cat /proc/mdstat`` should show you the following now::

    Personalities : [raid1]
    md0 : active raid1 loop1[1] loop0[0]
          30656 blocks super 1.2 [2/2] [UU]

    unused devices: <none>


The ``[UU]`` shows us that both devices are up.


Creating Logical Volumes
~~~~~~~~~~~~~~~~~~~~~~~~

As the devices have never been used in LVM, we need to create everything first::

    sudo pvcreate /dev/md0

This flags the devices as member in a *volume group*. Now we can craete a
*volume group* with this raid array as member::

    sudo vgcreate foobar /dev/md0

To see that it worked, run the following::

    sudo vgs

You should see the following::

    VG     #PV #LV #SN Attr   VSize  VFree
    foobar   1   0   0 wz--n- 28.00m 28.00m

This shows us that we have one *volume group* (you can imagine this as a
virtual hard-disk) with a bit less than 30MB of free space (we created 30M
files in the very first step).

Finally, we can create our *logical volumes* (virtual partitions). Let's create
two 10M partitions::

    sudo lvcreate -L10M -n part1 foobar
    sudo lvcreate -L10M -n part2 foobar

This will create two volums with the names *part1* and *part2*. They should now
be available in ``/dev/foobar`` or ``/dev/mapper`` and can be used like regular
disks. To see a quick status, you can run the commands ``pvs``, ``vgs`` and
``lvs`` for quick reports about *physical volumes*, *volume groups* and
*logical volumes*.


Cleanup
~~~~~~~

.. note::
    This is **only** necessary if you followed the above steps to simulate real
    devices using regular files. We need to free up all references before we can
    remove the loopback devices.

To simulate the physical connection, you can run the following commands to
clean up everything from the previous step::

    sudo vgchange -a n foobar  # This deactivates the volume group from LVM
    sudo mdadm --stop /dev/md0  # This removes the /dev/md0 device and frees up the loopback devices /dev/loop[01]
    sudo losetup -d /dev/loop0  # Finally, this removes the loopback devices
    sudo losetup -d /dev/loop1


Recovery
~~~~~~~~

Let's assume that you have only one disk, and you need to recover data from
this disk. This section shows how to reassemble everything.

As both the software raid and LVM store metadata in the devices (superblocks),
the reassembly is much easier than creation.

.. note::

    If you are using the dummy files as created above, we will set only one of
    the two files as block device. This is equivalent to physically connecting
    only one device::

        sudo losetup /dev/loop0 disk1


RAID
----

First we scan for RAID devices::

    sudo mdadm --assemble --scan

You should see the following::

    mdadm: /dev/md/0 has been started with 1 drive (out of 2).

And a quick look at ``/proc/mdstat`` shows the following::

    Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10]
    md0 : active raid1 loop0[0]
          30656 blocks super 1.2 [2/1] [U_]

    unused devices: <none>

Seeing ``[U_]`` shows us that one device is up, and the other one missing.


LVM
---

Now that the raid device ``/dev/md0`` is up and running, we can scan for LVM
metadata::

    sudo vgscan

This should show up with the following message::

    Reading all physical volumes.  This may take a while...
    Found volume group "foobar" using metadata type lvm2

Now, running the command ``pvs``, ``vgs`` and/or ``lvs`` should show the
previously created devices.


Restarting the array with all devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After recovery, you can reassemble the array with all devices in the exact same
way as in the previous "recovery" step. But in this case, you should see both
devices as "up" in ``/proc/mdstat``.
