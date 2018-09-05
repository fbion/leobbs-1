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
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
use Socket;

$LBCGI::POST_MAX=50000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;             
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "vercheck.cgi";

$query = new LBCGI;

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$action       = $query -> param('action');

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
            
    if ($action eq "process") {
	$versionnumbertemp = $versionnumber;
        $versionnumbertemp =~ s/\<(.+?)\>//isg;
	$out=&lbagent("www.leobbs.com","download/reg.cgi","ver=$versionnumbertemp&url=$boardurl");

        ($lastver, $finishfunc, $downtime, $nowdownloadver, $nowfunc,     $downloadtimes, $formtime, $gburl, $bigurl, $engurl, $temp ) = split(/\t/,$out);
        #最新版本  最新功能  估计提供时间  目前可以下载版本  已经完成功能  下载次数        开始时间   

($gburl1,$gburl1show,$gburl2,$gburl2show,$gburl3,$gburl3show,$gburl4,$gburl4show,$gburl5,$gburl5show) = split(/\|/,$gburl);
$gbdownloadinfo = "";
if ($gburl1 ne "") {
    if ($gburl1show eq "") { $gburl1show = "按这里进行下载"; }
    $gbdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb1 onClick='return gbconfirm();' title="按这里进行下载"><B>$gburl1show</B></a>~;
}
if ($gburl2 ne "") {
    if ($gburl2show eq "") { $gburl1show = "按这里进行下载"; }
    $gbdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb2 onClick='return gbconfirm();' title="按这里进行下载"><B>$gburl2show</B></a>~;
}
if ($gburl3 ne "") {
    if ($gburl3show eq "") { $gburl1show = "按这里进行下载"; }
    $gbdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb3 onClick='return gbconfirm();' title="按这里进行下载"><B>$gburl3show</B></a>~;
}
if ($gburl4 ne "") {
    if ($gburl4show eq "") { $gburl1show = "按这里进行下载"; }
    $gbdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb4 onClick='return gbconfirm();' title="按这里进行下载"><B>$gburl4show</B></a>~;
}
if ($gburl5 ne "") {
    if ($gburl5show eq "") { $gburl1show = "按这里进行下载"; }
    $gbdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb5 onClick='return gbconfirm();' title="按这里进行下载"><B>$gburl5show</B></a>~;
}

($bigurl1,$bigurl1show,$bigurl2,$bigurl2show,$bigurl3,$bigurl3show,$bigurl4,$bigurl4show,$bigurl5,$bigurl5show) = split(/\|/,$bigurl);
$bigdownloadinfo = "";
if ($bigurl1 ne "") {
    if ($bigurl1show eq "") { $bigurl1show = "按这里进行下载"; }
    $bigdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big1 onClick='return bigconfirm();' title="按这里进行下载"><B>$bigurl1show</B></a>~;
}
if ($bigurl2 ne "") {
    if ($bigurl2show eq "") { $bigurl1show = "按这里进行下载"; }
    $bigdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big2 onClick='return bigconfirm();' title="按这里进行下载"><B>$bigurl2show</B></a>~;
}
if ($bigurl3 ne "") {
    if ($bigurl3show eq "") { $bigurl1show = "按这里进行下载"; }
    $bigdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big3 onClick='return bigconfirm();' title="按这里进行下载"><B>$bigurl3show</B></a>~;
}
if ($bigurl4 ne "") {
    if ($bigurl4show eq "") { $bigurl1show = "按这里进行下载"; }
    $bigdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big4 onClick='return bigconfirm();' title="按这里进行下载"><B>$bigurl4show</B></a>~;
}
if ($bigurl5 ne "") {
    if ($bigurl5show eq "") { $bigurl1show = "按这里进行下载"; }
    $bigdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big5 onClick='return bigconfirm();' title="按这里进行下载"><B>$bigurl5show</B></a>~;
}

($engurl1,$engurl1show,$engurl2,$engurl2show,$engurl3,$engurl3show,$engurl4,$engurl4show,$engurl5,$engurl5show) = split(/\|/,$engurl);
$engdownloadinfo = "";
if ($engurl1 ne "") {
    if ($engurl1show eq "") { $engurl1show = "按这里进行下载"; }
    $engdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng1 onClick='return engconfirm();' title="按这里进行下载"><B>$engurl1show</B></a>~;
}
if ($engurl2 ne "") {
    if ($engurl2show eq "") { $engurl1show = "按这里进行下载"; }
    $engdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng2 onClick='return engconfirm();' title="按这里进行下载"><B>$engurl2show</B></a>~;
}
if ($engurl3 ne "") {
    if ($engurl3show eq "") { $engurl1show = "按这里进行下载"; }
    $engdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng3 onClick='return engconfirm();' title="按这里进行下载"><B>$engurl3show</B></a>~;
}
if ($engurl4 ne "") {
    if ($engurl4show eq "") { $engurl1show = "按这里进行下载"; }
    $engdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng4 onClick='return engconfirm();' title="按这里进行下载"><B>$engurl4show</B></a>~;
}
if ($engurl5 ne "") {
    if ($engurl5show eq "") { $engurl1show = "按这里进行下载"; }
    $engdownloadinfo .= qq~　<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng5 onClick='return engconfirm();' title="按这里进行下载"><B>$engurl5show</B></a>~;
}

#$lastver="<b>L<font color=#F26522>eo</font>B<font color=#00AEEF>BS</font></b> X Build040101";
#$finishfunc="1. 123<BR>2.123";
#$downtime="2004/01/07";
#$nowdownloadver="<b>L<font color=#F26522>eo</font>B<font color=#00AEEF>BS</font></b> X Build040101";
#$nowfunc="1. 2222<BR>2.3123";
#$downloadtimes="500";
#$formtime="2003/01/01";
#$gburl="http://111";
#$big5url="";
#$engurl="";
	
	if ($lastver eq "-1") {
	    print qq~
              <tr><td bgcolor=#2159C9" colspan=2><font face=宋体  color=#FFFFFF>
              <b>欢迎来到 LeoBBS 论坛管理中心/查看论坛版本更新</b>
              </td></tr>
              <tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
              <font color=#333333><b>$finishfunc</b><BR><BR>请直接访问 <a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a> 查看更新情况吧 ！
              </td></tr></table></td></tr></table>
            ~;
            exit;
	}

	if (($lastver ne "")&&($formtime ne "")&&($downtime ne "")) {
	    print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 查看论坛版本更新</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2><br><br>
            ~;
            $versionnumbertemp = $versionnumber;
            $versionnumbertemp =~ s/\<(.+?)\>//isg;
            if ($versionnumbertemp =~/LeoBBS/g) {
                $myver = $versionnumbertemp;
                $myver =~ s/LeoBBS X Build//isg;
                $myver =~ s/(.*)Build//isg;
                $myver =~ s/(.*)v//isg;

                $newver = $nowdownloadver;
            	$newver =~ s/\<(.+?)\>//isg;
                $newver =~ s/LeoBBS X Build//isg;
                $newver =~ s/(.*)Build//isg;
                $newver =~ s/(.*)v//isg;

                my $gengxin="";
                if ($myver >= $newver) {
                    print qq~<font face=宋体 color=#333333><center><b>您现在使用的是最新版本，感谢您使用雷傲极酷超级论坛 ！</b><br><br><br>~;
                    $gengxin="您无需升级";
                } else {
		    print qq~<font face=宋体 color=#333333><center><b>当前 $nowdownloadver 已经提供下载，如果您需要升级，请参看下面的连接 ！</b><br><br><br>~;
                    $gengxin="您需要升级";
               }
#               if ($big5url eq "") { $big5url = "没有"; } else { $big5url = qq~<a href=$big5url>$big5url</a>~; }
#               if ($engurl  eq "") { $engurl = "没有";  } else { $engurl  = qq~<a href=$engurl>$engurl</a>~;   }

               print qq~
               <table width=75%><tr><td>当前最新版本: $lastver  [ 你当前使用版本: $versionnumber]<br><hr>
               <img src=$imagesurl/icon/txt.gif width=16 height=16 border=0> <font color=blue>已完成功能:</font> （估计提供下载时间: <B>$downtime</b> ）<br><br>
               $finishfunc<br>
               <hr>
               </td></tr>
               <tr><td><br><br>当前可提供下载的最新版本: <B>$nowdownloadver</b>　 [<font color=red><B>$gengxin</B></font>]<br><hr>
               <img src=$imagesurl/icon/txt.gif width=16 height=16 border=0> <font color=red>新增功能列表:</font><br><br>
               $nowfunc<br><br><br>
               <hr>
               <img src=$imagesurl/icon/txt.gif width=16 height=16 border=0> <b>下载地址:<br>
               ~;
               if ($gbdownloadinfo ne "") {
                   print qq~<B>[简体版本]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>$gbdownloadinfo<br>~;
               } else {
                   print qq~<B>[简体版本]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>　暂时不提供<br>~;
               }
               if ($bigdownloadinfo ne "") {
               	   print qq~<B>[繁体版本]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>$bigdownloadinfo<br>~;
               } else {
               	   print qq~<B>[繁体版本]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>　暂时不提供<br>~;
               }
               if ($engdownloadinfo ne "") {
               	   print qq~<B>[英文版本]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>$engdownloadinfo<br>~;
               } else {
               	   print qq~<B>[英文版本]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>　暂时不提供<br>~;
               }
               print qq~
               <hr><br>
               <b>自 $formtime 以来，已经有 <b><font color=blue>$downloadtimes</font></b> 个网站安装了本论坛！</b>
               <hr>
               </td></tr></table>
               ~;
	    } else {
                print qq~
                <font face=宋体 color=#333333><center><b>你非法修改版本号，请及时改回连接和版本标示，谢谢合作！</b><br><br>
                ~;
	    }
            print qq~
            </center>
            </td></tr></table></td></tr></table>
            ~;
	}
	else {
	    print qq~
              <tr><td bgcolor=#2159C9" colspan=2><font face=宋体  color=#FFFFFF>
              <b>欢迎来到 LeoBBS 论坛管理中心/查看论坛版本更新</b>
              </td></tr>
              <tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
              <font color=#333333><b>无法获取版本信息</b><br>Socket 模块不能正常使用，可能是服务器的防火墙不允许，或者 LeoBBS 服务器在调整。<BR>请访问 <a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a> 查看更新情况吧 ！
              </td></tr></table></td></tr></table>
            ~;
	}
    }
    else {
	$versionnumbertemp = $versionnumber;
        $versionnumbertemp =~ s/\<(.+?)\>//isg;
        if ($versionnumbertemp =~/LeoBBS/g) {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛版本检查</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333 ><b>论坛版本检查</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                
                <font face=宋体 color=#990000 ><b><center>LeoBBS 论坛管理中心 / 论坛版本检查</center></b><br>
                <font face=宋体 color=#333333 >你可以查看当前 LeoBBS 站点论坛的版本情况，<br>知道当前最新版本和是否增加了有用的功能，是否适合你升级！<br><br>
                本程序没有危害性，而且我们特意没有采用加密方式传送，<br>仅仅是为了让大家获得最新版本的情况，谢谢你采用雷傲超级论坛！
                
                </td>
                </tr>
                              
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="检查版本更新情况"></form></td></tr></table></td></tr></table>
               ~;
	} else {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛版本检查</b>
                </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333 ><center><b>你非法修改版本号，请及时改回连接和版本标示，谢谢合作！</b><br><br>
                    </td></tr></table></td></tr></table>
                ~;
       }
    }

} else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

sub lbagent {
    eval("use Socket;");
    ($host,$path,$content) = @_;
    $host =~ s/^http:\/\///isg;
    $port = 80;
    $path = "/$path" if ($path !~ /^\//);
    my ($name, $aliases, $type, $len, @thataddr, $a, $b, $c, $d, $that);
    my ($name, $aliases, $type, $len, @thataddr) = gethostbyname($host);
    my ($a, $b, $c, $d) = unpack("C4", $thataddr[0]);
    my $that = pack('S n C4 x8', 2, $port, $a, $b, $c, $d);
    return unless (socket(S, 2, 1, 0));
    select(S);
    $| = 1;
    select(STDOUT);
    return unless (connect(S, $that));
    print S "POST http://$host/$path HTTP/1.0\n";
    print S "Content-type: application/x-www-form-urlencoded\n";
    my $contentLength = length $content;
    print S "Content-length: $contentLength\n";
    print S "\n";
    print S "$content";
    @results = <S>;
    close(S);
    undef $|;
    my $result = join("", @results);
    @results = split("\r\n\r\n", $result);
    @results = split("\n\n", $result) if (@results == 1);
    shift(@results);
    $result = join("", @results);
    return $result;
}
