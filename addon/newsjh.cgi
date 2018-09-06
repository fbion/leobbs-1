#!/usr/bin/perl
###################################################################################################
# 使用办法： newsjh.cgi?forum=分论坛号&max=显示几条贴子&maxlength=标题长度&display=1&mode=模式
# 例： 在你主页的适当位置加入以下语句
#      <script src="newsjh.cgi?forum=1&max=20&maxlength=20&mode=topic"></script>
#      这样就可以在相应位置显示1号论坛最新10个精华贴子，标题长度为 20，显示发贴时间，用帖子模式查看
#                                                    (display=0 表示不显示发贴时间)
#                                                    (mode=view 表示用新闻模式查看)
#
# 所有参数均可以省略，默认为查看第1个论坛的前20个精华帖子，标题最多20个字符、显示时间、用帖子模式
###################################################################################################

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
$mode       = $query -> param('mode');
$inforum       = $query -> param('forum');
$inforum       = &stripMETA("$inforum");
$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$display       = $query -> param('display');
$display       = &stripMETA("$display");
$maxlength     = $query -> param('maxlength');
$maxlength     = &stripMETA("$maxlength");
$mode = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # 默认帖子方式查看
$inforum   = 1  if ($inforum eq "");    # 默认查看第一个论坛
$display   = 1  if ($display eq "");    # 默认显示贴子时间
$max	   = 20 if ($max eq "");        # 默认显示 10 个精华帖子
$maxlength = 20 if ($maxlength eq "");  # 默认标题最多 20 个字符
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

print header(-charset=>UTF-8);
if ($inforum !~ /^[0-9]+$/) {
   print "document.write('普通&老大，别乱黑我的程序呀！')\n";
   exit;
}
    my $filetoopen = "${lbdir}forum$inforum/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    (my $no, $no, $no, $no, $no, $no ,$no ,$no ,$privateforum, $no) = split(/\t/,$forums);
if ($privateforum ne "yes") {
    $filetoopen = "$lbdir" . "boarddata/jinghua$inforum.cgi";
    if (-e $filetoopen) {
    	&winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
    else { undef @ontop; }
    $topcount = @ontop;
    $topcount=$max if ($topcount>$max);
    
    if ($topcount > 0) {
      $i=0;
      foreach $id (@ontop) {
      	chomp $id;
	next if ((!(-e "${lbdir}forum$inforum/$id.thd.cgi"))||($id eq ""));

	my $file = "$lbdir" . "forum$inforum/$id.pl";
	open (TMP, "$file");
	(my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon1, my $inposttemp) = split (/\t/,<TMP>);
	close (TMP);
 	$topictitle =~ s/^＊＃！＆＊//;
       
	my $file1 = "$lbdir" . "forum$inforum/$id.thd.cgi";
	if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")){
	open (TMP1, "$file1");
	my @tmp = <TMP1>;
	close (TMP);
	my $tmp = @tmp;
	$tmp --;
	my $tmp1 = $tmp[-1];
        $tmp1 =~ s/[\n\r]//isg;
	my $tmp2 = $tmp[0];
        $tmp1 =~ s/[\n\r]//isg;
	(my $membername, $topictitle, my $postipaddress, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/,$tmp2);
	(my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, $posticon1) = split(/\t/,$tmp1);
 	    $topictitle =~ s/^＊＃！＆＊//;
	    chomp $posticon;
	    $membername1 = "" if ($tmp eq 0);
	    $threadviews = ($tmp+1) * 8;
	    $postdate1 = $lastpostdate if ($lastpostdate ne "");
	    $inposttemp = $post1;
	    $inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//ig;
	    $inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//ig;
	    $inposttemp =~ s/\[quote\](.*)\[\/quote\]//ig;
	    $inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/ig;
	    $inposttemp =~ s/\:.{0,20}\://isg;
	    $inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	    $inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|jpeg|bmp|gif|swf)//isg;
	    $inposttemp =~ s/( )+$//isg;
	    $inposttemp =~ s/^( )+//isg;
	    $inposttemp =~ s/<(.|\n)+?>//g;
	    $inposttemp =~ s/\[.+?\]//g;
	    $inposttemp =~ s/[\a\f\n\e\0\r\t]//g;

	    $posticon =~ s/\s//isg;
	    if ($posticon =~/<br>/i) {
      		$posticon=~s/<br>/\t/ig;
      		@temppoll = split(/\t/, $posticon);
      		$temppoll = @temppoll;
      		if ($temppoll >1) {
      		    $posticon1 = "<br>";
      		}
      		else {
      		    $posticon1 = "";
      		}
	    }
	    $inposttemp = &lbhz($inposttemp,22);
            $posticon = "<br>" if ($posticon =~/<br>/i);

	    $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$tmp\t$threadviews\t$membername\t$postdate\t$membername1\t$postdate1\t$posticon1\t$inposttemp\t\n");
        }else{
   	    $threadviews = ($tmp+1) * 8 if ($threadviews eq "");
#   	    $threadviews = 9999 if ($threadviews > 9999);
            $posticon1 = "<br>" if ($posticon1 =~/<br>/i);
	    $topictitle =~ s/^＊＃！＆＊//;
            $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon1\t$inposttemp\t\n");
        }
	if ($topictitle ne "") {push (@topic, $rr); $i++;}
	last if ($i >= $max);
      }
   }
   else { undef @topic; }

if (@topic) {
    foreach $topic (@topic) {
	chomp $topic;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$topic);
	$longdate=&longdate($startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600));

           if (($posticon eq "")||($posticon !~ /^[0-9]+$/)) {
		$posticon = int(myrand(23));
		if ($posticon <10 ) {$posticon="0$posticon.gif"};
                if ($posticon > 9 ) {$posticon="$posticon.gif"};
           }
	$topictitle = &cleanarea("$topictitle");
 	$topictitle =~ s/\'/\`/g;
        $topictitle =~ s/\&amp;/\&/g;
	$topictitle =~ s/\&quot;/\"/g;
#	$topictitle =~ s/\&lt;/</g;
#	$topictitle =~ s/\&gt;/>/g;
	$topictitle =~ s/ \&nbsp;/　/g;
	$topictitle =~ s/  /　/g;
	if  ($display eq 1) {
	    $disptime= " $longdate";
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
	    $str.=qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$inforum&topic=$topicid target=_blank><ACRONYM TITLE="主题： $topictitle">$topictitletemp</ACRONYM></a>　<a href=profile.cgi?action=show&member=~ . ($uri_escape eq "no" ? $startedby : uri_escape($startedby)) . qq~ target=_blank>[$startedby]</a>　$disptime<br>~;
	 }
	 else {
	     $topicspace=$maxlength-length($topictitle);
	     $addspace = "";
	     for ($i=0;$i<$topicspace;$i++) {
	     	$addspace = $addspace ."&nbsp;";
	     }
	     $str.=qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$inforum&topic=$topicid target=_blank>$topictitle</a>$addspace　<a href=profile.cgi?action=show&member=~ . ($uri_escape eq "no" ? $startedby : uri_escape($startedby)) . qq~ target=_blank>[$startedby]</a>　$disptime<br>~;
	 }
    }
}
else {
        $str="-* 没有相应的论坛或者此论坛无精华文章 *-";
}
}
else {
    $str="-* 这是保密论坛 *-";
}

print "document.write('$str')\n";
exit;
