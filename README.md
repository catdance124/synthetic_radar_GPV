# synthetic_radar_GPV

## env
### linux
ubuntu 18.04.1 LTS  
on VMware Workstation 15 Player  
### windows
windows10 x64
http://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/Windows_64/
synthetic/
　├ Ggis1km_image_generator_WINDOWS.py
　├ temp.bin
　└ wgrib2/
　　├ wgrib2.exe
　　├ cyggcc_s-seh-1.dll
　　├ cyggfortran-3.dll
　　├ cyggomp-1.dll
　　├ cygquadmath-0.dll
　　└ cygwin1.dll

## reference
１kmメッシュ全国合成レーダーGPV  
http://www.jmbsc.or.jp/jp/online/file/f-online30100.html  
http://database.rish.kyoto-u.ac.jp/arch/jmadata/synthetic-original.html  
詳細  
https://www.data.jma.go.jp/add/suishin/catalogue/format/ObdObs001_format.pdf  
活用例  
http://agora.ex.nii.ac.jp/digital-typhoon/radar/graphics/index.html.ja  

## utility
##### wgrib2  
https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/  
commands: https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/long_cmd_list.html  
ref: http://www.hysk.sakura.ne.jp/Linux_tips/how2use_wgrib

##### ~~pygrib~~
データが対応していなかった  
MSMデータなどを使うならこっちが楽そう  

# メモ
## Ubuntu
[/etc/apt/source.list のリポジトリを日本国内に変更する](http://www.aise.ics.saitama-u.ac.jp/~gotoh/HowToInstallUbuntu1804OnWSL.html#toc5)
```
$ cd /etc/apt
$ sudo sed -i.bak -e "s/http:\/\/archive\.ubuntu\.com/http:\/\/jp\.archive\.ubuntu\.com/g" sources.list
$ apt-get update && apt-get -y upgrade
```
## [pyenv](http://blog.algolab.jp/post/2016/08/21/pyenv-anaconda-ubuntu/)
必要なパッケージをインストール
```
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev libpng-dev
```

pyenv インストール
```
$ git clone git://github.com/yyuu/pyenv.git ~/.pyenv
$ git clone https://github.com/yyuu/pyenv-pip-rehash.git ~/.pyenv/plugins/pyenv-pip-rehash
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
$ source ~/.bashrc
```
Anacondaのバージョン確認
```
$ pyenv install -l | grep anaconda3
  anaconda3-5.0.1
  anaconda3-5.1.0
  anaconda3-5.2.0
  anaconda3-5.3.0
  anaconda3-5.3.1
  anaconda3-2018.12
```
ここではAnaconda3-5.3.1をインストール
```
$ pyenv install anaconda3-5.3.1
$ pyenv global anaconda3-5.3.1
$ echo 'export PATH="$PYENV_ROOT/versions/anaconda3-5.3.1/bin:$PATH"' >> ~/.bashrc
$ source ~/.bashrc
```
## pygrib
pygribにはpyprojかbasemapが必要
```
$ conda install basemap
$ conda install -c conda-forge/label/gcc7 pygrib
```
### import BasemapのError回避
PROJ_LIBが見つからないので指定して与える
```python
#Hack to fix missing PROJ4 env var
import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap
```
## jupyter リモート
https://qiita.com/syo_cream/items/05553b41277523a131fd
```
$ pip install jupyter
$ ipython
```
```python
from notebook.auth import passwd
passwd()
```
```
$ mkdir ~/.jupyter
$ vim ~/.jupyter/jupyter_notebook_config.py
```
```python
# ~/.jupyter/jupyter_notebook_config.py
c = get_config()

# Notebook上でplotを表示できるようにする
c.IPKernelApp.pylab = 'inline'
# 全てのIPから接続を許可
c.NotebookApp.ip = '*'
# IPython notebookのログインパスワード
c.NotebookApp.password = 'sha1:1f1f48943783:4da60e7ba677c2184f4d5378b3ca1ef46cc8fe09'
# 起動時にブラウザを起動させるかの設定
c.NotebookApp.open_browser = False
# ポート指定
c.NotebookApp.port = 8888
```
## data 
```
wget -P synthetic/ http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/2017/06/16/Z__C_RJTD_20170616000000_RDR_JMAGPV__grib2.tar
```
## jupyter tips
!,%を付けるとshellが実行できる  
!はアプリケーションで，%はosコマンド？
```python
!wget -nc -P path URL
%cd target_path
ls = %ls
print(ls)
# shellの出力をpython変数に渡すことができる
```
pythonで宣言した変数をshellに渡すことができる  
$をつけて渡す
```python
path = '~/temp'
URL = 'http://hoge.tar'
!wget -nc -P $path $URL
# !wget -nc -P ~/temp http://hoge.tar と等価
```
### wget tips
-nc 同名ファイルは保存しない  
-P path 指定パスに保存する  

### tar tips
-tf tarファイルの中身を確認  
-xvf 展開  
-C path 展開・圧縮先パスを指定

## wgrib2 インストール
FORTRANをインストールし，環境変数に指定しておく
```
$ cd ~
$ sudo apt-get install gfortran
$ export FC=gfortran
$ export CC=gcc
$ wget ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz
$ tar -xvzf wgrib2.tgz
$ cd grib2/
$ make
```
~/grib2/wgrib2/wgrib2が実行ファイル  
パスの通ったディレクトリにコピー
```
$ sudo cp ~/grib2/wgrib2/wgrib2 /usr/local/bin/
```
usage
```
$ wgrib2 data
# 1:0:d=2017010120:var discipline=0 center=34 local_table=1 parmcat=1 parm=201:surface:-10-0 min acc fcst:
```
ID: ? : d=基準日時 : 気象項目 : 条件 : 初期値(anl) or 予測(fcst) :  
vars =
discipline
center
local_table 
parmeter category 
parmeter  
http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/varX.html

## wgrib2 tips
デフォでNS->SNに変換されるので指定してNSのままに
```
$ wgrib2 data -order we:ns
```
ファイル出力ができる  
中身はデータ値が格子に沿って羅列されたもの(ここではNW->SE)  
https://qiita.com/ysomei/items/12d6622bed030f6ac793#ruby-%E3%81%8B%E3%82%89%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B  
-text filename  
-bin filename  
-ieee filename  
出力名に-を指定することで標準出力可能
```
$ wgrib2 data -order we:ns -no_header -text -
```
