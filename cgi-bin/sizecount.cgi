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

use strict;
use warnings;
use diagnostics;
use diagnostics;

use LBCGI;
use File::Find;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "sizecount.cgi";

$query = new LBCGI;

$nextforum = $query->param('nextforum');
$action = $query->param("action");
$action = &cleaninput("$action");
$nextforum = 0 if ($nextforum eq "");

$inmembername = $query->cookie("adminname");
$inpassword = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&admintitle;

if ($action eq "process") {
    #1
    &getmember("$inmembername", "no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
        #2
        $tsize = 0;
        find(\&countsize, $lbdir);
        $lbsd = 'Bytes';
        $cgisize = $progsize = $osize = $tsize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print qq~
                <tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 统计论坛占用空间</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<br><br><br>
		<table width=85% align=center cellspacing=0 cellpadding=0 border=0>
		<tr><td><B><font color=blue>cgi-bin 占用空间：</B></td><td><b><font color=blue>&nbsp;$tsize $lbsd</b></td><td><b><font color=blue>($osize 字节)</b></td></tr>
		~;
        $tsize = 0;
        find(\&countsize, "${lbdir}$memdir");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 用户库占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        $tsize = 0;

        find(\&countsize, "${lbdir}data");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 数据文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        $tsize = 0;
        find(\&countsize, "${lbdir}help");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 帮助文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        $tsize = 0;

        opendir(DIRS, "$lbdir");
        my @files = readdir(DIRS);
        closedir(DIRS);
        @files = grep (/^\w+?$/i, @files);
        my @memfavdir = grep (/^memfav/i, @files);
        $memfavdir = $memfavdir[0];

        find(\&countsize, "${lbdir}$memfavdir");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 用户个人收藏占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        $tsize = 0;
        find(\&countsize, "${lbdir}boarddata");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 论坛重要数据目录占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        $tsize = 0;
        find(\&countsize, "${lbdir}lock");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 论坛锁定文件目录占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        $tsize = 0;

        find(\&countsize, "${lbdir}memfriend");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 用户好友列表占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

        $tsize = 0;
        find(\&countsize, "${lbdir}$msgdir");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 用户短消息占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

        $tsize = 0;

        opendir(DIRS, "$lbdir");
        my @files = readdir(DIRS);
        closedir(DIRS);
        @files = grep (/^\w+?$/i, @files);
        my @searchdir = grep (/^search/i, @files);
        $searchdir = $searchdir[0];

        find(\&countsize, "${lbdir}$searchdir");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $progsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 搜索记录占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

        open(FILE, "<${lbdir}data/allforums.cgi");
        @forumslist = <FILE>;
        close(FILE);
        chomp @forumslist;
        foreach (@forumslist) {
            ($forumid, $typename, $no, $forumname) = split(/\t/);
            if ($typename =~ /^childforum-[0-9]+/) {
                $typename2 = $typename;
                $typename2 =~ s/childforum-//;
                $cforumtypes{$typename2}->{$forumid} = $forumname;
            }
            $forumtypes{$typename}->{$forumid} = $forumname;
        }
        $output = '';
        while (($typename, $pointer) = each %forumtypes) {
            while (($forumid, $forumname) = each %$pointer) {
                $path = "${lbdir}forum$forumid";
                $tsize = 0;
                find(\&countsize, $path);
                $lbsd = 'Bytes';
                $osize = $tsize;
                if ($tsize > 1024) {
                    $tsize /= 1024;
                    $lbsd = 'KB';
                }
                if ($tsize > 1024) {
                    $tsize /= 1024;
                    $lbsd = 'MB';
                }
                if ($tsize > 1024) {
                    $tsize /= 1024;
                    $lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f", $tsize);
                $tsize =~ s/\s//g;

                $forumsizes{$forumid} = "$forumid\t$forumname\t&nbsp;$tsize $lbsd\t$osize";
            }
        }
        $forumsize = 0;
        while (($typename, $pointer) = each %forumtypes) {
            next if ($typename =~ /^childforum-[0-9]+/);
            @forumids = keys %$pointer;
            $tsize = 0;
            foreach (@forumsizes{@forumids}) {
                ($tforumno, $no, $no, $size) = split(/\t/);
                $tsize += $size;
                $hashname = $cforumtypes{$tforumno};
                while (($temp, $cforumname) = each %$hashname) {
                    ($no, $cforumname, $cshowsize, $cosize) = split(/\t/, $forumsizes{$temp});
                    $tsize += $cosize;
                    $output{$tforumno} .= "<tr><td>|　|　|　|- $cforumname</td><td>$cshowsize</td><td><font color=blue>($cosize 字节)</td></tr>\n";
                }
            }
            @forumids = keys %$pointer;
            $tsize = 0;
            foreach (@forumsizes{@forumids}) {
                ($no, $no, $no, $size) = split(/\t/);
                $tsize += $size;
            }
            $lbsd = 'Bytes';
            $osize = $tsize;
            $forumsize += $tsize;
            if ($tsize > 1024) {
                $tsize /= 1024;
                $lbsd = 'KB';
            }
            if ($tsize > 1024) {
                $tsize /= 1024;
                $lbsd = 'MB';
            }
            if ($tsize > 1024) {
                $tsize /= 1024;
                $lbsd = 'GB';
            }
            $tsize = sprintf("%6.2f", $tsize);
            $tsize =~ s/\s//g;

            $output .= "<tr><td>||- <font color=blue>$typename</td><td><font color=blue>&nbsp;$tsize $lbsd</td><td><font color=blue>($osize 字节)</td></tr>\n";
            foreach (@forumsizes{@forumids}) {
                ($tforumno, $forumname, $showsize, $osize) = split(/\t/);
                $output .= "<tr><td>|||- $forumname</td><td>$showsize</td><Td>($osize 字节)</td><tr>\n$output{$tforumno}";
            }
        }
        $osize = $tsize = $forumsize;
        $progsize -= $osize;
        $lbsd = 'Bytes';
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;
        print "<tr><td>|- <B>论坛帖子占用空间：</B></td><td><B>&nbsp;$tsize $lbsd</B></td><td><B>($osize 字节)</B></td></tr>\n";
        print $output;

        $osize = $tsize = $progsize;
        $lbsd = 'Bytes';
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;
        print "<tr><td>|- 程序文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

        $tsize = 0;
        find(\&countsize, $imagesdir);
        $lbsd = 'Bytes';
        $nonsize = $osize = $tsize;
        $allsize = $cgisize + $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr height=20><td colspan=3>&nbsp;</td></tr>\n";
        print "<tr><td><font color=blue><b>non-cgi 占用空间：</b></td><td><font color=blue><b>&nbsp;$tsize $lbsd</b></td><td><font color=blue><b>($osize 字节)</b></td></tr>\n";

        $tsize = 0;
        find(\&countsize, "${imagesdir}$usrdir");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $nonsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 帖子附件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

        $tsize = 0;
        find(\&countsize, "${imagesdir}usravatars");
        $lbsd = 'Bytes';
        $osize = $tsize;
        $nonsize -= $osize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 用户上传头像占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

        $osize = $tsize = $nonsize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td>|- 其他文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
        print "<tr height=50><td colspan=3>&nbsp;</td></tr>\n";

        $osize = $tsize = $allsize;
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'KB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'MB';
        }
        if ($tsize > 1024) {
            $tsize /= 1024;
            $lbsd = 'GB';
        }
        $tsize = sprintf("%6.2f", $tsize);
        $tsize =~ s/\s//g;

        print "<tr><td><font color=red><b>论坛占用总空间：</b></td><td><font color=red><b>&nbsp;$tsize $lbsd</b></td><td><font color=red><b>($osize 字节)</b></td></tr>\n";

        print qq~
		</table>
		</td></tr>
		~;
    }
    else {
        &adminlogin;
    }
}
else {
    &getmember("$inmembername", "no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
        print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 统计论坛占用空间</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>统计论坛占用空间</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>请注意:</b><br>此过程将耗费大量CPU时间和系统资源，请尽量少用本功能！
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
sub countsize {
    $tsize += -s $File::Find::name;
}