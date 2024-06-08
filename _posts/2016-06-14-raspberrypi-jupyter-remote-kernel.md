---
layout: post
title: "Remote control a Raspberry Pi with Jupyter notebooks"
date: 2016-06-14
categories: jupyter raspberrypi
---


I have built [jupyter notebooks](jupyter.org) into my workflow in many areas.   They are great for integrating documentation, math, plots and code.  Interactive coding also makes proving out concepts fast.
The Raspberry Pi is a cool inexpensive embedded computer that has enough computation power to run a full linux stack with python. 

Why not use a jupyter notebook for running remote raspberry pi code.  In this blog post, I describe one method to use remote jupyter kernels to make experimenting with python IO code very easy.   

## Prereqs

I assume you have a headless raspberry pi with passwordless authentication setup and you know the ip address of the device.   I also assume you have a linux host (development machine), but portions will work on other operating systems.  

## Communication

In this post, I describe how to make a remote kernel on the rasperry pi.  This adds an additional communication link in the jupyter framework.   The browser uses http to access the jupyter notebook server.  Jupyter uses ZMQ to access local kernels, in this case ipythonkernel.   Ipythonkernel uses ssh to access your remote raspberry pi device and instantiate a local python kernel.  

![Browser-html-Jupyter-zmq-remote_ikernel-ssh-ipythonkernel](/blog/assets/2016/remote_ikernel_comm.svg)

Once we have this setup, we have a special kernel option in jupyter notebook that lets us run a remote notebook on the device.

## Raspberry Pi

### miniconda
[Miniconda](https://www.continuum.io/content/conda-support-raspberry-pi-2-and-power8-le) is a stripped down version of conda.

Conda makes installing python packages easy.   Miniconda is available for the armv7 processor on raspberry pi for standard packages.

First install miniconda on your raspberry pi [http://repo.continuum.io/miniconda/Miniconda-latest-Linux-armv7l.sh](http://repo.continuum.io/miniconda/Miniconda-latest-Linux-armv7l.sh)

Now through ssh we can install conda and pip packages.

    conda install numpy
    pip install ipykernel

Ipykernel is the package that includes ipython kernel that runs from a jupyter notebook. 

## Host

### Remote_ikernel

[Remote_ikernel](https://bitbucket.org/tdaff/remote_ikernel) 
is a package that acts as a local kernel for jupyter, but makes a connection to a remote kernel.   This acts as a gateway.  Communications is wrapped in an ssh tunnel. You can install this via source.

    hg clone https://bitbucket.org/tdaff/remote_ikernel
    python setyp.py install 

The remote_ikernel command automatically configures jupyter to add a kernel.
Replace pi@host with the ip address of your device.  

    remote_ikernel manage --add \
          --kernel_cmd="/usr/bin/env ipython kernel -f {connection_file}"  \
          --name="Python RPI" --interface=ssh \
          --host=pi@host --workdir='~' --language=python

The utility creates a kernel file where jupyter knows to look for it.

~/.local/share/jupyter/kernels

Restart jupyter notebook and you will see another kernel option. 

### Raspberry Pi IO

We can then access raspberry pi io from within a jupyter notebook.

![screenshot](/blog/assets/2016/remote_rpi_screenshot.png)

Here is a code snippet to peek at I2C registers.

    from __future__ import print_function
    import smbus
    
    def dumpio(bus, address, size, offset=0, pagesize=16):
        print("      ", "".join(['   %0x ' % i for i in range(pagesize)]))
        for page in range(0,size, pagesize):
            data = [bus.read_byte_data(address, reg) for reg in range(page, page+pagesize)]           
            print("0x%02x: " % page, "".join(['0x%02x ' % z for z in data]))
    
    bus = smbus.SMBus(1)
    address = 0x6B
    size = 0x40
    dumpio(bus, address, size)


### Remote file system

Sshfs allows creating a folder that gets synced with your raspberry pi similar to Dropbox.   If you write python libraries that you reference from a notebook, this makes it easy to edit code on the fly. 

[https://help.ubuntu.com/community/SSHFS](https://help.ubuntu.com/community/SSHFS)

These commands install and setup a linked folder.  Replace pi@host and paths.

    sudo apt-get install sshfs
    sudo gpasswd -a $USER fuse
    mkdir /home/me/local/path
    sshfs -o idmap=user pi@host:/home/pi/remote/path ~/local/path

You can unmount it later with this command.

    fusermount -u ~/local/path

![sshfs](/blog/assets/2016/remote_ikernel_fs.svg)



