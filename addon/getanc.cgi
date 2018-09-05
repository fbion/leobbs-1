#!/usr/bin/perl
###################################################################################
# LeoBBS 公告显示 ver 1.5
###################################################################################
# 使用办法： getanc.cgi?max=显示公告长度
# 例： 在你主页的适当位置加入以下语句
#      <script src="getanc.cgi?max=500"></script>
#      这样就可以在相应位置显示论坛的最新公告的前 500 字符。
#      如果想不限制显示字符数，可以设置 max 参数的值为 99999999，比如：
#      <script src="getanc.cgi?max=99999999"></script>
#
#      所有参数均可以省略，默认显示公告的前面 500 字符。
###################################################################################

#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
#  基于山鹰糊、花无缺制作的 LB5000 XP 2.30 免费版   #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBoard.com/          #
#      论坛地址： http://www.LeoBBS.com/            #
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

#unless ($ENV{'HTTP_REFERER'} =~ /$ENV{'HTTP_HOST'}/) {
#print "Content-Type:text/html\n\n";
#print "document.write('<font color=red>　对不起，不允许非本论坛主机调用！</font>');";
#exit;
#}
use LBCGI;
$LBCGI::POST_MAX=2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;
$query = new LBCGI;
$max	= $query -> param('max');
$max    = &stripMETA("$max");
$max	= 500 if ($max eq "");        # 默认显示公告的前 500 字符

print header(-charset=>gb2312);

    $filetoopen = "$lbdir" . "data/news.cgi";
    if (-e "$filetoopen") {
    	open(FILE, "$filetoopen");
    	flock (FILE, 1) if ($OS_USED eq "Unix");
        @announcements = <FILE>;
        close(FILE);
        ($title, $dateposted, $post, $nameposted) = split(/\t/, $announcements[0]);
                
      if ($post ne "") {
        $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
	$dateposted = &dateformat("$dateposted");
	        
	&lbcode(\$post);
	&doemoticons(\$post);
	&smilecode(\$post);
	$title =~ s/\'/\`/;
	$title =~ s/\&amp;/\&/g;
	$title =~ s/\&quot;/\"/g;
	$title =~ s/\&lt;/</g;
	$title =~ s/\&gt;/>/g;
	$title =~ s/ \&nbsp;/　/g;
	$title =~ s/  /　/g;
	$post =~ s/\'/\`/;
	$post =~ s/\&amp;/\&/g;
	$post =~ s/\&quot;/\"/g;
	$post =~ s/\&lt;/</g;
	$post =~ s/\&gt;/>/g;
	$post =~ s/ \&nbsp;/　/g;
	$post =~ s/  /　/g;
	if (length($post)>$max) {
	    $post = &lbhz("$post",$max) . "<p align=right><a href=announcements.cgi target=_blank>More>>></a>&nbsp;</p>";
	}
	$str=qq~ 
	<table width=95% border=0 cellspacing=0 cellpadding=0>
	<tr valign=top><td height=158> 
	<b>$title</b><br>$post
	</td></tr>
	<tr valign=top><td height=18 align=right>
	<br>$nameposted　　$dateposted&nbsp;
	</td></tr>
	</table>~;
      }
      else {
	$str = "当前没有公告！";
      }
    }
    else {
	$str = "当前没有公告！";
    }
$str=~s /\n//isg;
print "document.write('$str')\n";
exit;
