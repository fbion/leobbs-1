#!/usr/bin/perl
#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
require "data/boardinfo.cgi";
require "wap.pl";
$check = $query->param('check');
$lid = $query->param('lid');
&waptitle;
$show .= qq~<card  title="$boardname-登陆">~;
if ($check eq '1') {
    &check($lid);
    if ($inmembername ne '' && $inmembername ne '客人') {
        $pre = $query->param('pre');
        $mastnum = $query->param('mastnum');
        $mastnum2 = $query->param('mastnum2');
        $pre_index = $query->param('pre_index');
        $topicpre = $query->param('topicpre');
        open(file, "${lbdir}wap/$lid");
        my $bf = <file>;
        close(file);
        my ($inmembername, $xh2) = split(/\,/, $bf);
        open(file, ">${lbdir}wap/$lid");
        print file "$inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
        close(file);
        $show .= qq~<p>成功更改设置！</p><p><a href='wap.cgi?lid=$lid'>返回首页</a></p>~;
    }
    else {
        $show .= qq~<p>身份核认失败！请重新登陆</p><p><a href='wap_login.cgi'>登陆</a></p>~;
    }
    &wapfoot;
}
&check($lid);
$show .= qq~<p>个性设置 <br/>\n</p><p>
	列表项显示：<select name="pre" value="$pre">
		<option value="5">5篇</option>
		<option value="10">10篇</option>
	<option value="20">20篇</option>
	<option value="30">30篇</option></select>
	</p>
	<p>
	帖子回复每页显示：<select name="topicpre" value="$topicpre">
		<option value="1">1篇</option>
		<option value="3">3篇</option>
	<option value="10">10篇</option>
	<option value="15">15篇</option></select>
	</p>
	<p>
	论坛首页显示多少行：<select name="pre_index" value="$pre_index">
		<option value="10">10篇</option>
		<option value="16">16篇</option>
	<option value="25">25篇</option></select>
	</p>
	<p>
	帖子显示文字：<select name="mastnum" value="$mastnum">
		<option value="50">50字</option>
		<option value="100">100字</option>
	<option value="125">125字</option>
	<option value="500">500字</option></select>
	</p>
	<p>
	独立帖子显示文字：<select name="mastnum2" value="$mastnum2">
		<option value="340">340字</option>
		<option value="500">500字</option>
	<option value="1000">1000字</option>
	<option value="2000">2000字</option></select>
	</p>
	<p>
<anchor>[设置]<go href="wap_set.cgi" method="post">
<postfield name="pre" value="\$(pre)"/>
<postfield name="topicpre" value="\$(topicpre)"/>
<postfield name="pre_index" value="\$(pre_index)"/>
<postfield name="mastnum" value="\$(mastnum)"/>
<postfield name="check" value="1"/>
<postfield name="lid" value="$lid"/>
<postfield name="mastnum2" value="\$(mastnum2)"/></go>
</anchor> ~;
$show .= qq~
</p>~;
&wapfoot;
