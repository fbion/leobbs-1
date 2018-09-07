#!/usr/bin/perl
###################################################################################
#	LeoBBS 公告显示 ver 1.5 a (tinha 修改版)
###################################################################################
#	使用办法： getanc2.cgi?show=显示的公告数目&maxlength=标题长度&forum=分论坛编号
#	例：在您首页的适当位置加入以下语句
#	<script src="getanc2.cgi?show=5&maxlength=20&forum=1"></script>
#	这样就可以在网页显示编号 1 号分论坛的最新 5 则公告，-则标显 20 字元。
#	如想显示主论坛公告，可以把 &forum=分论坛编号 省去。
#	所有叁数均可以省略，预设显示所有公告，标题显示所有字元。
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
#print "document.write('<font color=red> 对不起，不允\许\非本论坛主机调用！</font>');";
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
$show = $query -> param('show');
$show = 999 if ($show eq "");	# 预设显示所有公告
$maxlength = $query -> param('maxlength');
$maxlength = &stripMETA("$maxlength");
$maxlength = 999999999 if ($maxlength eq "");	 # 预设标题显示所有字元
$forum = $query -> param('forum');

print header(-charset=>utf8);

if ($forum ne "") { $filetoopen = "$lbdir" . "data/news$forum.cgi";}
else { $filetoopen = "$lbdir" . "data/news.cgi";}

if (-e "$filetoopen") {
	open(FILE, "$filetoopen");
	@announcements = <FILE>;
	close(FILE);

	$lines = @announcements - 1;
	$show = $show - 1;
	if ($lines < $show) { $show = $lines;}

	foreach $announcements (@announcements [0 ... $show]) {
		($title, $dateposted, undef, $nameposted) = split(/\t/, $announcements);
		$dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
		$dateposted = &dateformatshort("$dateposted");
		$newstitleid++;

		if (length($title) > $maxlength) { $title = &lbhz("$title",$maxlength);}
		        $title =~ s/\'/\`/;
			$title =~ s/\&/\&amp;/g;
			$title =~ s/\&amp;\#/\&\#/isg;
			$title =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
			$title =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
			$title =~ s/\"/\&quot;/g;
			$title =~ s/</\&lt;/g;
			$title =~ s/>/\&gt;/g;
			$title =~ s/ /\&nbsp;/g;

		if ($forum ne "") { $showforum = "?forum=$forum";}
		else { $showforum = "";}

		$str.= qq~
		<tr align=left><td><font style="font-size:12pt;font-family:宋体"><a href=$boardurl/announcements.cgi$showforum#title$newstitleid target=_blank>$title</a></font></td></tr>
		<tr align=right valign=top><td><font style="font-size:9pt;宋体">$nameposted 公布于 $dateposted</font></td></tr><tr><td>  </td></tr>
		~;
		}
	}
else {
$str = "目前没有公告！";
}
$str=~s /\n//isg;
print "document.write('<table width=100% border=0 cellspacing=0 cellpadding=0>$str</table>')\n";
exit;

