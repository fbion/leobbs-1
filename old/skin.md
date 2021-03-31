LeoBBS X 雷傲超级论坛说明文档 

雷傲极酷超级论坛 LeoBBS X 说明文档

.

  
**特别声明：**  
　　本论坛为共享软件(shareware)，仅提供给个人网站免费使用，请勿非法修改、转载、散播、或用于其他图利行为，并请勿删除或修改任何版权标示和图标！  
　　一切商业网站和收费网站必须经过注册以后才可以继续使用本论坛，注册后可获得完善的售后服务和升级服务，具体注册相关事项请看：**[商业版注册说明](reg.htm)** 或联系 **[http://www.leobbs.org/](http://www.leobbs.org/)** 。  
　　如果您的页面中添加有 3721 和百度的浏览器控件下载的话，那么请勿使用本论坛，谢谢合作！  
　　当您的网站使用本论坛后，您论坛内容中所涉及的一切法律责任均与雷傲科技无关。  
  
  
**论坛皮肤文件结构说明：**  
　**1.** 以雷傲原始皮肤为例，皮肤文件分为：  
     配色文件                   leobbs.cgi       （在cgi-bin/data/skin中）      
  
     模版文件                   leobbs.cgi       （在cgi-bin/data/template中）  
  
     论坛顶部及导航栏样式文件     leobbs.pl        （在cgi-bin/myskin中）  
  
皮肤图片文件 leobbs（文件夹）  （在non-cgi/images中）

     （#注：因为配色文件**leobbs.cgi**中，$skin="leobbs"，所以其他两个文件和图片文件夹的名字均为**leobbs**）  

　**2.** 以春之舞皮肤为例，皮肤文件分为：  
     配色文件                   春之舞.cgi      （在cgi-bin/data/skin中）      
  
     模版文件                   czw.cgi       （在cgi-bin/data/template中）  
  
     论坛顶部及导航栏样式文件     czw.pl        （在cgi-bin/myskin中）  
  
     皮肤图片文件                czw（文件夹）  （在non-cgi/images中）  
  
     （#注：因为配色文件**春之舞.cgi**中，$skin="czw"，所以其他两个文件和图片文件夹的名字均为**czw**）  
　

**论坛配色文件说明：**

    下面是论坛所使用的色彩变量代码的简单介绍：  

代码：

* * *

`**论坛页首菜单**  
  
菜单带字体颜色                   $menufontcolor  
  
菜单带背景颜色                   $menubackground  
  
菜单带背景图片                   $menubackpic  
  
菜单带边界颜色                   $titleborder  
  
  
  
**字体外观和颜色**  
  
"最后发贴者"字体颜色             $lastpostfontcolor  
  
"加重区"字体颜色                 $fonthighlight  
  
一般用户名称字体颜色             $posternamecolor  
  
一般用户名称上的光晕颜色         $memglow  
  
坛主名称字体颜色                 $adminnamecolor  
  
坛主名称上的光晕颜色             $adminglow  
  
总版主名称字体颜色               $smonamecolor  
  
总版主名称上的光晕颜色           $smoglow  
  
分类区版主名称字体颜色           $cmonamecolor  
  
分类区版主名称上的光晕颜色       $cmoglow  
  
版主名称字体颜色                 $teamnamecolor  
  
版主名称上的光晕颜色             $teamglow  
  
副版主名称字体颜色               $amonamecolor  
  
副版主名称上的光晕颜色           $amoglow  
  
认证用户名称字体颜色             $rznamecolor  
  
认证用户名称上的光晕颜色         $rzglow  
  
过滤和禁言用户名称上的光晕颜色   $banglow  
  
  
  
**所有页面颜色**  
  
主字体颜色一                     $fontcolormisc  
  
主字体颜色二                     $fontcolormisc2  
  
其他背景颜色一                   $miscbackone  
  
其他背景颜色二                   $miscbacktwo  
  
  
  
**表格颜色**  
  
分类带背景颜色                   $catback  
  
标题栏背景图片                   $catbackpic  
  
分类带背景图片                   $catsbackpicinfo  
  
分类带字体颜色                   $catfontcolor  
  
所有表格边界颜色                 $tablebordercolor  
  
所有表格宽度                     $tablewidth  
  
  
  
**导航栏颜色**  
  
导航栏边线颜色                   $navborder  
  
导航栏背景颜色                   $navbackground  
  
导航栏字体颜色                   $navfontcolor  
  
  
  
**标题颜色**  
  
论坛/主题的标题栏背景颜色        $titlecolor  
  
论坛/主题的标题栏字体颜色        $titlefontcolor  
  
  
  
**论坛内容颜色**  
  
内容颜色一                       $forumcolorone  
  
内容颜色二                       $forumcolortwo  
  
内容字体颜色                     $forumfontcolor  
  
  
  
**回复帖子颜色**  
  
回复颜色一                       $postcolorone  
  
回复颜色二                       $postcolortwo  
  
回复字体颜色一                   $postfontcolorone  
  
回复字体颜色二                   $postfontcolortwo`

　  
   下面是举例LB原始风格的配色文件内容：  

代码：

* * *

`$adminglow = '#9898BA';  
$adminnamecolor = '#990000';  
$amoglow = 'pink';  
$amonamecolor = '#8b008b';  
$banglow = '#EE111';  
$catback = '#73A2DE';  
$catbackpic = 'bg.gif';  
$catfontcolor = '#FFFFFF';  
$catsbackpicinfo = 'bg.gif';  
$cmoglow = '#5577AA';  
$cmonamecolor = '#F76809';  
$cssmaker = "雷傲科技";  
$cssname = "LeoBBS";  
$cssurl = "[http://www.leobbs.org/";](http://www.leobbs.org/%22;)  
$fontcolormisc = '#000000';  
$fontcolormisc2 = '#000000';  
$fonthighlight = '#990000';  
$forumcolorone = '#F3F6FA';  
$forumcolortwo = '#FFFFFF';  
$forumfontcolor = '#000000';  
$lastpostfontcolor = '#000000';  
$lbbody = "bgcolor=#ffffff alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0";  
$memglow = '#9898BA';  
$menubackground = '#F3F6FA';  
$menubackground1 = '#F3F6FA';  
$menubackpic = 'cdbg.gif';  
$menufontcolor = '#000000';  
$miscbackone = '#FFFFFF';  
$miscbacktwo = '#F3F6FA';  
$navbackground = '#F7F7F7';  
$navborder = '#E6E6E6';  
$navfontcolor = '#4D76B3';  
$postcolorone = '#F3F6FA';  
$postcolortwo = '#FFFFFF';  
$posternamecolor = '#000066';  
$posternamefont = '宋体';  
$postfontcolorone = '#000000';  
$postfontcolortwo = '#000000';  
$rzglow = '#778877';  
$rznamecolor = '#55AA66';  
$skin = "leobbs";  
$smoglow = '#9898BA';  
$smonamecolor = '#990000';  
$tablebordercolor = '#4D76B3';  
$tablewidth = '97%';  
$teamglow = '#cccccc';  
$teamnamecolor = '#0000ff';  
$titleborder = '#4D76B3';  
$titlecolor = '#73A2DE';  
$titlefontcolor = '#ffffff';  
1;`

**论坛模板文件说明：**  

    就拿最基本的摸版leobbs风格摸版来说  

代码：

* * *

`<html>  
<head>  
<title>$page_title</title>  
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">  
<meta name=keywords content="雷傲,论坛,异灵,cgi,leobbs,leoboard,LB5000,bbs,leo,perl,lb,lbplus">  
$coolmeta  
<script language="javascript" type="text/javascript" SRC="$imagesurl/board.js"></SCRIPT>  
$coolclick  
<!--end Java-->  
  
<!--css info(editable)-->  
<style>  
A:visited{TEXT-DECORATION: none}  
A:active{TEXT-DECORATION: none}  
A:hover{TEXT-DECORATION: underline overline}  
A:link{text-decoration: none;}  
.t{LINE-HEIGHT: 1.4}  
BODY{FONT-FAMILY: 宋体; FONT-SIZE: 9pt;}  
caption,TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: 宋体; FONT-SIZE: 9pt}  
INPUT{FONT-SIZE: 9pt;}  
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: 宋体; font-size: 9pt; font-style: bold;}  
</style>  
<!--end css info-->  
</head>  
<link href="$imagesurl/leobbs.ico" rel="SHORTCUT ICON">  
<body $lbbody>  
<div id="popmenu" class="menuskin" onMouseover="clearhidemenu();highlightmenu(event,'on')" onMouseout="highlightmenu(event,'off');dynamichide(event)"></div>  
<SCRIPT>  
<!--  
function valigntop(){}  
function valignend(){}  
-->  
</SCRIPT>  
$lbboard_main  
</body>  
</html>`

  
  
  
其中：  
A:hover{TEXT-DECORATION: underline overline}   是关于鼠标的修改 （underline overline的意思就是下划线和上划线，就是当鼠标移动到超连接上的时候的样子）  
  
举个例子：  
MacOS皮肤的鼠标设定是当指向超连接的时候为十字形~并有虚下划线和凹进去的样子，代码为：  
A:hover { LEFT: 1px;  POSITION: relative; TOP: 1px; CURSOR: crosshair;BORDER-BOTTOM: #808080 1px dotted A:hover ;}  
更多特效可以在网上搜集  
  
  
最重要的就是这个部分  
<SCRIPT>  
<!--  
function valigntop(){}  
function valignend(){}  
\-->  
</SCRIPT>  
为论坛所有表格的上美化边框和下美化边框的JS调用代码，  
因为leobbs风格里没有这两部分美化边框，所以代码是空的。

如果有上下美化图片  
就用Macos苹果风格为例子  
<SCRIPT>  
<!--  
function valigntitle(){  
document.write("<table width=95% border=0 cellpadding=0 cellspacing=0 align=center>")  
}  
function valigntop(){  
document.write("<SCRIPT>valigntitle()</SCRIPT><tr><td><img src=$imagesurl/macos/top\_1.gif></td><td background=$imagesurl/macos/top\_2.gif width=100% align=center></td><td><img src=$imagesurl/macos/top\_3.gif></td></tr></table>")  
}  
function valignend(){  
document.write("<SCRIPT>valigntitle()</SCRIPT><tr><td><img src=$imagesurl/macos/end\_1.gif></td><td background=$imagesurl/macos/end\_2.gif width=100% align=center></td><td><img src=$imagesurl/macos/end\_3.gif></td></tr></table>")  
}  
\-->  
</SCRIPT>  
  
所以大家做皮肤的时候如果有上下美化边框的话，只需要按照这个图片名字然后设定自己要设定的路径就可以了， 具体更多方法可以通过了解相关HTML代码来学习。

需要注意的是，与论坛其他文件不同，在模版文件中，$imagesurl指代non-cgi/images  
  
  
最后  
lbboard\_main  
就是指代论坛的主体部分了， 你可以在这里的上方和下方加入论坛顶部和底部的图片。  
所以如果你想在论坛的顶部增加图片的话，只要不涉及到顶部导航栏，直接加在这个代码的上面就可以。  
如果涉及顶部菜单栏样式，则需要在顶部样式文件中修改。  
  
以Macos苹果风格为例子  
就可以在这个上面加入，就是顶部图片了。  
  
　

代码：

* * *

`<table width=95% border="0" cellspacing="0" cellpadding="0" align="center"><tr><td width=131><img src=$imagesurl/macos/toplogo.jpg></td><td background=$imagesurl/macos/toplogobg.jpg width=100%></td><td width=131><img src=$imagesurl/macos/toplogo2.jpg></td></tr></table>  
<table width=95% border="0" cellspacing="0" cellpadding="0" align="center"><tr><td width=131><img src=$imagesurl/macos/1.gif></td><td background=$imagesurl/macos/2.gif width=100%></td><td width=131><img src=$imagesurl/macos/3.gif></td></tr></table>`

  
  
  
或者加入到cgi-bin/myskin下的相对应的皮肤的顶部pl文件里也一样,但需要加输出，格式为$output .= qq~你要编辑的在页面上显示出来的内容~;  
  
  
**下面是搜集来的CCS常用代码介绍：**  
  
A:link,A:active,A:visited{  
TEXT-DECORATION:none ;  
Color:#000000  
}  
  
A:hover{  
TEXT-DECORATION: underline;  
Color:#4455aa  
}  
  
上面这指的是鼠标在对链接文字进行操作、操作后和操作时所产生的效果  
A属性  
link：文字连接的默认颜色、效果等  
active：点击时产生的效果  
visited：点击后的效果  
hover：鼠标悬停在链接上时所产生的效果  
  
Decoration属性  
none：无效果  
underline：下划线效果  
  
大家可以根据这两种常用属性来配出喜欢的链接文字效果。  
  
  
BODY{  
FONT-SIZE: 11.5px;  
COLOR: #000000;  
FONT-FAMILY: Verdana,宋体;  
scrollbar-face-color: #DEE3E7;  
scrollbar-highlight-color: #FFFFFF;  
scrollbar-shadow-color: #DEE3E7;  
scrollbar-3dlight-color: #D1D7DC;  
scrollbar-arrow-color:  #006699;  
scrollbar-track-color: #EFEFEF;  
scrollbar-darkshadow-color: #98AAB1;  
}  
  
body：指HTML内<body>标签的属性  
  
font-size：字体大小，单位分为px（象素）和pt（磅），一般我们常用的是象素尺寸为12px或者11.5px，磅的大小为9pt或者8pt，两种单位最终显示的大小都是一样的，用哪种单位就看个人习惯了。  
  
color：默认情况下是字体颜色，颜色大家可以使用RGB颜色，也可以使用16位颜色代码。推荐使用16位颜色代码。  
  
FONT-FAMILY：字体样式，大家会经常看到在font-family设置里一下出现3种字体（例：FONT-FAMILY: Verdana,Tahoma,宋体），一般前两种为英文字体，最后的是中文字体。英文字体设置两种是为了防止如果客户端没有第一种字体，马上使用第二组英文字体。大多数情况下，中文操作系统中都会支持宋体，所以我们也就不必要再设置第二种中文字体了。  
  
scrollbar：指滚动条  
scrollbar-face-color：表面颜色  
scrollbar-highlight-color：高亮区颜色  
scrollbar-shadow-color：阴影颜色  
scrollbar-3dlight-color：3D颜色  
scrollbar-arrow-color：箭头颜色  
scrollbar-track-color：轨道颜色（滚动条底色）  
scrollbar-darkshadow-color：深阴影颜色  
IE5.5以后的版本都会支持这种自定义滚动条的效果。

**论坛顶部样式文件说明：**

关于顶部文件的概述  
  
在cgi-bin/myskin下的pl文件  
为这个皮肤所对应的顶部文件  
  
是专门为适应特殊顶部页眉而分离出来的文件  
  
如果你要做特殊样式的论坛顶部样式  
就需要在这里进行编辑了  
里面一共有三个变量组成  
$daohang 导航栏内容  
$yemei 顶部页眉内容  
$firstout 设定显示顺序，如果先显示页眉内容的话，这个变量值为 "yemei"，如果先显示导航栏的话，这个变量值为 "daohang"  
  
  
但注意需要显示在页面上的内容，必须按照这个格式加输出命令  
$yemei = qq~你要编辑的在页面上显示出来的页眉内容HTML网页代码~;  
$daohang = qq~你要编辑的在页面上显示出来的导航栏内容HTML网页代码~;  
需要你了解大量HTML编程，具体可以参考我已经发布的那些特殊样式的皮肤的顶部文件，也可以在原有基础上修改。  
  
基本的小知识是  
┌──────┐  
└──────┘  
上面的就是 <tr> </tr>  
而  
┌──┬──┐  
└──┴──┘  
就是  
<tr>  
<td> </td>  
</tr>    
  
更多的可以在很多网页教程里看到，而且意思也比较容易看明白，也可以参照已经发布的皮肤去修改。

  
**论坛的其他说明文档联接：**  
[论坛属性设置完整说明](filemod.htm)  
[论坛数据转换说明](convert.htm)  
[论坛用户库结构和修改方法](userformat.htm)  
[论坛功能列表](function.htm)  
[LeoBBBS X 论坛皮肤制作说明](skin.htm)  
[制作 BitTorrent 下载区的说明](bittorrent.htm)  
[论坛安全手册](safe.htm)  
[LeoBBBS X 论坛商业版注册说明](reg.htm)  
[雷傲论坛插件和雷傲论坛商业插件版说明](plug.htm)  
[LeoBBBS X 论坛虚拟主机选购说明](vhost.htm)  
  
  
  
**开发团队技术演示及支持论坛：**  
**[雷傲极酷超级论坛](http://bbs.leobbs.org/)**  
**[LeoBBS X Develop Team](http://bbs.leobbs.org/cgi-bin/forums.cgi?forum=2)**  
  
  

  
  

* * *

版权所有：[雷傲科技](http://www.leobbs.org) & [雷傲极酷超级论坛](http://bbs.leobbs.org)　　Copyright 2000-2005