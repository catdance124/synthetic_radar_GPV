import os
import datetime
import subprocess
import re
import configparser

class Downloader:
    def __init__(self, tar_path, bin_path):
        self.tar_path = tar_path
        self.bin_path = bin_path
        subprocess.run(['mkdir', '-p', self.tar_path])
        subprocess.run(['mkdir', '-p', self.bin_path])
    
    def set_date(self, dt):
        # URLを指定
        directory = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original'
        date = dt.strftime('%Y/%m/%d')
        self.timestamp = dt.strftime('%Y%m%d%H%M%S')
        tar_filename = 'Z__C_RJTD_'+self.timestamp+'_RDR_JMAGPV__grib2.tar'
        self.URL = directory +'/'+ date +'/'+ tar_filename
        self.tar_file_path = self.tar_path + '/' + tar_filename
        self.bin_path_year = self.bin_path + '/' + dt.strftime('%Y')
        subprocess.run(['mkdir', '-p', self.bin_path_year])
        
    def get_bin_file(self):
        # binファイルがあるかを確認
        bin_file_path = self.bin_path_year+'/Z__C_RJTD_'+self.timestamp+'_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin'
        if os.path.exists(bin_file_path):
            print('already exist: ',bin_file_path)
        else:
            # tarファイルを~/tarに保存
            wget_result = subprocess.getstatusoutput('wget -nc -P '+self.tar_path+' '+self.URL)  # getstatusoutputは(exitcode, output)を返す
            if wget_result[0] != 0:  # ダウンロードエラーの場合
                error_detail = re.findall(r'エラー.*', wget_result[1])[0]
                self.out_error_URL('download', error_detail)
            else:
                # tarファイルから1kmメッシュデータのみを取り出す
                filelist = subprocess.getstatusoutput('tar -tf '+self.tar_file_path)[1].split('\n')  # tarファイル内ファイル名リスト
                ggis_name = [s for s in filelist if 'Ggis1km' in s]  # ファイル名を取得
                if ggis_name:  # リストが空でなければTrueを返す
                    ggis_name = ggis_name[0]
                    subprocess.run(['tar', '-C', self.bin_path_year, '-xvf', self.tar_file_path, ggis_name]) # tarファイルから/binに取り出す
                    subprocess.run(['rm', self.tar_file_path])  # tarファイルは不要なので削除
                    self.out_available(1)
                else:
                    self.out_error_URL('tarfile', 'no file')
                        
    def out_error_URL(self, error_type, error_detail):
        print(error_type+': '+self.URL)
        with open(self.bin_path+'/error_URL_'+self.timestamp[:4]+'.csv', 'a', encoding="utf_8_sig") as f:
            f.write(error_type+','+str(error_detail)+','+self.URL+'\n')
        self.out_available(0)
    
    def out_available(self, n):  # 1なら存在する，0なら存在しない
        with open(self.bin_path+'/available_'+self.timestamp[:4]+'.csv', 'a', encoding="utf_8_sig") as f:
            f.write(self.timestamp+','+str(n)+'\n')

if __name__ == '__main__':
    # 設定読み込み
    inifile = configparser.ConfigParser()
    inifile.read('./downloader_config.ini', 'UTF-8')

    start = inifile.get('period', 'start')
    end = inifile.get('period', 'end')
    num = inifile.get('interval', 'num')
    timescale = inifile.get('interval', 'timescale')
    tar_path = inifile.get('path', 'tar_path')
    bin_path = inifile.get('path', 'bin_path')

    dt = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M:%S')
    dt_limit = datetime.datetime.strptime(end, '%Y/%m/%d %H:%M:%S')
    
    # インスタンスを作成しダウンロード開始
    downloader = Downloader(tar_path, bin_path)
    while dt < dt_limit:
        downloader.set_date(dt)
        downloader.get_bin_file()
        dt = dt + eval('datetime.timedelta(' + timescale + '=' + num + ')')