#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
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

use warnings;
use strict;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "lookemotes.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

@params = $query->param;
foreach $param (@params) {
    $theparam = $query->param($param);
    $theparam = &cleaninput("$theparam");
    $PARAM{$param} = $theparam;
}

$action = $PARAM{'action'};
$in_forum = $PARAM{'forum'};
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));

$inmember = $query->param('member');
$in_member_name = $query->param("membername");
$in_password = $query->param("password");
$action = &cleaninput("$action");
$inmember = &cleaninput("$inmember");
$in_member_name = &cleaninput("$in_member_name");
$in_password = &cleaninput("$in_password");
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

if ($in_member_name eq "" || $in_member_name eq "客人") {$in_member_name = "客人";}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}

&mischeader("论坛EMOTE列表");

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

my %Mode = (
    'style' => \&styleform,

);

if ($Mode{$action}) {
    $Mode{$action}->();
}


##################################################################################
sub styleform {
    &mischeader("查看论坛 EMOTE 列表");
    $filetoopen = "$lbdir" . "data/emote.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    $emote = <FILE>;
    close(FILE);

    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=5 cellspacing=0 style="border-collapse: collapse">
        <tr><td bgcolor=$forumcolorone $catbackpic colspan=2 align=center>注意:下列所有的"对象"将被替换成发贴人的用户名.</td>
       ~;
    @pairs1 = split(/\&/, $emote);
    foreach (@pairs1) {
        ($toemote, $beemote) = split(/=/, $_);
        chomp $beemote;
        $output .= qq~
	<tr><td bgcolor=$forumcolorone>$toemote</td><td  bgcolor=$forumcolortwo>$beemote</td>	           
~;
    }
}

$output .= qq~</tr></table><SCRIPT>valignend()</SCRIPT><br><br></body></html>~;
&output("$board_name - 查看论坛 EMOTE 列表", \$output);
exit;

