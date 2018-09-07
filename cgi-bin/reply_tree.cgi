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
$LBCGI::POST_MAX=100000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "reply_tree.cgi";
$query = new LBCGI;
#Cookie 路径
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
	$boardurltemp =$boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
#	$cookiepath =~ tr/A-Z/a-z/;
}

#取得论坛及主题编号
$inforum			= int($query -> param('forum'));
$intopic			= int($query -> param('topic'));
$instart			= int($query -> param('start'));
&ERROROUT("老大，别乱黑我的程序呀！") if (($inforum !~ /^[0-9]+$/)||($intopic !~ /^[0-9]+$/)||($instart !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

$screenmode = $query->cookie("screenmode");
$screenmode = 8 if ($screenmode eq "");
$addtimes = ($timedifferencevalue + $timezone)*3600;

#取出主題 ID
$id_of_this_topid	= sprintf("%04d%05d",$inforum,$intopic);
#用户资料
$inmembername	= $query->cookie("amembernamecookie");
$inpassword 	= $query->cookie("apasswordcookie");
$userregistered	= "no";
&ERROROUT("老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
unless ((!$inmembername) or ($inmembername eq "客人")) { 
	&getmember("$inmembername","no");
	$mymembercode=$membercode;
	$myrating=$rating;
	&ERROROUT("密码与用户名不相符，请重新登录！") if ($inpassword ne $password);
}
&ERROROUT("会员专用功能，请先登录！") if ($userregistered eq "no");
#取得分论坛资料
&getoneforum("$inforum");
$myinmembmod = $inmembmod;
$testentry = cookie("forumsallowed$inforum");
if (((($testentry ne $forumpass)||($testentry eq ""))&&($privateforum eq "yes"))||(($startnewthreads eq "cert")&&($membercode eq "me")&&($userincert eq "no"))) {
	&ERROROUT("你不允许进入该论坛！") if(($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));
}

&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &ERROROUT("你不允许进入该论坛！") if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &ERROROUT("你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&ERROROUT("你不允许进入该论坛，你的金钱为 $mymoney，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney < $enterminmony);
	&ERROROUT("你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

#初始化内容，回覆数
my($OUTPUT_TABLE,$REPLY_COUNT);
$addtimes = ($timedifferencevalue + $timezone)*3600;
#读取内容
$file_of_this_topic = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
open(FILE, "$file_of_this_topic") or &ERROROUT("这个主题不存在！可能已经被删除！");
@threads = <FILE>;
close(FILE);

(my $membername1, my $topictitle1, my $postipaddresstemp1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, my $posticon1) = split(/\t/, $threads[0]);

    if ($jfmark eq "yes") {
	if ($post1 =~m/\[jf=(.+?)\](.+?)\[\/jf\]/isg){ 
	    $jfpost=$1;
	    if (($jfpost <= $jifen)||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	    } else { 
	    &ERROROUT("由于主帖中设置有积分标签，所以无法快速查看，请点入后查看此帖，谢谢！") if ($noviewjf eq "yes");
   	    }
   	}
    }


shift(@threads);


@threads = reverse(@threads);
chomp @threads;
#取得文章总数
$TREPLY_COUNT = @threads;
$REPLY_COUNT = $TREPLY_COUNT+1;
my $numberofitems = $TREPLY_COUNT;
#取出主题文章
&ERROROUT("本主题没有任何回复。") unless(@threads);

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $topictitlemax = 85; } elsif ($tablewidth > 770) { $topictitlemax = 70; } else { $topictitlemax = 40; }
} else {
    if ($screenmode >=10) { $topictitlemax = 85; } elsif ($screenmode >=8) { $topictitlemax = 70; } else { $topictitlemax = 40; }
}

#分页//add by hztz
my $tempnumberofpages = $numberofitems / $maxtopics;
$numberofpages = int($tempnumberofpages);
$numberofpages++ if ($numberofpages != $tempnumberofpages);

if ($numberofpages > 1) {
	$startarray = $instart;
	$endarray = $instart + $maxtopics - 1;
	$endarray = $numberofitems - 1 if ($endarray >= $numberofitems);

	if ($replynum eq "last" && $treeview ne "yes") {
		$instart = ($numberofpages - 1) * $maxtopics;
		$startarray = $instart;
		$endarray = $numberofitems - 1;
	}

	my $currentpage = int($instart / $maxtopics) + 1;
	my $endstart = ($numberofpages - 1) * $maxtopics;
	my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<font face=webdings><span style=cursor:hand title="首 页" onclick="loadThreadFollows($inforum, \\\'$intopic&start=0\\\')">9</span></font>~;
	my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<font face=webdings><span style=cursor:hand title="尾 页" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$endstart\\\')">:</span></font>~;

	my $uppage = $currentpage - 1;
	my $nextpage = $currentpage + 1;
	my $upstart = $instart - $maxtopics;
	my $nextstart = $instart + $maxtopics;
	my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<font face=webdings><span style=cursor:hand title="第$uppage页" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$upstart\\\')">7</span></font>~;
	my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<font face=webdings><span style=cursor:hand title="第$nextpage页" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$nextstart\\\')">8</span></font>~;

	my $tempstep = $currentpage / 7;
	my $currentstep = int($tempstep);
	$currentstep++ if ($currentstep != $tempstep);
	my $upsteppage = ($currentstep - 1) * 7;
	my $nextsteppage = $currentstep * 7 + 1;
	my $upstepstart = ($upsteppage - 1) * $maxtopics;
	my $nextstepstart = ($nextsteppage - 1) * $maxtopics;
	my $showupstep = $upsteppage < 1 ? "" : qq~<span style=cursor:hand title="第$upsteppage页" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$upstepstart\\\')">←</span> ~;
	my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<span style=cursor:hand title="第$nextsteppage页" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$nextstepstart\\\')">→</span> ~;

	$pages = "";
	my $currentstart = $upstepstart + $maxtopics;
	for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
	{
		last if ($i > $numberofpages);
		$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<span style=cursor:hand onclick="loadThreadFollows($inforum, \\\'$intopic&start=$currentstart\\\')">$i</span> ~;
		$currentstart += $maxtopics;
	}
	$pages = "<font color=$menufontcolor>页次：<b><font color=$fonthighlight>$currentpage</font> / $numberofpages页</b> 每页最多 <font color=$fonthighlight>$maxtopics</font> 个 共 <font color=$fonthighlight>$numberofitems</font> 个 $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font>";
}
else {
	$startarray = 0;
	$endarray = $numberofitems - 1;
	$pages = "<font color=$menufontcolor>该主题的回复只有一页</font>";
}

$REPLY_COUNT = $REPLY_COUNT - $startarray;
#取得输出内容
foreach (@threads[$startarray .. $endarray]){
	my @postdata = split(/\t/,$_);
	#更新回覆数
	$REPLY_COUNT--;
	$OUTPUT_TABLE .= &OUTPUT_TABLE($postdata[0], $postdata[5], $postdata[6], $postdata[7]);
}
	$OUTPUT_TABLE .= qq(<br><br><DIV style="BORDER-RIGHT: black 1px solid; PADDING-RIGHT: 2px; BORDER-TOP: black 1px solid; PADDING-LEFT: 2px; PADDING-BOTTOM: 2px; MARGIN-LEFT: 18px; BORDER-LEFT: black 1px solid; WIDTH: 600px; COLOR: black; PADDING-TOP: 2px; BORDER-BOTTOM: black 1px solid; BACKGROUND-COLOR: lightyellow;text-align:center">[ $pages ]</DIV>);
OUTPUT_TREE($boardname,$OUTPUT_TABLE,0);


#输出显示
sub OUTPUT_TABLE{
	#取得内容，回覆者
	my ($OUTPUT_NAME, $OUTPUT_TIME, $OUTPUT_MSG, $OUTPUT_ICON) = @_;
	#处理文章内容
        $OUTPUT_TIME = &dateformat($OUTPUT_TIME + $addtimes);

    $OUTPUT_MSG =~ s/\[ADMINOPE=(.+?)\]//isg;
	if ($OUTPUT_MSG =~ /\[POSTISDELETE=(.+?)\]/) {
	    $OUTPUT_MSG = "此回复已经被屏蔽";
	}

        if (($OUTPUT_MSG =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/)||($OUTPUT_MSG =~ /LBSALE\[(.*?)\]LBSALE/)) {
            $OUTPUT_MSG = "保密";
        } else {
	    $OUTPUT_MSG =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	    $OUTPUT_MSG =~ s/\[quote\](.*)\[\/quote\]//isg;
	    $OUTPUT_MSG =~ s/\[equote\](.*)\[\/equote\]//isg;
	    $OUTPUT_MSG =~ s/\[fquote\](.*)\[\/fquote\]//isg;
	    $OUTPUT_MSG =~ s/\[hidepoll\]//isg;
	    $OUTPUT_MSG =~ s/\[这个(.+?)最后由(.+?)编辑\]\n//isg;
	    $OUTPUT_MSG =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
	    $OUTPUT_MSG =~ s/\[hide\](.*)\[\/hide\]//isg; 
	    $OUTPUT_MSG =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
	    $OUTPUT_MSG =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
	    $OUTPUT_MSG =~ s/\[jf=(.+?)\](.+?)\[\/jf\](.*)\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
	    $OUTPUT_MSG =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
	    $OUTPUT_MSG = &temppost("$OUTPUT_MSG");
	}
	
	if (length($OUTPUT_MSG)>=$topictitlemax) {
            $OUTPUT_MSG=&lbhz($OUTPUT_MSG,$topictitlemax);
	}

	$OUTPUT_MSG = "(无内容)" unless($OUTPUT_MSG ne "");
	#初始化输出内容
	my $OUTPUT_TABLE;
	#处理连结值
	my $START=0;my $SID=$REPLY_COUNT+1;
	if($REPLY_COUNT >= $maxtopics){
		my ($crelyid,undef)=split(/\./,($REPLY_COUNT/$maxtopics));
		$START=$crelyid*$maxtopics;
	}
	$SID="bottom" if($SID eq $TREPLY_COUNT+1);
	if (($OUTPUT_ICON eq "")||($OUTPUT_ICON =~ /\<br\>/i)) {
	    $OUTPUT_ICON = int(myrand(23));
    	    $OUTPUT_ICON = "0$OUTPUT_ICON" if ($OUTPUT_ICON<10);
	    $OUTPUT_ICON = "$OUTPUT_ICON.gif";
	}
	$OUTPUT_ICON = qq~<img src=$imagesurl/posticons/$OUTPUT_ICON $defaultsmilewidth $defaultsmileheight>~;

	#输出内容表格
	$REPLY_COUNT1 = $REPLY_COUNT+1;
	$OUTPUT_TABLE .= qq~<span style=width:100%><span style=width:58%>　　　　$OUTPUT_ICON　<a href=topic.cgi?forum=$inforum&topic=$intopic&start=$START#$SID target=_blank>$OUTPUT_MSG</a></span><span style=width:12%><a href=post.cgi?action=replyquote&forum=$inforum&topic=$intopic&postno=$REPLY_COUNT1 title=引用回复这个贴子 target=_blank><img src=$imagesurl/images/replynow.gif border=0 width=16 align=absmiddle></a></span><span style="width:14%">[ <span style="cursor:hand" onClick="javascript:O9('~ . ($uri_escape eq "no" ? $OUTPUT_NAME : uri_escape($OUTPUT_NAME)) . qq~')">$OUTPUT_NAME</span> ]</span><span style=width:14%>$OUTPUT_TIME</span>~;
	#处理输出内容
	$OUTPUT_TABLE =~ s/\n//g;
	$OUTPUT_TABLE =~ s/\'/\\\'/g;
	return "$OUTPUT_TABLE";
}

sub ERROROUT{
	my $ERROR_MSG = shift;
	my $OUTPUT_TABLE;
	$OUTPUT_TABLE .= qq(<DIV style="BORDER-RIGHT: black 1px solid; PADDING-RIGHT: 2px; BORDER-TOP: black 1px solid; PADDING-LEFT: 2px; PADDING-BOTTOM: 2px; MARGIN-LEFT: 18px; BORDER-LEFT: black 1px solid; WIDTH: 240px; COLOR: black; PADDING-TOP: 2px; BORDER-BOTTOM: black 1px solid; BACKGROUND-COLOR: lightyellow;cursor:hand" onclick="loadThreadFollow($inforum,$intopic,'$id_of_this_topid')">$ERROR_MSG</DIV>);
	$OUTPUT_TABLE =~ s/\n//g;
	$OUTPUT_TABLE =~ s/\'/\\\'/g;
	&OUTPUT_TREE($boardname,$OUTPUT_TABLE,1);
}

sub OUTPUT_TREE{
	my ($title,$output,$err) = @_;
	chomp $output;

	print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

print <<"HTML";
<html>
<head> 
<title>文章树</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
<SCRIPT>
<!--
//初始化内容值
parent.followTd$id_of_this_topid.innerHTML='$output';
//已读取
parent.document.images.followImg$id_of_this_topid.loaded='yes';
-->
</SCRIPT>
</body>
</html>
HTML
		
	exit;
}