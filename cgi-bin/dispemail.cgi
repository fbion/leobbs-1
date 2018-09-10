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
use LBCGI;

$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "dispemail.cgi";

$query = new LBCGI;

my $allow_eamil_file = "${lbdir}data/allow_email.cgi";
if (-e $allow_eamil_file) {
    open(AEFILE, $allow_eamil_file);
    $allowtype = <AEFILE>;
    $allowmail = <AEFILE>;
    close(AEFILE);
    chomp $allowtype;
    chomp $allowmail;
}

$allowmail =~ s/\t+/\t/g;
$allowmail =~ s/^\t//;
$allowmail =~ s/\t$//;
$allowmail =~ s/\t/<br>/g;

$lbbody = 'topmargin="0" bottommargin="0" leftmargin="0" rightmargin="0"';
$allowtype_d = ($allowtype eq "allow") ? '必需使用下列邮箱才能注册' : '不允许使用下列邮箱注册';

$output = <<"HTML";
<table cellpadding=0 cellspacing=0 width=100% height="90%" bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100% height="100%">
<tr>
<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>$allowtype_d</b></font></td></tr>
<td bgcolor=$miscbackone height="90%" valign="top"><font color=$fontcolormisc>$allowmail</font></td></tr>
</table>
</td></tr>
</table><br>
HTML

print header(-charset => UTF -8, -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&output("$boardname - 邮箱限制", \$output, 'msg');
exit;
