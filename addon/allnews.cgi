#!/usr/bin/perl
#########################################################################################################################
# 论坛新新贴子，显示整个论坛的最新贴 ver 2.1
#########################################################################################################################
# 使用办法： allnews.cgi?maxlength=标题长度&display=显示方式&name=名字显示&link=颜色代码&vlink=颜色代码&alink=颜色代码&max=显示几条贴子
# 例： 在你主页的适当位置加入以下语句
#      <script src="allnews.cgi?maxlength=20&display=1&name=1&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic&max=10"></script>
#      这样就可以在相应位置显示整个论坛的最新 10 个贴，标题长度 20，显示发贴时间，显示发贴人，用帖子模式查看
#                                            (display=0 表示不显示发贴时间)
#                                            (name=0 表示不显示发贴人)
#                                            (mode=view 表示用新闻模式查看)
# link是超链接的颜色，vlink是已访问过的超链接，alink是当前超链接
# 
# 对于显示贴子个数，论坛最多只记录 30 个，所以，设置这个数字的时候不必超过 30 ！
#
# 所有参数均可以省略，默认为最新10个贴，标题最多20个字符、显示时间、用帖子模式
#########################################################################################################################

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
$|++;
$query = new LBCGI;

$maxlength   = $query -> param('maxlength');
$maxlength   = &stripMETA("$maxlength");
$display     = $query -> param('display');
$display     = &stripMETA("$display");
$name        = $query -> param('name');
$name        = &stripMETA("$name");
$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$link        = $query -> param('link');
$link        = &stripMETA("$link");
$vlink       = $query -> param('vlink');
$vlink       = &stripMETA("$vlink");
$alink       = $query -> param('alink');
$alink       = &stripMETA("$alink");
$mode        = $query -> param('mode');
$mode        = &stripMETA("$mode");
$mode      = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # 默认帖子方式查看
$maxlength = 20 if ($maxlength eq "");  # 默认标题最多 20 个字符
$display   = 1  if ($display eq "");    # 默认显示贴子时间
$name      = 1  if ($name eq "");       # 默认显示发贴人
$max	   = 10 if ($max eq "");        # 默认显示 10 个帖子
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
    $filetoopen = "$lbdir" . "data/recentpost.cgi";
    if (-e $filetoopen) {
	open(FILE, "$filetoopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
        @topics = <FILE>;
        close(FILE);
        $topics = @topics;
        $max = $topics if ($topics<$max);
        $max--;

        $str="<span LINK=#$link VLINK=#$vlink ALINK=#$alink>";
	$addtime = $timedifferencevalue*3600 + $timezone*3600;
        foreach $topic (@topics[0 ... $max]) {
            chomp $topic;
            ($forumid, $topicid, $topictitle, $posttime, $posticon1, $membername) = split(/\t/,$topic);
            $topictitle =~ s/^＊＃！＆＊//;
            next if (($forumid !~ /^[0-9]+$/)||($topicid !~ /^[0-9]+$/));
            $posttime = dateformat($posttime + $addtime);
            if (($posticon1 eq "")||($posticon1 !~ /^[0-9]+\.gif$/i)) {
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
	    if  ($display eq 1) {
	        $disptime= " ($posttime)";
	    }
	    else { undef $disptime; }
	    if ($name eq 1) {
	        $memberspace=16-length($membername)-1;
	        $addmspace = "";
	        for ($i=0;$i<$memberspace;$i++) {
	     	    $addmspace = $addmspace ."&nbsp;";
		}
		$addmspace = qq~　　<a href=$boardurl/profile.cgi?action=show&member=~ . ($uri_escape eq "no" ? $membername : uri_escape($membername)) . qq~ title=点击查看$membername的资料 target=_blank>[$membername]</a>$addmspace~;
	    }
	    else { undef $addmspace; }

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
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><ACRONYM TITLE=\"主题： $topictitle\"><font color=$color>$topictitletemp</font></ACRONYM></a>$addmspace$disptime<br>";
	    }
	    else {
  	        $topicspace=$maxlength-length($topictitle);
	        $addspace = "";
	        for ($i=0;$i<$topicspace;$i++) {
	     	   $addspace = $addspace ."&nbsp;";
	        }
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><font color=$color>$topictitle</font></a>$addspace$addmspace$disptime<br>";
	    }
        }
    }
    else {
        $str.="论坛上没有最新贴子";
    }    

print "document.write('$str')\n";
exit;
