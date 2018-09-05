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

$thisprog = "setidbans.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$wordarray     = $query -> param('wordarray');
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

	$wordarray =~ s/[\`\~\!\@\#\$\%\&\=\\\{\}\;\'\:\"\,\.\/\<\>]//isg;
        $wordarray =~ s/\s+/\n/ig;
        $wordarray =~ s/\n\n/\n/ig;
        my @hasbannedid=split(/\n/,$wordarray);
	foreach (@hasbannedid){
	    $nametocheck = $_; 
	    $nametocheck =~ s/ /\_/g; 
	    $nametocheck =~ tr/A-Z/a-z/; 
	    $nametocheck = &stripMETA($nametocheck); 
	    my $namenumber = &getnamenumber($nametocheck);
	    &checkmemfile($nametocheck,$namenumber);
	    $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi"; 
	    if (-e $filetoopen) { 
		open(FILE9,"$filetoopen"); 
		my $filedata = <FILE9>; 
		close(FILE9); 
		($lmembername, $lpassword, $lmembertitle, $lmembercode, $lnumberofposts) = split(/\t/,$filedata); 
		if (($lmembercode eq "ad")||($lmembercode eq "smo")||($lmembercode eq "cmo")||($lmembercode eq "mo")||($lmembercode eq "amo")){
		    print qq(
<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>欢迎来到论坛管理中心 / ID 禁止</b>
</td></tr>
<tr>
<td bgcolor=#FFFFFF valign=middle colspan=2>
<font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
<b>你不能禁止 ID:$_,因为他（她）是管理员！</b><br><br>
);
		    print qq~</td></tr></table></body></html>~;
		    exit;
		}
	    }
	    unlink ("${lbdir}cache/id/$nametocheck.cgi") if (-e "${lbdir}cache/id/$nametocheck.cgi");

    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/id/$_") if ((-M "${lbdir}cache/id/$_") *86400 > 600);
    }

	}
        $wordarray2display = $wordarray;
        $wordarray2display =~ s/\n/<br>/g;
	$wordarray =~ s/\n/\t/isg;
        $filetomake = "$lbdir" . "data/idbans.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / ID 禁止</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
		<b>你已经禁止了下列 ID</b><br><br>
		);
                    print qq(<b>$wordarray2display</b><br>);
                print qq(
                <br><br><br><center><a href="setidbans.cgi">再次增加一些禁止的 ID</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#2159C9" colspan=2><font color=#FFFFFF>
			<b>欢迎来到 LeoBBS 论坛管理中心</b>
			</td></tr>
			<tr>
			<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
			<font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    	</td></tr></table></td></tr></table>
		     	);
                    }
                }
        }
        
    else {
        
        &getmember("$inmembername","no");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $idfiletoopen = "$lbdir" . "data/idbans.cgi";
                open (FILE, "$idfiletoopen");
                @bannedids = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / ID 禁止</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>ID 禁止列表</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>请注意:</b>如果你禁止了一个 ID 的话，那么这个 ID 将而无法登录！<br>
		<br>
		<b>说明:</b><BR>
		             你如果要禁止一个 ID，可以直接输入 ID 在这里，比如： Tom<BR>
		             每行写一个 ID，注意最后回车！<BR><BR>
	                </font></td>
		</tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
		<textarea cols=60 rows=18  name="wordarray">);
		                foreach (@bannedids) {
		                   $singleid = $_;
		                   chomp $_;
		                   next if ($_ eq "");
						   #$singleid =~ s/\n\s/\n/g;
				   $singleid =~ s/\t/\n/isg;
		                   print qq($singleid);
		                }
		                print qq(</textarea><BR>
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=提交></td></form></tr></table></td></tr></table>
);
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
