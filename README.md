synthetic_radar_GPV
====
レーダーエコー強度画像を作成するツール\
中身について[Qiita](https://qiita.com/kinosi/items/56b664d9a10d35b4a183)の記事があります．

## Description
[京都大学生存圏研究所データベース](http://database.rish.kyoto-u.ac.jp/arch/jmadata/synthetic-original.html)から[１kmメッシュ全国合成レーダーエコー強度GPV](http://www.jmbsc.or.jp/jp/online/file/f-online30100.html)を取得し，レーダーエコー強度画像を作成します．\
京都大学生存圏研究所データベースの気象庁データは**学術目的に限り**無償利用可能です．

## Demo
画像の座標・範囲，画像の背景色，カラーバーの有無，カラーマップの指定，海岸線の有無，海岸線の質が選択できます．\
以下は`2018/07/03 11:00:00`の`(31.33, 130.34)`を中心にした画像
| detail | image(2018/07/03 11:00:00) |
|:-----------|:------------:|
| 背景: 白<br>カラーバー: 有<br>カラーマップ: jet<br>海岸線: 有<br>海岸線の質: low | <img src="https://user-images.githubusercontent.com/37448236/54401344-a1203b80-470a-11e9-9beb-212fc94ea189.png" width=50%> |
| 背景: 白<br>カラーバー: 無<br>カラーマップ: jet<br>海岸線: 有<br>海岸線の質: crude | <img src="https://user-images.githubusercontent.com/37448236/54401342-9ebde180-470a-11e9-950d-99f8aa427660.png" width=50%> |
| 背景: 黒<br>カラーバー: 有<br>カラーマップ: jet<br>海岸線: 有<br>海岸線の質: low | <img src="https://user-images.githubusercontent.com/37448236/54401335-98c80080-470a-11e9-8d5a-83b385097a52.png" width=50%> |
| 背景: 黒<br>カラーバー: 有<br>カラーマップ: gray<br>海岸線: 無 | <img src="https://user-images.githubusercontent.com/37448236/54401339-9c5b8780-470a-11e9-905f-dcb5a6ac2f0d.png" width=50%> |
| 背景: 白<br>カラーバー: 無<br>カラーマップ: jet<br>海岸線: 無 | <img src="https://user-images.githubusercontent.com/37448236/54401348-a3829580-470a-11e9-8e9b-94bffa2f83d4.png" width=50%> |

## Requirement
matplotlib, numpy, Basemap,
[wgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)

## Usage
### `config.ini`に設定記入
```python
[period]
# format
#    start = YYYY/mm/dd HH:MM:SS
#    end   = YYYY/mm/dd HH:MM:SS
start = 2018/07/01 00:00:00
end   = 2018/07/05 00:00:00
```
- period -> ダウンロードする期間に関するセクション
    - start -> 期間の始まり
    - end -> 期間の終わり
```python
[interval]
# format
#    num ... number of time interval
#    timescale: {'minutes', 'hours', 'days', 'weeks'}
# e.g. num=2, timescale=hours -> download at 2 hours inteval
# CAUTION: minimum interval is 10 minutes!
num = 10
timescale = minutes
```
- interval -> ダウンロードする間隔に関するセクション
    - num -> 時間の数字部分
    - timescale -> 時間スケールを指定（下記が使えます）[timedelta](https://docs.python.org/ja/3/library/datetime.html#datetime.timedelta)の引数に準拠
        - minutes
        - hours
        - days
        - weeks
    
        num = 20, timescale = daysとすると，20日間隔でデータを取得する．\
        **データ自体が10分間隔で取得されているので，それより細かい時間指定は不可能**
```python
[download_path]
# format
#    tar_path ... temporary save location for downloaded tar file
#    bin_path ... save location for bin file
tar_path = ./tar
bin_path = /mnt/hgfs/kagoshima/bin_test
```
- download_path -> ファイルパスに関するセクション
    - tar_path -> 取得した.tarファイルの保存先（逐次削除するので一時的にしかファイルはありません）
    - bin_path -> 取り出した.binファイルの保存先
```python
[generate_path]
# format
#    bin_path ... location of saved bin file (default: same as download_path.bin_path)
#    img_path ... save location for generated image
bin_path = ../weather/data/kagoshima/bin_test
img_path = ../weather/data/kagoshima/bin_test/img_kagoshima
```
- generate_path -> ファイルパスに関するセクション
    - bin_path -> .binファイルが保存されているディレクトリ（基本的には[download_pathセクションのbin_path](https://qiita.com/kinosi/items/56b664d9a10d35b4a183#%E3%82%B3%E3%83%B3%E3%83%95%E3%82%A3%E3%82%B0%E8%AA%AC%E6%98%8E)と同じです）
    - img_path -> 作成した画像ファイルの保存先
```python
[center_location]
# format
#    latitude  ... latitude of image's center location
#    longitude ... longitude of image's center location
latitude  = 31.33
longitude = 130.34
```
- center_location -> 画像の中心座標に関するセクション
    - latitude -> 中心の緯度
    - longitude -> 中心の経度
```python
[area]
# format
#    d ... distance from image center(lat,lon) to edge
d = 2
```
- area-> 画像がカバーする範囲に関するセクション
    - d-> 中心から東西南北に±dを画像の範囲とする
```python
[image]
# format
#    base_color: {'black', 'white'} ... image's backgroud color
#    color_map: e.g.{'jet', 'gray'}(Colormaps in Matplotlib) ... image's cloud color
#    draw_coastline: bool ... whether to draw coastline
#    coastline_quality: {c(crude), l(low), i(intermediate), h(high), f(full)}
#                      ... coastline quality (only when draw_coastline is True)
#    draw_colorbar: bool ... whether to draw colorbar
base_color = white
color_map = jet
draw_coastline = True
coastline_quality = l
draw_colorbar = True
```
- image-> 画像の見た目に関するセクション
    - base_color-> 画像全体の背景の色（下記が使えます）
        - black
        - white
    - color_map-> 降水強度を描画するカラーマップ（下記で動作確認しました）[matplotlib.cm](https://matplotlib.org/examples/color/colormaps_reference.html)に準拠します
        - jet
        - gray
    - draw_coastline-> 海岸線を描画するかどうか
    - coastline_quality-> 海岸線の描画精度（draw_coastline = Trueのときのみ動作）（下記が使えます）
        - c
        - l
        - i
        - h
        - f
    - draw_colorbar-> カラーバーを描画するかどうか
```python
[windows]
# for windows wgrib2 path setting
wgrib2_path = C:/Users/Milano/Desktop/wgrib2/wgrib2.exe
```
- windowsで`Ggis1km_image_generator_WINDOWS.py`を起動する際にwgrib2のパスを設定する必要がある
### スクリプト起動
上記`config.ini`設定後，スクリプト起動
```bash
$ python Ggis1km_downloder.py
```
```bash
$ python Ggis1km_image_generator.py
```
`download_path.bin_path`に１kmメッシュ全国合成レーダーエコー強度GPVバイナリファイル(GRIB2形式)が，\
`generate_path.img_path`に作成した画像ファイルが保存される．

## Install
```bash
$ git clone https://github.com/catdance124/synthetic_radar_GPV.git
```
### wgrib2 install
```bash
$ cd ~
$ sudo apt-get install gfortran
$ export FC=gfortran
$ export CC=gcc
$ wget ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz
$ tar -xvzf wgrib2.tgz
$ cd grib2/
$ make
$ sudo cp ~/grib2/wgrib2/wgrib2 /usr/local/bin/
```
### Basemap install
```bash
$ conda install basemap
```


___
___
# 以下開発時メモ

## env
### linux
ubuntu 18.04.1 LTS  
on VMware Workstation 15 Player  
### windows
仮想環境ではmatplotlibのsavefigがどんどん遅くなっていったので  
クラスタで回すために対応させた  

windows10 x64  anaconda
```
$ conda install basemap
```
http://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/Windows_64/  
ファイル配置  
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
## Basemap
```
$ conda install basemap
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
### .pyでは使えないので
subprocessを代用
```python
import subprocess
subprocess.run(['./wgrib2/wgrib2.exe',filepath,'-order','we:ns','-no_header','-bin','temp.bin'])
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
