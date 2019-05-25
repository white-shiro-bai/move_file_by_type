import os
import hashlib
import shutil
from pymediainfo import MediaInfo
import json
import multiprocessing

srcdir = "d:\\wx\\acountdir" #需要整理的目录
tardir = "d:\\190525微信归档\\账号文件" #整理的目标目录
tread = 8 #需要并发的线程数

def extname(file):
    #调用mediainfo识别无扩展名文件
    media_info = MediaInfo.parse(file)
    data = json.loads(media_info.to_json())
    try:
        filetype = data["tracks"][0]["format"]
        if filetype == 'MPEG-4':
            return ('mp4')
        elif filetype == 'JPEG':
            return ('jpg')
        else:
            return(filetype)
    except:
        return('无法识别的文件')


def all_path(dirname):
    #拿到目录下的所有文件
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)
    return result


def GetFileMd5(filename):
    #为每个文件生成MD5
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def movefile(srcfile,dstfile):
    #移动文件
    if not os.path.isfile(srcfile):
        print (srcfile+" not exist!")
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print ("move" + srcfile + "->" + dstfile)

def do_files(file):
    dirname,filename=os.path.split(file)
    ext = os.path.splitext(filename)
    name,type=ext
    #解出目录，文件名和扩展名
    if type == '':
        #如果没有扩展名，则执行检测文件类型
        print ('读取文件：'+file)
        print ('文件名：'+name)
        type2 = extname(file)
        md5 = GetFileMd5(file)
        print ('文件类型:' + type2)
        print ('md5是:' + md5)
        if type2 == '无法识别的文件':
            #如果无法检测出文件类型，则按照无法识别处理，做MD5防止重复和错误覆盖
            targetfile = tardir+'\\'+str(type2)+'\\'+name+'_'+md5
            print('移动文件:'+file+'到'+targetfile)
            movefile(file,targetfile)
            print('----------------------')
        else:
            #如果检测出文件类型，则修改扩展名并按照正常文件处理，做MD5防止重复和错误覆盖
            targetfile = tardir+'\\'+str(type2)+'\\'+name+'_'+md5+'.'+str(type2)
            print('移动文件:'+file+'到'+targetfile)
            movefile(file,targetfile)
            print('----------------------')

    else:
        #如果文件自带扩展名，则不检测，只做MD5防止重复或错误覆盖
        print ('读取文件：'+file)
        print ('文件名：'+name)
        type2 = type.replace('.','')
        md5 = GetFileMd5(file)
        print ('文件类型:' + type2)
        print ('md5是:' + md5)
        targetfile = tardir+'\\'+type2+'\\'+name+'_'+md5+'.'+str(type2)
        print('移动文件:'+file+'到'+targetfile)
        movefile(file,targetfile)
        print('----------------------')

def get_all_file_info():
    #主程序
    files = all_path(srcdir)
    p = multiprocessing.Pool(processes = tread)
    total_count = len(files)
    print ('total_count:'+str(total_count))
    count = 1
    for file in files:
        p.apply_async(do_files,(file,))
        print( str(count) + 'of' + str(total_count) )
        count = count + 1
    p.close()
    p.join()


if __name__ == '__main__':
    get_all_file_info()
