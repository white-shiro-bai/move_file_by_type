# move_file_by_type
根据文件的类型把目录和子目录中的所有文件归类。文件类型识别依赖 mediainfo.dll 和 pymediainfo

使用前需要安装 pymediainfo
pip install pymediainfo

把mediainfo.dll拷贝到python.exe所在目录
mediainfo.dll 需要自行安装mediainfo，注意该应用区分x64和x86，需要与python版本对应。

依赖安装完，即可使用
