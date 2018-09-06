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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "exportemail.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action       = $query -> param("action");
$action       = &cleaninput("$action");
$inexport     = $query -> param('exporter');
$intarname    = $query -> param('tarname');
$intarname    =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
&getmember("$inmembername");
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) { #s1
    if ($action eq "delete") {
    	unlink ("${imagesdir}$intarname.csv");
    	print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>欢迎来到论坛管理中心 / 导出会员 Email</b></td></tr><tr>
<td bgcolor=#FFFFFF valign=middle colspan=2><b><br>
<center>删除用户资料残留文件 $imagesdir$intarname.csv 成功!<br><br><a href=exportemail.cgi>再次导出其他用户类型的 Email.</a></center>);
    }
    elsif ($action eq "process") {
	opendir (DIR, "$imagesdir"); 
	my @countvar = readdir(DIR);
	closedir (DIR);
	@countvar = grep(/\.csv$/i,@countvar);
	foreach (@countvar) {
            unlink ("${imagesdir}$_");
        }

        $inexportusers  = $query -> param('exportusers');
        $inexportusers  =~ s/\, /\,/gi;
        $inexportusers  =~ s/ \,/\,/gi;
        $inexportusers  =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
        @senduserlist   = split(/\,/,$inexportusers);
        print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>欢迎来到论坛管理中心 / 导出会员 Email</b></td></tr><tr>
<td bgcolor=#FFFFFF valign=middle colspan=2><b>如下是您所需要用户类型的 Email 列表：</b><br>
<table><tr><td bgcolor=#FFFFFF valign=middle align=center colspan=2>
<textarea cols=60 rows=10>
);
	open (MEMFILE, "${lbdir}data/lbmember.cgi");
	@cgi1 = <MEMFILE>;
	close(MEMFILE);
	$counts=0;
	if ($inexportusers ne "") {
    	    foreach $exusers (@senduserlist){
    	    	chomp $exusers;
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,$no,$no,$no,$email) = split(/\t/,$_);
		    if ($membername eq $exusers) {
		    	push (@cgi,"$membername,$email,$counts,\n");
		    	$counts++;
		    }
		}
	    }
	}
	else {
	    if ($inexport eq "allmanager") {
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,my $membercode,my $no,$no,my $email) = split(/\t/,$_);
		    if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo")) {
		    	push (@cgi,"$membername,$email,$counts,\n");
		    	$counts++;
		    }
		}
	    }
	    elsif ($inexport eq "all") {
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,my $membercode,my $no,$no,my $email) = split(/\t/,$_);
	    	    push (@cgi,"$membername,$email,$counts,\n");
		    $counts++;
		}
	    }
	    else {
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,my $membercode,my $no,$no,my $email) = split(/\t/,$_);
		    if ($membercode eq $inexport) {
		    	push (@cgi,"$membername,$email,$counts,\n");
		    	$counts++;
		    }
		}
	    }
	}
	unshift (@cgi, "姓名,电子邮件地址,foxaddrID,foxaddrListMembers\n");
        my $time=time;
        $time=crypt($time,"lb");
        $time=~s /\///isg;
        $time=~s /\.//isg;
        $tarname=$time;        
	$filetomake = "${imagesdir}$tarname" . ".csv";
	open(FILE, ">$filetomake");print FILE @cgi;close FILE;
	    
	print qq(@cgi</textarea><BR></td></tr>);
        print qq(<br><br><a href=$imagesurl/$tarname.csv>点击此处下载邮件列表 (Foxmail-CSV地址簿格式)</a><br>
<a href=$thisprog?action=delete&tarname=$tarname>点击此处删除 FTP 上遗留的这个文件</a><br><br><center><a href="exportemail.cgi">再次导出其他用户类型的Email</a></center>);
    }
    else {
       my $memteam1 = qq~<option value="rz1">所有$defrz1(认证用户)</option>~ if ($defrz1 ne "");
       my $memteam2 = qq~<option value="rz2">所有$defrz2(认证用户)</option>~ if ($defrz2 ne "");
       my $memteam3 = qq~<option value="rz3">所有$defrz3(认证用户)</option>~ if ($defrz3 ne "");
       my $memteam4 = qq~<option value="rz4">所有$defrz4(认证用户)</option>~ if ($defrz4 ne "");
       my $memteam5 = qq~<option value="rz5">所有$defrz5(认证用户)</option>~ if ($defrz5 ne "");
	print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>欢迎来到论坛管理中心 / 导出会员 Email</b></td></tr><tr>
<td bgcolor=#EEEEEE valign=middle align=center colspan=2><font color=#333333><b>导出会员 Email</b></td></tr>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="process">
<tr><td bgcolor=#FFFFFF valign=middle colspan=2><br>
　　<b>通过这功能可以将导出的会员资料导入到 Foxmail 的地址簿内，以便于您能通过邮件来更好地与会员联系。</b><br><br>
<font color=#000000>导出对象：　　<select name="exporter" size="1"><option value="all">所有用户</option><option value="allmanager">所有管理员</option><option value="ad">所有坛主</option><option value="smo">所有总版主</option><option value="cmo">分类区版主</option><option value="mo">所有版主</option><option value="amo">所有副版主</option><option value="rz">所有认证会员</option>$memteam1$memteam2$memteam3$memteam4$memteam5<option value="me">所有普通会员</option></select><br>
<font color=#000000>导出指定对象：<input type=text name="exportusers" size=30>　 (用逗号分开各会员 ID )
<br></td></tr>
<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
<input type=submit name=submit value=提交></td></form></table></tr></td></tr></table>
);
    }
}
else {
    &adminlogin;
}
print qq~</td></tr></table></body></html>~;
exit;
