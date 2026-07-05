# 环境安装
`pip install pandas`
# 项目结构
```
AES
├── README.md
├── hash.py
├── K.csv
└── hash_test.txt
```
# 项目说明
获取文件hash值：运行hash.py
# 参数修改
在hash.py中修改输入文件路径。
# 常见报错
`the size of file must be less than 2^64`  
文件大小必须小于2^64比特。  
`please put the file in %s`  
文件路径错误。
# 使用说明
### hash.py
把待运算文件命名为hash_test.txt，运行mix.py，输出hash值。