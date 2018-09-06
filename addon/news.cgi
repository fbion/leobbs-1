#!/usr/bin/perl
###############################################################################################################################################
# LeoBBS 分论坛新贴子 ver 2.0
###############################################################################################################################################
# 使用办法： news.cgi?forum=分论坛号&max=显示几条贴子&maxlength=标题长度&display=1&link=颜色16进制代码&vlink=颜色16进制代码&alink=颜色16进制代码
# 例： 在你主页的适当位置加入以下语句
#      <script src="news.cgi?forum=1&max=10&maxlength=20&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic"></script>
#      这样就可以在相应位置显示1号论坛的最新10个贴子，标题长度为 20，显示发贴时间，用帖子模式查看
#                                                   (display=0 表示不显示发贴时间)
#                                                   (mode=view 表示用新闻模式查看)
# link是自定义超链接的颜色，vlink是自定义已访问的超链接的颜色，alink是自定义当前超链接的颜色
#
# 所有参数均可以省略，默认为查看第1个论坛的前10个帖子，标题最多20个字符、显示时间、用帖子模式
###############################################################################################################################################

#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
#  基于山鹰糊、花无缺制作的 LB5000 XP 2.30 免费版   #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBoard.com/          #
#      论坛地址： http://www.LeoBBS.com/            #
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

#unless ($ENV{'HTTP_REFERER'} =~ /$ENV{'HTTP_HOST'}/) {
#print "Content-Type:text/html\n\n";
#print "document.write('<font color=red>　对不起，不允许非本论坛主机调用！</font>');";
#exit;
#}
use LBCGI;
$LBCGI::POST_MAX=2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";

$|++;
$query = new LBCGI;
$number        = $query -> param('forum');
$number        = &stripMETA("$number");
$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$display       = $query -> param('display');
$display       = &stripMETA("$display");
$maxlengths    = $query -> param('maxlength');
$maxlengths    = &stripMETA("$maxlengths");
$link	       = $query -> param('link');
$link          = &stripMETA("$link");
$alink	       = $query -> param('alink');
$alink         = &stripMETA("$alink");
$vlink	       = $query -> param('vlink');
$vlink         = &stripMETA("$vlink");
$mode       = $query -> param('mode');
$mode       = &stripMETA("$mode");
$mode = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # 默认帖子方式查看
$number    = 1  if ($number eq "");     # 默认查看第一个论坛
$display   = 1  if ($display eq "");    # 默认显示贴子时间
$max	   = 10 if ($max eq "");        # 默认显示 10 个帖子
$maxlengths= 30 if ($maxlengths eq "");  # 默认标题最多 30 个字符
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>UTF-8);
if ($number !~ /^[0-9]+$/) {
   print "document.write('普通&老大，别乱黑我的程序呀！')\n";
   exit;
}

if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

if ($enterminmony > 0 || $enterminjf > 0 || $enterminweiwang > 0 || $allowusers ne '') {
    $str="-* 这是保密论坛，不能列表 *-";
    goto ENDPPP;
}
    my $filetoopen = "${lbdir}forum$number/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    (my $no, $no, $no, $no, $no, $no ,$no ,$no ,$privateforum, $startnewthreads,$no) = split(/\t/,$forums);

if (($startnewthreads eq "cert")&&($userincert eq "no")) {
    $str="-* 这是保密论坛，不能列表 *-";
    goto ENDPPP;
}

if ($privateforum ne "yes") {
    $filetoopen = "$lbdir" . "boarddata/listno$number.cgi";
    if (-e $filetoopen) {
        open(FILE, "$filetoopen");
        @topics = <FILE>;
        $topics = @topics;
        $max = $topics if ($topics<$max);
    
        $max--;
        undef $str;
        $addtime = $timedifferencevalue*3600 + $timezone*3600;
        foreach $topic (@topics[0 ... $max]) {
	    chomp $topic;
            $maxlength = $maxlengths;
            ($topicid, $no) = split(/\t/,$topic);

    my $rr = &readthreadpl($number,$topicid);
    if ($rr ne "") {
	($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp) = split (/\t/,$rr);
    }
    else { next; }

            next if ($topicid !~ /^[0-9]+$/);
            $lastpostdate = &longdate($lastpostdate + $addtime);
 	    $topictitle =~ s/^＊＃！＆＊//;
 	    
            if (($posticon1 eq "")||($posticon1 !~ /^[0-9]+$/)) {
		$posticon1 = int(myrand(23));
		if ($posticon1 <10 ) {$posticon1="0$posticon1.gif"};
                if ($posticon1 > 9 ) {$posticon1="$posticon1.gif"};
            }
	    $topictitle = &cleanarea("$topictitle");
 	    $topictitle =~ s/\'/\`/g;
            $topictitle =~ s/\&amp;/\&/g;
	    $topictitle =~ s/\&quot;/\"/g;
#	    $topictitle =~ s/\&lt;/</g;
#	    $topictitle =~ s/\&gt;/>/g;
	    $topictitle =~ s/ \&nbsp;/　/g;
	    $topictitle =~ s/  /　/g;
	    if  ($display eq 1) {
	        $disptime= " $lastpostdate";
	    }
	    else { undef $disptime; }
	    if (length($topictitle)>$maxlength) {
	        $topictitletemp=&lbhz("$topictitle",$maxlength); 
	        $topictitletemp =~ s/\'/\`/;
		$topictitletemp =~ s/\&/\&amp;/g;
		$topictitletemp =~ s/\&amp;\#/\&\#/isg;
		$topictitletemp =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
		$topictitletemp =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
		$topictitletemp =~ s/\"/\&quot;/g;
		$topictitletemp =~ s/</\&lt;/g;
		$topictitletemp =~ s/>/\&gt;/g;
		$topictitletemp =~ s/ /\&nbsp;/g;
	        $topictitletemp = $topictitletemp ."&nbsp;" if (length($topictitletemp) < $maxlength);
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank><ACRONYM TITLE=\"主题： $topictitle\">$topictitletemp</ACRONYM></a>$disptime<br>";
	    }
	    else {
	        $topicspace=$maxlength-length($topictitle);
	        $topictitle =~ s/ /\&nbsp;/g;
	        $addspace = "";
	        for ($i=0;$i<$topicspace;$i++) {
	     	    $addspace = $addspace ."&nbsp;";
	        }
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank>$topictitle</a>$addspace$disptime<br>";
	    }
        }
    }
    else {
        $str="-* 没有找到相应的论坛 *-";
    }
}
else {
    $str="-* 这是保密论坛，不能列表 *-";
}
ENDPPP:

print "document.write('<span LINK=#$link VLINK=#$vlink ALINK=#$alink>$str')\n";
exit;
