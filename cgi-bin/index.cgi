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
$LBCGI::POST_MAX=20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$action = $query -> param('action');

if ($action eq "change_skin") {
    if ($inmembername eq "") { $inmembername = "客人"; }
    else {
    &getmember("$inmembername","no");
    &error("普通错误&老大，偷用户名不偷密码有什么用呢？") if ($inpassword ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");  
    }
   $refrashurl = $query -> param('thisprog');
   $refrashurl = "leobbs.cgi" if($refrashurl eq "");
   $refrashurl = uri_escape($refrashurl);
#   unlink ("${lbdir}cache/myinfo/$inmembername.pl");
   $inselectstyle   = $query->param("skin");
#   $inselectstyle = "" if (lc($inselectstyle) eq "leobbs");
   &error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
   my $selectstylecookie= cookie(-name => "selectstyle" , -value => $inselectstyle, -path => "$cookiepath/");
   print header(-cookie  =>[$selectstylecookie], -charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
   print qq ~<script>location.href="$refrashurl";</script>~;
   print qq~页面已经更新，程序自动刷新，如果没有自动刷新，请手工刷新一次！！<BR><BR><meta http-equiv="refresh" content="3; url=$refrashurl">~;
   exit;
}
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "<script language='javascript'>document.location = 'leobbs.cgi'</script>";
print qq~页面已经更新，程序自动刷新，如果没有自动刷新，请手工刷新一次！！<BR><BR><meta http-equiv="refresh" content="3; url=leobbs.cgi">~;
exit;
