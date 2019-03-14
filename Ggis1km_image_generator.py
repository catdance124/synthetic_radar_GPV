import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import os
from pathlib import Path
import re
import subprocess
import configparser

#Hack to fix missing PROJ4 env var
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap, cm

# 設定読み込み
inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'UTF-8')


def convert_rep_to_level(intensity):
    '''
    https://www.data.jma.go.jp/add/suishin/catalogue/format/ObdObs001_format.pdf
    ※3 1kmメッシュ気象庁レーダー全国合成のレベル値(0~251)に沿って変換する
    '''
    intensity_level = np.zeros_like(intensity)
    intensity_level[intensity==9.999e+20] = 0  # レーダー外の値
    intensity_level[intensity==0.1] = 0
    intensity_level[intensity==260] = 255
    
    # 変換のための各パラメータ
    step_list = [0.1, 0.25, 0.5, 1.0, 2]
    block_first = [0.25, 2.13, 5.25, 10.5, 181]
    data_num = [18, 12, 10, 170, 38]

    for i, step in enumerate(step_list):
        rep = block_first[i] - step
        for i in list(range(data_num[i])):
            rep = round(rep + step, 2)
            mmh = round((rep*2-step)/2, 2)
            intensity_level[intensity==rep] = mmh
            
    return intensity_level

def crop_latlon(intensity, city, d):
    # 緯度経度の設定
    grid_shape = (3360,2560)
    lat_step = (48-20) / grid_shape[0]
    lon_step = (150-118) / grid_shape[1]

    lats = np.zeros((grid_shape[0],1))
    lons = np.zeros((1,grid_shape[1]))

    for i in list(range(grid_shape[0])):
        lats[i][0] = 48 - i*lat_step
    for i in list(range(grid_shape[1])):
        lons[0][i] = 118 + i*lon_step

    lats = np.tile(lats, (1,grid_shape[1]))
    lons = np.tile(lons, (grid_shape[0],1))

    # 座標を指定，その周辺を切り取る
    n = np.where(lats[:,0] < city[0]+d)[0][0]
    s = np.where(city[0]-d < lats[:,0])[0][-1]
    e = np.where(city[1]-d < lons[0,:])[0][0]
    w = np.where(lons[0,:] < city[1]+d)[0][-1]
    
    intensity_city = intensity[n:s,e:w]
    lats_city = lats[n:s,e:w]
    lons_city = lons[n:s,e:w]
    
    return intensity_city, lats_city, lons_city

def draw_map(intensity, city, save_file_path=None):
    # 切り出し
    intensity_city, lats_city, lons_city = crop_latlon(intensity, city, inifile.getint('area', 'd'))

    flat_lats_city = np.ravel(lats_city)
    flat_lons_city = np.ravel(lons_city)
    
    # 色指定
    # black指定 -> 海岸線白，背景黒  white指定 -> 海岸線黒，背景白
    base_color = inifile.get('image', 'base_color')
    coastline_color = 'white' if base_color == 'black' else 'black'
    zero_color = 0 if base_color == 'black' else 1
    
    # 色の変更
    cm = eval('plt.cm.' + inifile.get('image', 'color_map'))
    cm_list = cm(np.arange(cm.N))
    cm_list[0,:3] = zero_color    # カラースケール0番目の値の色を変更
    mycmap = ListedColormap(cm_list)
    
    # 描画矩形座標を指定
    m = Basemap(llcrnrlat=lats_city.min(), urcrnrlat=lats_city.max(), \
                llcrnrlon=lons_city.min(), urcrnrlon=lons_city.max(), \
                resolution=inifile.get('image', 'coastline_quality'))
    
    # 海岸線
    if inifile.getboolean('image', 'draw_coastline'):
        m.drawcoastlines(color=coastline_color)

    # 描画
    m.contourf(x=flat_lons_city, y=flat_lats_city, data=intensity_city, \
               levels=list(range(0,255)), latlon=True, tri=True, cmap=mycmap)
    
    # 枠を消す
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    
    # カラーバー
    if inifile.getboolean('image', 'draw_colorbar'):
        plt.colorbar()
    
    # save
    plt.savefig(save_file_path, transparent=True, \
                bbox_inches = 'tight', pad_inches = 0, facecolor=base_color)  # 余白を消す

    plt.clf()

def bin2img(filepath, save_path=None):
    timestamp = re.findall(r'\d{14}', filepath)[0]
    if save_path is not None:
        os.makedirs(save_path, exist_ok=True)
        save_file_path = save_path + '/' + timestamp + '.png'
        if os.path.exists(save_file_path):  # 既に保存したいファイルがあるときスキップ
            return
    
    # wgrib2で.binファイル(GRIB2ファイル)を読み、形式を変えtemp.binファイルに保存
    subprocess.run(['wgrib2', filepath, '-order', 'we:ns', '-no_header', '-bin', './wgrib2_temp.bin'])
    
    # 読み込み
    f = open('./wgrib2_temp.bin', mode='rb')
    intensity = np.fromfile(f, dtype='float32',sep='').reshape(3360,2560)  # 格子形状に変形し読み込む
    intensity_level = convert_rep_to_level(intensity)  # データ代表値をレベル値に変換

    city = (inifile.getfloat('center_location', 'latitude'), \
            inifile.getfloat('center_location', 'longitude'))  # 座標を指定
    
    draw_map(intensity_level, city, save_file_path=save_file_path)


if __name__ == '__main__':
    bin_path = Path(inifile.get('generate_path', 'bin_path'))
    save_path = inifile.get('generate_path', 'img_path')

    for filepath in sorted(bin_path.glob('**/*.bin')):
        bin2img(str(filepath), save_path)