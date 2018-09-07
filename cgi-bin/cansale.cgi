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

use strict;
use warnings;
use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "cansale.cgi";

$query = new LBCGI;

$userarray     = $query -> param('userarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
            
if ($action eq "process") {
    &getmember("$inmembername","no");
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

	$userarray .= "\n";
	$userarray =~ s/\t//isg;
	$userarray =~ s/\r\n/\n/ig;
	$userarray =~ s/\n+/\n/ig;
	$userarray =~ s/\n/\t/isg;
        $userarray =~ s/\*\[\]\(\)\?\+\=\|//isg;

        @saveduserarray = split(/\t/,$userarray);
        
        $filetomake = "$lbdir" . "data/cansalelist.cgi";
        open (FILE, ">$filetomake");
        $saletype = $query -> param('saletype');
	print FILE $saletype . "\t" . $userarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                
		print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
                );
if ($saletype eq 0) { print qq~<b>你已经保留了下列用户名，只有这些用户才能出售帖子。</b><br><br>~; }
else { print qq~<b>你已经保留了下列用户名，这些用户不允许出售帖子。</b><br><br>~;  }
                foreach $user(@saveduserarray) {
                    chomp $user;
                    print qq($user<br>);
                }
                print qq(<br><br><br><center><a href="cansale.cgi">保留更多可以出售帖子的用户名</a></center>);
	}
        else {
		print qq(
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF align=center colspan=2>
                    <font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    </td></tr></table></td></tr></table>
                );
	}
    }
    else {
        &adminlogin;
    }

}
else {
        
        &getmember("$inmembername","no");
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
		$badusers = "";
                $filetoopen = "$lbdir" . "data/cansalelist.cgi";
                open (FILE, "$filetoopen");
                $badusers = <FILE>;
                close (FILE);

$saletypehtml = qq~
<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
列表名单为： <input name="saletype" type="radio" value="0"> 允许买卖 <input name="saletype" type="radio" value="1"> 不允许买卖<br><br>
</td>
</tr>~;
$saletype = 0;
$saletype = $1, $badusers =~ s/^[01]\t// if ($badusers =~ /^([01])\t/);
$saletypehtml =~ s/(value="$saletype")/$1 checked/;

                $badusers =~ s/\t/\n/g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 保留可以出售帖子的用户名</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>保留可以出售帖子的用户名</b>
                </td></tr>
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
		$saletypehtml                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#000000>
                <b>请注意：</b> 此功能是用来保留一些可以出售帖子的用户名。
                <BR><BR>输入的时候，每行输入一个保留的用户名即可。<BR><BR>
                如果需要设置允许所有的用户都可以进行帖子买卖，那么请保持内容空白即可。<BR><BR>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF align=center colspan=2>
                <textarea cols=60 rows=10 wrap="virtual" name="userarray">$badusers</textarea><BR><BR>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <input type=submit name=submit value="提 交"></td></form></tr></table></td></tr></table>
                );
                
	}
	else {
	    &adminlogin;
	}
}
print qq~</td></tr></table></body></html>~;
exit;
