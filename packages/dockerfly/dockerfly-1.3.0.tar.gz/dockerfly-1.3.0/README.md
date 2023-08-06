dockerfly，让你的容器更真实
=====================================
dockerfly是为了让你的container运行起来"更像"一台真正的虚拟机，对网络部分做点包装的小工具。
dockerfly不是大而全的容器管理工具，如果你要管理10台以上的物理机，或者运维30个以上的服务，那么dockerfly不适合你。
如果你每天为了开发测试环境的统一而心烦，如果你想在自己的笔记本上为自己的不同项目镜像分门别类，那么dockerfly就是为你准备的。

dockerfly为你搭建穷人版的vSphere (^_^)。

缘起
========================

docker推荐一个container内只运行一个进程，网络部分同docker主机共享。使用supervisor管理多进程。
在很多真实场景下，这种方法局限性很大。

例如，我有一个项目A，里面已经采用了supervisor管理多个进程，另外带有web，我希望能有docker快速建立一个Container，用于平时的测试和开发。
这样你的选择只能是:

* 建立的container采用端口映射的办法，把80端口映射到docker主机

* 把进程放到supervisor里面，每次run container的时候启动

* 操作需要用 `docker exec -i -t <container_id> bash` 上去

这样的局限很明显的:

* 这台container没有自己的对外IP，很多TestCase跑起来会很复杂

* 我无法同时启动多个占用80端口的container

* 无法在另外一台机器获得shell

* 我自己进程管理的supervisor和docker用的supervisor会混在一起，不干净

解决办法
--------

在container中开启sshd，把它想象成一台真正的虚拟机。

[baseimage-docker](http://phusion.github.io/baseimage-docker/)也做了一些类似的工作，但是dockerfly将基本镜像，container创建等操作结合起来，更为方便。


警告
--------

已经有很多人警告过这种方法是不可取的，因为docker诞生之初并不是为了构建一个Vmware类的虚拟机来设计的。
这样做会有安全性上的问题，dockerfly在实现的时候没有过多考虑安全问题，它只是假设你在一台完全由你控制的机器上，方便的搭建开发测试环境。

安装:
========================

* 推荐linux内核3.18以上，推荐开启docker overlay文件系统。`docker>=1.6`

*  pull一个实验镜像下来

    ```
    docker pull memorybox/centos6_sshd
    ```

*  安装dockerfly

    ```
    git clone https://github.com/memoryboxes/dockerfly.git && pip install -r dockerfly/requirements.txt
    cd dockerfly && ./run.sh
    ```

* 将需要Attach的物理网卡(如eth1)设置为混杂模式

    ```
    ifconfig eth1 promisc
    ```

* 访问`http://host:80` ，会有一个很简单的web页面，供你创建/删除、启动/停止你的container。
  创建一台container后，你可以直接ssh登陆，在上面像VMware虚拟机一样操作。
  tcpdump一下，你可以看到网络数据包和真正的网卡流量是一致的。

怎样工作:
========================

dockerfly采用了在容器内创建Macvlan网卡的办法来增强docker的网络功能。

* 我有一台物理机或是Vmware虚拟机-PhysicalHostA，有两块网卡:eth0和eth1，同在192.168.1网段，是互通的

        +---------+
        | Physical|
        \ HostA   /
        |\       /|
        | ------  |
        | eth0 ------ 192.168.1.10/24, gateway:192.168.1.1
        | eth1 ------ 192.168.1.11/24, gateway:192.168.1.1
        +---------+

* 首先启动一台docker container

    ```
    docker run -i -t xxx /bin/bash
    ```

* 在物理机中创建一个Macvlan网卡Attach到eth1上

    ```
    ip link add MacVlanEthA link eth1 type macvlan mode bridge
    ```

* 得到docker container的pid，用ip link命令把虚拟网卡映射到docker的network namespace中

    ```
    ip link set netns $(docker container pid) MacVlanEthA
    ```

>> docker的pid可以用dockerfly提供的脚本获取

>> ```
>> python dockerfly/bin/dockerflyctl.py getpid <container_id>
>> ```

* 为MacVlanEthA设置IP，路由

    ```
    docker exec $(docker container id) ip route del default
    docker exec $(docker container id) ip addr add 192.168.1.100 dev MacVlanEthA
    docker exec $(docker container id) ip route add default via 192.168.159.1 dev MacVlanEthA
    ```

* 在docker container xxx内执行:

    ```
    ifconfig
    ```

   可以看到MacVlanEthA的ip被设置为192.168.1.100

* 设置物理机eth1为混杂模式

    ```
    ifconfig eth1 promisc
    ```

* 在物理机执行:

    ```
    [PhysicalHostA@localhost]~# ping 192.168.1.100
    PING 192.168.159.1 (192.168.1.100) 56(84) bytes of data.
    64 bytes from 192.168.1.100: icmp_seq=1 ttl=128 time=0.663 ms
    64 bytes from 192.168.1.100: icmp_seq=2 ttl=128 time=0.180 ms
    ...
    ```


* 用类似的方法添加新的容器及网卡，此时的网络组成如下图:


                                                               +-----------------------------------------------+---------------+
        +---------+                  *******                   |                    Physical host Docker                       |
        | Physical|                **       **                 |   +---------+           +---------+           +---------+     |
        \ hostA   /              **  Local    **               |   | Docker  |           | Docker  |           | Docker  |     |
        |\       /|  --------->  *   NetWork   *  <----------- |   \ hostA   /           \ hostB   /           \ hostC   /     |
        | ------  |              **           **               |   |\       /|           |\       /|           |\       /|     |
        |eth0,eth1|                **       **                 |   | ------  |           | ------  |           | ------  |     |
        +---------+                  *******                   |   | MacVlan |           | MacVLan |           |...EthC1 |     |
                                                               |   | EthA    |           | EthB    |           |   EthC2 |     |
                                                               |   +---------+           +---------+           +---------+     |
                                                               |  192.168.1.100         192.168.1.101          192.168.1.102   |
                                                               |                                               192.168.1.103   |
                                                               +-----------------------------------------------+---------------+

* 如果你的container内开启sshd服务的话，此时可以直接把这些container当作VMWare的虚拟机来用了。

>> 如何在镜像内开启sshd，可以参考:

>> https://github.com/tutumcloud/tutum-centos

>> https://github.com/tutumcloud/tutum-ubuntu

* 如果你只是想简单试用一下的话，我做了一个基础镜像，默认用户名/密码是:root/rootroot，放在

    https://registry.hub.docker.com/u/memorybox/centos6_sshd/

  可以执行下面命令获取:

  ```
  docker pull memorybox/centos6_sshd
  ```

**dockerfly就是将上面这些操作做了一个简单封装，供你轻松地1秒钟启动一台类似Vmware虚拟机。**

Caveats
========================

再次警示一下，这样做并不是docker的推荐做法。问题如下:

* 多个虚拟网卡绑定到一个混杂模式的物理网卡上，会有网络性能问题

* 在container中开启sshd服务，无法保证安全性

* 用户以root身份在container中操作，容易导致所有container挂掉

* 最后，这些功能其实用Vagrant等工具也可以实现的，只不过是学习成本的大小而已

如果你不Care这些问题，你会感觉使用dockerfly创建的container，感觉和Vmware虚拟机是一样的，而且你获得了近似于物理机的性能，以及秒级别的创建/删除container的能力。

**Different people use Docker for different purposes, so Don't be afraid, but be careful.**

Best Practice:
========================

dockerfly比较适合下面几个场景:

每日构建
---------

传统的每日构建一般只会build出二进制包，利用docker，可以每天构建一个带有执行环境的container，这样开发和测试都可以从dockerfly中轻松启用一台即时构建的container，提升开发测试效率。

回归测试
--------

* 一般回归测试为了保证执行环境的统一，都要在setUp和tearDown中写许多环境相关的代码。

* dockerfly提供了简单的Restful API接口，可以创建/删除/启动/停止/执行命令/拷贝文件等，这样终于可以走进`创建一台机器->跑一个测试`的时代了，而且启动/删除container的动作在秒钟级别，效率很高。环境无疑是最干净的。

临时项目开发
--------------

像多个python项目环境的隔离，一直用virtualenv之类的工具，用container来隔离会更干净，同时可以将一台机器划分成多个项目的containers，每台container分配一个IP，服务各行其道，互不干扰。


Reference
========================

* Linux 上的基础网络设备详解

http://www.ibm.com/developerworks/cn/linux/1310_xiawc_networkdevice/index.html

* Linux 上虚拟网络与真实网络的映射

http://www.ibm.com/developerworks/cn/linux/1312_xiawc_linuxvirtnet/index.html

* 网络虚拟化技术: TUN/TAP MACVLAN MACVTAP

https://blog.kghost.info/2013/03/27/linux-network-tun/

* Coupling Docker and Open vSwitch

http://fbevmware.blogspot.com/2013/12/coupling-docker-and-open-vswitch.html

* four ways to connect a docker

http://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/

* Docker containers should not run an SSH server

https://news.ycombinator.com/item?id=7950326

* Proposal: Native Docker Multi-Host Networking

https://github.com/docker/docker/issues/8951

License (Simplified BSD)
========================
http://choosealicense.com/licenses/bsd-2-clause/

LATEST VERSION
========================
1.3.0

