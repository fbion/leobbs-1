LeoBBS X 雷傲超级论坛说明文档 
雷傲极酷超级论坛 LeoBBS X 说明文档

.

  
**伪静态的实现：**  
  
  
一. APACHE 1.3.x & 2.X  
  
  
  
　　在通常情况下，把 addon 目录下的 .htaccrss 文件复制到你 cgi-bin 下，和 CGI 程序文件放一起，然后直接看第“三”步骤即可！如果第三步骤测试不成功，那么请按照下面的步骤手工设置！  
  
  
　　1. 打开 apache/conf/httpd.conf 文件，搜索到以下两行，把这两行最前面的 # 去掉(如果第二行的内容找不到，就略过)。  
  
#LoadModule rewrite\_module modules/mod\_rewrite.so  
#AddModule mod\_rewrite.c  
  
  
　　2. 继续搜索类似下面这样的内容（由于安装路径不同，可能会有差异，请仔细搜索一下）。  
  
<Directory "d:/Apache/htdocs/cgi-bin">  
  
在此行下直接添加下面这行  
  
AddHandler cgi-script .cgi .md .pl  
  
　　然后看接下去的几行，把最后的 None 改成 All，类似下面的样子（对照一下就可以了）。  
  
AllowOverride All  
  
Options All  
  
  
  
  
  
　　3. 在此文件的最后添加下面这段。  
  
RewriteEngine On  
  
RewriteRule ^(.\*)/topic-(\[0-9\]+)-(\[0-9\]+)-(\[0-9\]+)-(\[0-9\]+)-(.\*)\\.md$ $1/topic\\.cgi\\?forum=$2&topic=$3&start=$4&show=$5&replynum=$6  
  
RewriteRule ^(.\*)/leobbs\\.md$ $1/leobbs\\.cgi  
  
RewriteRule ^(.\*)/leobbs-(.+)\\.md$ $1/leobbs\\.cgi?action=$2  
  
RewriteRule ^(.\*)/announcements\\.md$ $1/announcements\\.cgi  
  
RewriteRule ^(.\*)/announcements-(.+)\\.md$ $1/announcements\\.cgi?forum=$2  
  
RewriteRule ^(.\*)/profile-(.\*)\\.md$ $1/profile\\.cgi\\?action=show&member=$2  
  
RewriteRule ^(.\*)/view-(\[0-9\]+)-(\[0-9\]+)\\.md$ $1/view\\.cgi\\?forum=$2&topic=$3  
  
RewriteRule ^(.\*)/forums-(\[0-9\]+)-(\[0-9\]+)\\.md$ $1/forums\\.cgi\\?forum=$2&show=$3  
  
RewriteRule ^(.\*)/printpage-(\[0-9\]+)-(\[0-9\]+)\\.md$ $1/printpage\\.cgi\\?forum=$2&topic=$3  
  
  
  
　　4. 重新启动 Apache 服务，只要没有提示错误，伪静态的服务器端安装就算完成了。  
  
  
  
二. IIS 5.0 & 6.0  
  
  
  
　　1. 将 addon 目录下的 Rewrite.rar 解压缩至目录名 Rewrite 下。  
  
  
  
　　2. 将 Rewrite 目录保存至服务器某路径下。  
  
  
  
　　3. 打开“控制面板”－“管理工具”－“IIS信息服务管理器”－“网站”－“您的站点”－“属性”。  
  
  
  
　　4. 在“ISAPI筛选器”项点击“添加”，筛选器名称填入 Rewrite，可执行文件为 Rewrite 目录下的 Rewrite.dll（通过“浏览”指定绝对地址）。  
  
  
  
　　5. 重启 IIS，只要没有提示错误，伪静态的服务器端安装就算完成了。  
  
  
  
三.　程序中的设置：  
  
  
  
　　光在服务器端设置好伪静态还是不够的，必须在程序中打开伪静态的支持开关，登录雷傲论坛的管理区，在“基本变量设置”的最后，“是否采用伪静态方式”此行后面，点“按此测试”如果能正常看到论坛首页，就说明设置成功，然后此项目选择“使用”，保存即可！如果提示的是“文件没有找到或者404错误”，那就说明设置错误，请重新设置！  
  
  
  
注：如果服务器端没有经过设置，或者“按此测试”的时候没有看到正常的论坛首页，那么千万不要在程序端打开伪静态方式，否则论坛将无法正常使用！  
  
  
  

  
  

* * *

版权所有：[雷傲科技](http://www.leobbs.com) & [雷傲极酷超级论坛](http://bbs.leobbs.com)　　Copyright 2000-2005