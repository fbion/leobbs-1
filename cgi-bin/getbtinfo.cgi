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

use BTINFO;
use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/styles.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "getbtinfo.cgi";
use LBCGI;
$query = new LBCGI;
#&ipbanned;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$forum  = $query->param("forum");
$inforum = $forum;
&error("打开文件&老大，别乱黑我的程序呀！") if ($inforum !~ /^[0-9]+$/);
$intopic = $query->param("topic");
&error("打开文件&老大，别乱黑我的程序呀！") if ($intopic !~ /^[0-9]+$/ && $intopic ne "");

$filename = $query->param('filename');
$filename =~ s/[\a\f\n\e\0\r\t\*\\\/\,\|\<\>\?\.]//isg;
if ($intopic ne "") { $tmptopic = $intopic%100; $filename = "$tmptopic/$filename"; }
&error("打开文件&该 BitTorrent 文件不存在！！") unless (-e "${imagesdir}$usrdir/$inforum/$filename.torrent");

my $btinfofile = "${imagesdir}$usrdir/$inforum/$filename.torrent.btfile";
my $filetoopens = &lockfilename($btinfofile);
unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 33);
unless ((!(-e "$filetoopens.lck")) && -e $btinfofile && (-M $btinfofile) * 86400 < 180)
{
	&winlock($btinfofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(FILE, $btinfofile);
	my $btfileinfo = <FILE>;
	my $hash = <FILE>;
	my $seedinfo = <FILE>;
	close(FILE);
	chomp($btfileinfo);
	chomp($hash);
	chomp($seedinfo);
	(my $announce, undef) = split(/\|/, $seedinfo);
	if ($hash eq "")
	{
		$/ = "";
		open(FILE, "${imagesdir}$usrdir/$inforum/$filename.torrent");
		binmode(FILE);
		my $upfilecontent = <FILE>;
		close(FILE);
		$/ = "\n";
		$btfileinfo = process_file($upfilecontent);
		($btfileinfo, $hash, $announce) = split(/\n/, $btfileinfo);
	}
	my $seedinfo = output_torrent_data($hash, $announce);
	$btinfo = "$btfileinfo\n$hash\n$announce\|$seedinfo";

	open(FILE, ">$btinfofile");
	print FILE $btinfo;
	close(FILE);
	&winunlock($btinfofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
}
else
{
	$/ = "";
	open(FILE, $btinfofile);
	$btinfo = <FILE>;
	close(FILE);
	$/ = "\n";
	chomp($btinfo);
	my ($btfileinfo, $hash, $seedinfo) = split(/\n/, $btinfo);
	($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
	if ((($seeds eq "")||($seeds eq "未知"))&&($announce ne "")) {
	  eval("use BTINFO;");
	  if ($@ eq "") {
	    my $seedinfo = output_torrent_data($hash, $announce);
	    $btinfo = "$btfileinfo\n$hash\n$announce\|$seedinfo";
	    ($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
	    if (($seeds ne "")&&($seeds ne "未知")) {
	        open(FILE, ">$btinfofile");
	        print FILE $btinfo;
	        close(FILE);
	    }
	  }
	}
}

my ($btfileinfo, undef, $seedinfo) = split(/\n/, $btinfo);

($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
if ($seeds eq "") {
	$seeds = "未知";
	$leeches = "未知";
	$downloaded = "未知";
}

print qq~
<html>
<head>
<title>欢迎您光临$boardname BitTorrent</title>
<meta http-equiv="Content-Type" Content="text/html; charset=gb2312">
<style>
a:visited	{text-decoration: none}
a:active	{text-decoration: none}
a:hover		{text-decoration: underline overline}
a:link		{text-decoration: none;}
a:hover		{color: #5511ff; text-decoration: none; position: relative; right: 0px; top: 1px} 
.t		{line-height: 1.4}
.t		{line-height: 1.4}
body		{font-family: 宋体; font-size: 9pt;}
td,div,form,option,p,td,br{font-family: Tahoma; font-size: 9pt} 
textarea,select	{border-width: 1; border-color: #000000; background-color: #efefef; font-family: Tahoma; font-size: 9pt; font-style: bold;}
</style>
</head>
<body topmargin=0 marginwidth=0 marginheight=0>
<br><center>
<table cellSpacing=1 cellPadding=4 bgColor=$tablebordercolor width=150>
<tr bgColor=$titlecolor><td align=middle nowrap><font color=$titlefontcolor>$filename.torrent</td></tr>
<tr bgColor=$postcolorone><td nowrap>&nbsp;<font color=$postfontcolorone>种子数：$seeds�������Ӳ��ϻ��߾ܾ����ݲ�ѯ��</td></tr>
</table>
<br><br>
</body></html>~;
exit;