#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}

use warnings;
use strict;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/boardskin.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setplugin.cgi";

$query = new LBCGI;

@params = $query->param;
foreach (@params) {
    $theparam = $query->param($_);
    $theparam =~ s/\\/\\\\/g;
    $theparam =~ s/\@/\\\@/g;
    $theparam = &unHTML("$theparam");
    ${$_} = $theparam;
    if ($_ ne 'action') {
        $printme .= "\$" . "$_ = \"$theparam\"\;\n";
    }
}

$inmembername = cookie("adminname");
$inpassword = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

&getmember("$inmembername", "no");

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {


    if ($action eq "process") {

        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/boardskin.cgi";

        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);

        if (-e $filetomake && -w $filetomake) {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛插件设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333 ><center><b>所有的信息已经保存</b><br><br>
                </center>~;
            $printme =~ s/\n/\<br>/g;
            $printme =~ s/\"//g;
            $printme =~ s/\$//g;
            $printme =~ s/\\\@/\@/g;
            $printme =~ s/1\;//g;
            print $printme;

            print qq~
                </td></tr></table></td></tr></table>
                ~;
            require "${lbdir}data/boardskin.cgi";
            require "${lbdir}addplugin.pl";
            open(FILE, ">${lbdir}data/skincache.pl");
            $pluginadd =~ s/\\/\\\\/isg;
            $loggedinas =~ s/\\/\\\\/isg;
            $pluginadd =~ s/~/\\\~/isg;
            $loggedinas =~ s/~/\\\~/isg;
            $pluginadd =~ s/\$/\\\$/isg;
            $loggedinas =~ s/\@/\\\@/isg;
            $pluginadd =~ s/\$/\\\$/isg;
            $loggedinas =~ s/\@/\\\@/isg;
            print FILE qq(\$pluginadd = qq~$pluginadd~;\n);
            print FILE qq(\$loggedinas .= qq~$loggedinas~;\n);
            print FILE "1;\n";
            close(FILE);

        }
        else {
            print qq~
                    <tr><td bgcolor=#2159C9" colspan=2><font face=宋体  color=#FFFFFF>
                    <b>欢迎来到 LeoBBS 论坛管理中心</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    </td></tr></table></td></tr></table>
                    ~;
        }

    }
    else {
        $inmembername =~ s/\_/ /g;

        print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛插件设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333 ><b>论坛插件设定</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
            
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000 ><b><center>LeoBBS 论坛插件设定</center></b><br>
                <font face=宋体 color=#333333 >你可以增加和删除论坛的一些附加插件，方便论坛升级，提高论坛娱乐性！
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 1 </a></b><br>论坛插件 1 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin1name" value="$plugin1name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 1 URL</b><br>论坛插件1的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin1url" value="$plugin1url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 2 </a></b><br>论坛插件 2 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin2name" value="$plugin2name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 2 URL</b><br>论坛插件2的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin2url" value="$plugin2url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 3 </a></b><br>论坛插件 3 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin3name" value="$plugin3name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 3 URL</b><br>论坛插件3的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin3url" value="$plugin3url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 4 </a></b><br>论坛插件 4 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin4name" value="$plugin4name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 4 URL</b><br>论坛插件4的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin4url" value="$plugin4url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 5 </a></b><br>论坛插件 5 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin5name" value="$plugin5name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 5 URL</b><br>论坛插件5的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin5url" value="$plugin5url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 6 </a></b><br>论坛插件 6 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin6name" value="$plugin6name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 6 URL</b><br>论坛插件6的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin6url" value="$plugin6url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 7 </a></b><br>论坛插件 7 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin7name" value="$plugin7name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 7 URL</b><br>论坛插件7的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin7url" value="$plugin7url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 8 </a></b><br>论坛插件 8 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin8name" value="$plugin8name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 8 URL</b><br>论坛插件8的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin8url" value="$plugin8url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 9 </a></b><br>论坛插件 9 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin9name" value="$plugin9name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 9 URL</b><br>论坛插件9的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin9url" value="$plugin9url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 10 </a></b><br>论坛插件 10 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin10name" value="$plugin10name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 10 URL</b><br>论坛插件10的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin10url" value="$plugin10url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 11 </a></b><br>论坛插件 11 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin11name" value="$plugin11name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 11 URL</b><br>论坛插件11的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin11url" value="$plugin11url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 12 </a></b><br>论坛插件 12 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin12name" value="$plugin12name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 12 URL</b><br>论坛插件12的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin12url" value="$plugin12url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 13 </a></b><br>论坛插件 13 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin13name" value="$plugin13name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 13 URL</b><br>论坛插件13的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin13url" value="$plugin13url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 14 </a></b><br>论坛插件 14 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin14name" value="$plugin14name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 14 URL</b><br>论坛插件14的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin14url" value="$plugin14url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 15 </a></b><br>论坛插件 15 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin15name" value="$plugin15name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 15 URL</b><br>论坛插件15的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin15url" value="$plugin15url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 16 </a></b><br>论坛插件 16 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin16name" value="$plugin16name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 16 URL</b><br>论坛插件16的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin16url" value="$plugin16url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 17 </a></b><br>论坛插件 17 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin17name" value="$plugin17name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 17 URL</b><br>论坛插件17的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin17url" value="$plugin17url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 18 </a></b><br>论坛插件 18 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin18name" value="$plugin18name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 18 URL</b><br>论坛插件18的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin18url" value="$plugin18url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 19 </a></b><br>论坛插件 19 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin19name" value="$plugin19name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 19 URL</b><br>论坛插件19的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin19url" value="$plugin19url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 20 </a></b><br>论坛插件 20 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin20name" value="$plugin20name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 20 URL</b><br>论坛插件10的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin20url" value="$plugin20url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 21 </a></b><br>论坛插件 21 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin21name" value="$plugin21name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 21 URL</b><br>论坛插件21的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin21url" value="$plugin21url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 22 </a></b><br>论坛插件 22 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin22name" value="$plugin22name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 22 URL</b><br>论坛插件22的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin22url" value="$plugin22url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 23 </a></b><br>论坛插件 23 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin23name" value="$plugin23name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 23 URL</b><br>论坛插件23的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin23url" value="$plugin23url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 24 </a></b><br>论坛插件 24 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin24name" value="$plugin24name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 24 URL</b><br>论坛插件24的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin24url" value="$plugin24url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 25 </a></b><br>论坛插件 25 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin25name" value="$plugin25name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 25 URL</b><br>论坛插件25的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin25url" value="$plugin25url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 26 </a></b><br>论坛插件 26 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin26name" value="$plugin26name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 26 URL</b><br>论坛插件26的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin26url" value="$plugin26url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 27 </a></b><br>论坛插件 27 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin27name" value="$plugin27name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 27 URL</b><br>论坛插件27的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin27url" value="$plugin27url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 28 </a></b><br>论坛插件 28 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin28name" value="$plugin28name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 28 URL</b><br>论坛插件28的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin28url" value="$plugin28url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 29 </a></b><br>论坛插件 29 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin29name" value="$plugin29name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 29 URL</b><br>论坛插件29的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin29url" value="$plugin29url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 30 </a></b><br>论坛插件 30 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin30name" value="$plugin30name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 30 URL</b><br>论坛插件30的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin30url" value="$plugin30url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 31 </a></b><br>论坛插件 31 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin31name" value="$plugin31name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 31 URL</b><br>论坛插件31的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin31url" value="$plugin31url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 32 </a></b><br>论坛插件 32 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin32name" value="$plugin32name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 32 URL</b><br>论坛插件32的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin32url" value="$plugin32url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 33 </a></b><br>论坛插件 33 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin33name" value="$plugin33name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 33 URL</b><br>论坛插件33的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin33url" value="$plugin33url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 34 </a></b><br>论坛插件 34 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin34name" value="$plugin34name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 34 URL</b><br>论坛插件34的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin34url" value="$plugin34url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 35 </a></b><br>论坛插件 35 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin35name" value="$plugin35name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 35 URL</b><br>论坛插件35的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin35url" value="$plugin35url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 36 </a></b><br>论坛插件 36 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin36name" value="$plugin36name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 36 URL</b><br>论坛插件36的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin36url" value="$plugin36url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 37 </a></b><br>论坛插件 37 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin37name" value="$plugin37name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 37 URL</b><br>论坛插件37的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin37url" value="$plugin37url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 38 </a></b><br>论坛插件 38 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin38name" value="$plugin38name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 38 URL</b><br>论坛插件38的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin38url" value="$plugin38url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 39 </a></b><br>论坛插件 39 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin39name" value="$plugin39name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 39 URL</b><br>论坛插件39的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin39url" value="$plugin39url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 40 </a></b><br>论坛插件 40 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin40name" value="$plugin40name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 40 URL</b><br>论坛插件40的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin40url" value="$plugin40url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 41 </a></b><br>论坛插件 41 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin41name" value="$plugin41name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 41 URL</b><br>论坛插件41的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin41url" value="$plugin41url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 42 </a></b><br>论坛插件 42 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin42name" value="$plugin42name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 42 URL</b><br>论坛插件42的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin42url" value="$plugin42url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 43 </a></b><br>论坛插件 43 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin43name" value="$plugin43name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 43 URL</b><br>论坛插件43的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin43url" value="$plugin43url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 44 </a></b><br>论坛插件 44 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin44name" value="$plugin44name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 44 URL</b><br>论坛插件44的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin44url" value="$plugin44url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 45 </a></b><br>论坛插件 45 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin45name" value="$plugin45name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 45 URL</b><br>论坛插件45的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin45url" value="$plugin45url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 46 </a></b><br>论坛插件 46 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin46name" value="$plugin46name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 46 URL</b><br>论坛插件46的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin46url" value="$plugin46url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 47 </a></b><br>论坛插件 47 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin47name" value="$plugin47name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 47 URL</b><br>论坛插件47的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin47url" value="$plugin47url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 48 </a></b><br>论坛插件 48 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin48name" value="$plugin48name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 48 URL</b><br>论坛插件48的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin48url" value="$plugin48url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 49 </a></b><br>论坛插件 49 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin49name" value="$plugin49name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 49 URL</b><br>论坛插件49的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin49url" value="$plugin49url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 50 </a></b><br>论坛插件 50 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin50name" value="$plugin50name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 50 URL</b><br>论坛插件50的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin50url" value="$plugin50url"></td>
                </tr>      

               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提交"></form></td></tr></table></td></tr></table>
               
               ~;

    }
}
else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

