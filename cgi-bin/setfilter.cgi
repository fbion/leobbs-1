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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "setfilter.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$userarray     = $query -> param('userarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
            
if ($action eq "process") {
    &getmember("$inmembername","no");
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

	$userarray .= "\n";
        $userarray =~ s/[\a\f\e\0\r\t\|]//isg;
	$userarray =~ s/\r\n/\n/ig;
	$userarray =~ s/\n+/\n/ig;
	$userarray =~ s/\n/\t/isg;
	$userarray =~ s/＊＃！＆＊//isg;

        @saveduserarray = split(/\t/,$userarray);
        
        $filetomake = "$lbdir" . "data/wordfilter.cgi";
        open (FILE, ">$filetomake");
        print FILE $userarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                
		print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
                <b>下列不良词语被保存，这些词汇在论坛中将自动被 ****** 替换。</b><br><br>
                );
                
                foreach $user(@saveduserarray) {
                    chomp $user;
                    print qq($user<br>);
                }
                print qq(<br><br><br><center><a href="setfilter.cgi">继续增加要过滤的不良词语</a></center>);
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
                $filetoopen = "$lbdir" . "data/wordfilter.cgi";
                open (FILE, "$filetoopen");
                $badusers = <FILE>;
                close (FILE);
                
                $badusers =~ s/\t/\n/g;
                $badusers =~ s/\&/\&amp;/g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 不良词语过滤</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>不良词语过滤</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#000000>
                <b>请注意：</b> 此功能是用来对一些不良词汇进行过滤。这样出现这些不良词汇的帖子将无法发布！
                <BR><BR>输入的时候，每行输入一个不良词汇即可。<BR><BR>
                特别注意：不允许对 | 字符进行过滤。<BR><BR>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF align=center colspan=2>
                <textarea cols=60 rows=20 wrap="virtual" name="userarray">$badusers</textarea><BR><BR>
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
