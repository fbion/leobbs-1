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
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$query = new LBCGI;
&error("连接出错&对不起，不允许使用 GET 连结！") unless ($ENV{'REQUEST_METHOD'} =~ /^POST$/i);
&error("连接出错&对不起，不允许非本论坛主机连结！") if ($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/ && $ENV{'HTTP_HOST'} ne '' && $ENV{'HTTP_REFERER'} ne '');
$in_forum = $query->param('forum');
$in_topic = $query->param('topic');
$in_post_no = $query->param('postno');
$decrypt = $query->param('clno');
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic !~ /^[0-9]+$/) || ($in_forum !~ /^[0-9]+$/) || ($in_post_no !~ /^[0-9]+$/) || ($decrypt !~ /^[0-9]+$/));
$in_member_name = $query->cookie("amembernamecookie");
$in_password = $query->cookie("apasswordcookie");
&error("普通错误&老大，别乱黑我的程式呀！！") if (($in_member_name =~ m/\//) || ($in_member_name =~ m/\\/) || ($in_member_name =~ m/\.\./));
$in_member_name =~ s/\///g;
$in_member_name =~ s/\.\.//g;
$in_member_name =~ s/\\//g;
if ((!$in_member_name) or ($in_member_name eq "客人")) {
    &error("普通错误&必需为本论坛用户方可进入，请重新登录！");
}
else {
    &getmember("$in_member_name", "no");
    &error("普通错误&密码与用户名不相符，请重新登录！") if ($in_password ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");
}
my $filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
if (open(FILE, "$filetoopen")) {
    @threads = <FILE>;
    close(FILE);
    chomp @threads;
}
else {
    &error("连接出错&找不到该编号的连结，请确定你来自一个有效的连接！");
}
$get_the_post = $threads[$in_post_no];
@split_the_post = split(/\t/, $get_the_post);
$post_text = $split_the_post[6];
if ($post_text =~ /\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/i) {
    $post_text = "#$post_text";
    $post_text =~ s/\n//sg;
    @clinklist = ();
    $clinkcount = 0;
    $post_text =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\n\$clinklist[\$clinkcount]="$1:\/\/$2";\n\$clinkcount++;\n\#/isg;
    eval($post_text);
    $get_the_link = $clinklist[$decrypt];
    chomp $get_the_link;
}
$get_the_link = $clinklist[$decrypt];
chomp $get_the_link;
&error("连接出错&找不到该编号的连结，请确定你来自一个有效的连接。") if ($get_the_link eq "");
if ($get_the_link =~ m/^(http|https|ftp):\/\//i) {
    print header(-charset => "UTF-8", -location => $get_the_link, -expires => now, -cache => yes);
}
else {
    &error("连接出错&该编号的连结不是支持的通讯协定，本程序只支持 HTTP,HTTPS 和 FTP 。");
}
exit;
