# Image for Adalum-Pluto
C/Python bindings for ad.

## build & run
In this directory, run below command

```
$ docker build -t pluto .
```

```
$ docker run --privileged \
    -v /var/run/dbus:/var/run/dbus \
    -v /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
    --rm -it pluto bash
```

`dbus`や`avahi`のマウントは`iio_info`などがデバイスの検索をする場合に必要。`--privilleged`により、ホストの`/dev`以下をコンテナから参照できる。

デバイスごとにマウントする場合は以下の通り。
```
$ docker run --device=/dev/ttyACM0:/dev/ttyACM1 \
    -v /var/run/dbus:/var/run/dbus \
    -v /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
    --rm -it pluto bash
```
ホストの`/dev/ttyACM0`を`/dev/ttyACM1`としてマウントできる。（上記動作せず。Avahiにアクセスできない。）

## Adalum-Plutoに関するメモ

### users guide
-  https://wiki.analog.com/university/tools/pluto/users

### get ip/usb addr
- https://ez.analog.com/wide-band-rf-transceivers/design-support/f/q-a/102669/use-multiple-adalm-pluto-for-gnu-radio

（恐らく[libiio](https://github.com/analogdevicesinc/libiio/blob/master/README_BUILD.md)が必要）
```
$ iio_info -S
```
以下でusbのリスト取得
```
$ iio_info -S | grep -E "\\[usb:.*\\]" | sed -e "s/.*\[\(usb:.*\)\].*/\1/"
```

```python
import subprocess
subprocess.run(R'iio_info -S | grep -E "\\[usb:.*\\]" | sed -e "s/.*\[\(usb:.*\)\].*/\1/"', shell=True)
```

### シリアル通信
[公式ページ](https://wiki.analog.com/university/tools/pluto/drivers/linux)にあるkermitはサポートされていない。`cu`コマンドで代替できる。
```
$ sudo gpasswd -a $USER dialout
$ sudo apt install cu
$ sudo chmod 666 /dev/ttyACM0
$ sudo cu -s 115200 -l /dev/ttyACM0
```

### GNU Radioでiioモジュールのインポートに失敗する
[GNU Radio](https://wiki.analog.com/resources/tools-software/linux-software/gnuradio)を参考にした（libiioのインストール部分だけは[ここ](https://github.com/analogdevicesinc/libiio/blob/master/README_BUILD.md)を見た）がGNU Radioで動かすときに`iio`モジュールに`pluto-source`かなにかがないと言われた。

[これ](https://techfocusalexn.wordpress.com/2021/04/03/setting-up-adalm-pluto-on-ubuntu/)したらうまく行った。下記抜粋。

>In my case (GRC 3.8) one has to copy the gr-iio (originally installed in /usr/local/lib/python3/dist-packages/iio) to /usr/lib/python3/dist-packages. The guide said to copy to gnuradio, which did not help.
Then the export command: export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages should be executed. But that is not all, the Python iio library must be uninstalled (or deleted from /home/[username]/.local/lib/python3.8/site-packages/).

### C/C++ Compile
`iio`へのリンクが必要

```
$ gcc smpl.c -liio
```