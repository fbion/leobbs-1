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

$thisprog = "setbadwords.cgi";
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
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
            

if ($action eq "process") {
 
    &getmember("$inmembername","no");
        
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
 
 	$wordarray =~ s/[\f\n\r]+/\n/ig;
	$wordarray =~ s/[\r \n]+$/\n/ig;
	$wordarray =~ s/^[\r\n ]+/\n/ig;
        $wordarray =~ s/\n\n//g;
        $wordarray =~ s/\n/\&/g;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/badwords.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>所有信息已经被成功保存。</b></center><br><br>
                <b>下列“词语自动转换”被保存！</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($bad, $good) = split(/\=/,$_);
                    print qq(所有出现 <b>$bad</b> 的地方将被 <b>$good</b> 替换。<br>);
                }
                print qq(
                <br><br><br><center><a href="setbadwords.cgi">再次增加词语自动转换</a><br></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>信息没有被保存！</b><br>文件或者目录不可写。
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
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
                # Open the badword file

                $filetoopen = "$lbdir" . "data/badwords.cgi";
                open (FILE, "$filetoopen") or $badwords = "damn=d#amn\nhell=h#ll";
                $badwords = <FILE> if (!$badwords);
                close (FILE);
                
                $badwords =~ s/\&/\n/g;
        	$badwords =~ s/\n\n/\n/ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 词语自动转换</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>词语自动转换</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=宋体 color=#000000>
                词语自动转换可以阻止一些不好的字眼出现在论坛中。你可在下面写入词语和转换后的词语。<br>
                这样，这些词语在<b>发表文章</b>时，会被自动转换。<br>
                <b>使用方法：</b>使用方法：</b>写入一个词语和转换后的词语，并在中间加上 "=" (等于号)。<BR><br>
		<b>特别提示：</b>如果你仅仅是过滤，而不在乎转换后的词语，那么请使用"<a href=setfilter.cgi>不良词语过滤</a>"功能，这样可以提高效率！<BR><BR><BR>
                <b>注意1，请尽量减少词语自动转换的条目，多使用"<a href=setfilter.cgi>不良词语过滤</a>"功能！</b><br><br>
                <b>注意2，每行只能写一个！</b><br><br>
                <b>注意3，尽量避免使用 * ( ) 之类的符号！</b><br><br>
                <b>例如：</b>fuck=f##k<br><br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=20 wrap="virtual" name="wordarray">$badwords</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <input type=submit name=submit value="提 交"></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
