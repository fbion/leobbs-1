#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

$versionnumber = "<b>L<font color=#F26522>eo</font>B<font color=#00AEEF>BS</font></b> X Build090208";

$ENV{"HTTP_CLIENT_IP"} = '' if ($ENV{"HTTP_CLIENT_IP"} !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
$ENV{"HTTP_X_FORWARDED_FOR"} = '' if ($ENV{"HTTP_X_FORWARDED_FOR"} !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
$ENV{'REMOTE_ADDR'} = $ENV{'HTTP_X_FORWARDED_FOR'} if (($ENV{'REMOTE_ADDR'} eq "127.0.0.1")&&($ENV{'HTTP_X_FORWARDED_FOR'} ne "")&&($ENV{'HTTP_X_FORWARDED_FOR'} ne "unknow"));
$skin = "leobbs" if ($skin eq "");

($memdir,$msgdir,$usrdir,$saledir) = split (/\|/, getdir());
&error("有问题&论坛中 cgi-bin 下的 members 目录不存在，请检查后继续！") if($memdir eq "");
&error("有问题&论坛中 cgi-bin 下的 messages 目录不存在，请检查后继续！") if($msgdir eq "");
&error("有问题&论坛中 non-cgi 下的 usr 目录不存在，请检查后继续！") if($usrdir eq "");
&error("有问题&论坛中 cgi-bin 下的 sale 目录不存在，请检查后继续！") if($saledir eq "");

sub dofilter {
    my $infiltermessage=shift;
    
    if (open (FILE, "${lbdir}data/wordfilter.cgi")) {
	$wordfilter = <FILE>;
	close (FILE);
	chomp $wordfilter;
	$wordfilter=~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
	$wordfilter=~ s/\t/\|/ig;
	$wordfilter=~ s/\|\|/\|/ig;
	$wordfilter=~ s/^\|//ig;
	$wordfilter=~ s/\|$//ig;
    }
    else { $wordfilter = "";}

    my $tempinfilter = $infiltermessage;
    if ($wordfilter) { $tempinfilter =~ s/$wordfilter/ *** /isg; }
    if ($tempinfilter ne $infiltermessage) { &error("有问题&你所写的内容中也许包含了一些本论坛不允许发布的言论，请仔细检查后，重新发布，谢谢！"); }
    $tempinfilter =~ s/\&nbsp\;//ig;
    $tempinfilter =~ s/\<.+?\>//ig;
    $tempinfilter =~ s/\[.+?\]//g;
    $tempinfilter =~ s/ |　|\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\]//g;
    my $tempinfilter1 = $tempinfilter;
    if ($wordfilter) { $tempinfilter1 =~ s/$wordfilter/ *** /isg; }
    if ($tempinfilter1 ne $tempinfilter) { &error("有问题&你所写的内容中也许包含了一些本论坛不允许发布的言论，请仔细检查后，重新发布，谢谢！！"); }

    if (open (FILE, "${lbdir}data/badwords.cgi")) {
	$badwords = <FILE>;
	close (FILE);
	$badwords=~ s/[\a\f\n\e\0\r\t]//ig;
	$badwords=~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
    }
    else { $badwords = "";}

    if ($badwords) {
        study($infiltermessage);
	my @pairs = split(/\&/,$badwords);
	foreach (@pairs) {
	    my ($bad, $good) = split(/=/,$_);
	    chomp $good;
	    $infiltermessage =~ s/$bad/$good/isg;
        }
    }
    return $infiltermessage;
}

sub checksearchbot {  #返回 0 = 搜索引擎访问 ，返回 1 = 非搜索引擎（或者不允许搜索引擎直接访问）
   return 1 if ($allowsearch ne "yes");
   my $useragent = $ENV{'HTTP_USER_AGENT'};
   foreach my $eachsearch ("Google","baiduspider","lycos","yahooseeker","MSNBOT","InfoSeek","Inktomi","Yahoo! Slurp")
   {
       return 0 if ($useragent =~ /$eachsearch/i);
   }
   return 1;
}

sub ipbanned {
    $inmembername = $query->cookie("amembernamecookie") if ($inmembername eq "");
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $infilemembername = $inmembername;
    $infilemembername =~ s/ /_/g;
    $infilemembername =~ tr/A-Z/a-z/;
    $infilemembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $ipaddress     = $ENV{"REMOTE_ADDR"};
    $trueipaddress = $ENV{"HTTP_CLIENT_IP"};
    $trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./ || $trueipaddress =~ m/a-z/i);
    $trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./ || $trueipaddress =~ m/a-z/i);
    $trueipaddress =~ s/\.\.//g;
    $trueipaddress =~ s/[a-z\\\/]//isg;
    $infilemembername = $trueipaddress if (($inmembername eq "")||($inmembername eq "客人"));
    if ((-e "${lbdir}cache/id/$infilemembername.cgi")&&((-M "${lbdir}cache/id/$infilemembername.cgi") *86400 < 1800)) {
    	#直接通过
    }
    else { require "doipbanned.pl"; }
}

sub title {
  if ($showskin ne "off") {
    eval{ require "${lbdir}data/skinselect.pl"; };
    if ($@) { 
    	require "${lbdir}dorepireskin.pl";
	print header();
	print "<script language='javascript'>javascript:this.location.reload()</script>";
        print "页面已经更新，程序自动刷新，如果没有自动刷新，请手工刷新一次！！<BR><BR><meta http-equiv='refresh' content='3;'>";
	exit;
    }
  } else { $userskins=""; $skinselect=""; }

    &doonoff;
    $newmail = "<p>";
    if ($inmembername eq "" || $inmembername eq "客人") {
	$inmembername = "客人";
	$loggedinas = qq~<b>客人</b>： <a href=loginout.cgi?forum=$inforum title=从这里开始进入论坛>登录</a> <img src=$imagesurl/images/fg.gif width=1> <a href=register.cgi?forum=$inforum title=注册了才能发表文章哦！><B><font color=$fonthighlight>按这里注册</font></B></a> <img src=$imagesurl/images/fg.gif width=1> <a href=profile.cgi?action=lostpassword title=好惨啊，忘记密码登录不了 style=cursor:help>忘记密码</a> <img src=$imagesurl/images/fg.gif width=1> <a href=whosonline.cgi title=看看有谁在线……>在线</a> <img src=$imagesurl/images/fg.gif width=1> <a href="search.cgi?forum=$inforum" title=按关键字、作者来搜寻>搜索</a> $skinselect<img src=$imagesurl/images/fg.gif width=1> <span style=cursor:hand onClick=javascript:openScript('help.cgi',500,400) title=常见问题的解答>帮助</span>&nbsp;~;
	if (($regaccess eq "on" && &checksearchbot)&&($thisprog ne "loginout.cgi")&&($thisprog ne "register.cgi")&&($thisprog ne "profile.cgi")&&($thisprog ne "viewavatars.cgi")) {
	    print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	    print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    exit;
	}
	if(($regpuonoff eq "ontop")&&($thisprog eq "leobbs.cgi")||($regpuonoff eq "oneach")&&($thisprog ne "loginout.cgi")&&($thisprog ne "register.cgi")) {
	    if ($boardlogo =~ /\.swf$/i) {$forumgraphic1 = qq~<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/myimages/$boardlogo quality=high width=$boardlogow height=$boardlogoh pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>~}
            else {$forumgraphic1 = qq~<img src=$imagesurl/myimages/$boardlogo border=0>~};		
            $popupmsg = qq~请先注册以避免此视窗出现~ if(!$popupmsg);
            $popupmsg = &HTML("$popupmsg");
	    $loggedinas .=qq~<script src="$imagesurl/images/lbpopup.js"></script><div id="lbplocation" style="position: absolute;visibility: hidden;height: 1;width: 1;top: 100;left: 50"><table width=520 height=320 bgcolor=$titleborder style="border: 1 outset $miscbackone"><tr><td><table width=490 height=290 bgcolor=$menubackground align=center style="border: 1 inset $miscbacktwo"><tr><td align=center valign=middle><a href=leobbs.cgi>$forumgraphic1</a><br>$popupmsg<br><br><b><a href=register.cgi title=按这里进行注册><U>注　册</U></a>　　<a href=loginout.cgi?forum=$inforum title=从这里开始进入论坛><U>登　入</U></a></b><p>(此视窗将于 5 秒后自动关闭)</td></tr></table></td></tr></table></div>~;
	}
    }
    else {
       if (($thisprog eq "leobbs.cgi")||($thisprog eq "forums.cgi")||($thisprog eq "topic.cgi")) {
	 $memberfilename = $inmembername;
	 $memberfilename =~ s/ /\_/g;
	 $memberfilename =~ tr/A-Z/a-z/;

  	 if ((-e "${lbdir}cache/mymsg/$memberfilename.pl")&&((-M "${lbdir}cache/mymsg/$memberfilename.pl") < (-M "${lbdir}$msgdir/in/${memberfilename}_msg.cgi"))) {
    	    eval{ require "${lbdir}cache/mymsg/$memberfilename.pl";};
    	    if ($@) { unlink ("${lbdir}cache/mymsg/$memberfilename.pl"); $totalmessages = 0;$unread = 0; }
  	 } else {
  	     require "domymsg.pl";
	 }
      }
      $loggedinas = qq~$inmembername：<a href=loginout.cgi?forum=$inforum>重登录</a> <img src=$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[1])" onMouseout="delayhidemenu()">控制面板</span> <img src=$imagesurl/images/fg.gif width=1> <a href=search.cgi?forum=$inforum title=按关键字、作者来搜寻论坛内的帖子>搜索</a> <img src=$imagesurl/images/fg.gif width=1> <a href=whosonline.cgi title=看看有谁在线……>在线</a> <img src=$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[0])" onMouseout="delayhidemenu()">论坛设施</span> $skinselect<img src=$imagesurl/images/fg.gif width=1> <span style=cursor:hand onClick="javascript:openScript('help.cgi',500,400)" title=常见问题的解答>帮助</span> <img src=$imagesurl/images/fg.gif width=1> <a href=loginout.cgi?action=logout title=在公众的地方上网记得要按退出哦><font color=$fonthighlight>退出</font></a>&nbsp;~;
    }

    if ($useadscript ne 0) {
        $adscript = &HTML("$adscript");
        $adscript =~ s/\$imagesurl/$imagesurl/isg;
	$adscript =~ s/\[br\]/\n/isg;
    }
    else { $adscript =""; }

    if ($thisprog eq "leobbs.cgi" && $adscriptmain ne "") {
        $adscriptmain = &HTML("$adscriptmain");
        $adscriptmain =~ s/\$imagesurl/$imagesurl/isg;
	$adscriptmain =~ s/\[br\]/\n/isg;
	$adscript = $adscriptmain;
    }

    if ($inforum eq "") {
        if ($boardlogo ne "") {
            if ($boardlogo =~ /\.swf$/i) {$forumgraphicoutput = qq~<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/myimages/$boardlogo quality=high width=$boardlogow height=$boardlogoh pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>~}
                else {$forumgraphicoutput = qq~<img src=$imagesurl/myimages/$boardlogo>~};
        }
    } else {
	if ($forumgraphic) {
	    ($fgwidth,$fgheight) = split(/\|/,$fgwidth);
	    if ($forumgraphic =~ /\.swf$/i) {$forumgraphicoutput = qq~<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/myimages/$forumgraphic quality=high width=$fgwidth height=$fgheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>~}
	        else {$forumgraphicoutput = qq~<a href=forums.cgi?forum=$inforum><img src=$imagesurl/myimages/$forumgraphic border=0></a>~};
	} else {
	    if ($boardlogo =~ /\.swf$/i) {$forumgraphicoutput = qq~<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/myimages/$boardlogo quality=high width=$boardlogow height=$boardlogoh pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>~}
	        else {$forumgraphicoutput = qq~<a href=forums.cgi?forum=$inforum><img src=$imagesurl/myimages/$boardlogo border=0></a>~};
	}
    }

    if (-e "${lbdir}data/skincache.pl") {
        eval{ require "${lbdir}data/skincache.pl";};
        if ($@) {  unlink ("${lbdir}data/skincache.pl"); }
    }
    $loggedinas .= qq~<img src=$imagesurl/images/fg.gif width=1> <a href=admin.cgi target=_blank>管理中心</a>&nbsp;~ if (($membercode eq "ad")||($membercode eq "smo"));

    if ($navadd ne "") {
    	$navadd=&HTML($navadd);
    	$loggedinas .= qq~<img src=$imagesurl/images/fg.gif width=1> $navadd&nbsp;~;
    }

    if ($thisprog eq "leobbs.cgi") {
    	$headmark = "$headmark1$headmark";
    	$footmark = "$footmark1$footmark";
    }
        

    if ($headmark ne "") { $headmark=&HTML($headmark); $headmark =~ s/\n/<BR>/isg; $headmark =~ s/\$imagesurl/$imagesurl/isg; $headmark =~ s/\[br\]/\n/isg; }
    if ($footmark ne "") { $footmark=&HTML($footmark); $footmark =~ s/\n/<BR>/isg; $footmark =~ s/\$imagesurl/$imagesurl/isg; $footmark =~ s/\[br\]/\n/isg;}

    if ($menubackpic ne "") { $menubackpic = "background=$imagesurl/images/$skin/$menubackpic"; }

    $output = qq~
<style>
.menuskin{position:absolute;background-color:$menubackground;border:1px solid $titleborder;line-height:20px;z-index:100;visibility:hidden;}
#mouseoverstyle{BACKGROUND-COLOR: #C9D5E7; margin:1px;}
#mouseoverstyle a{color:white;}
.menuitems{margin:1px;padding:1px;word-break:keep-all;}
</style>
<script>
linkset[1]='<div class=menuitems>&nbsp;<span style=cursor:hand onClick=javascript:openScript("messanger.cgi?action=new",600,400) title=发送悄悄话短讯息给站内的朋友>发短讯给朋友</span>&nbsp;</div><div class=menuitems>&nbsp;<a href=profile.cgi?action=modify title=编辑修改您的个人资料><font color=$menufontcolor>修改我的资料</font></a>&nbsp;</div><div class=menuitems>&nbsp;<a href=fav.cgi?action=show&member=$inmembername title=对您收藏的帖子进行管理><font color=$menufontcolor>管理我的收藏</font></a>&nbsp;</div><div class=menuitems>&nbsp;<span style=cursor:hand onClick=javascript:openScript("friendlist.cgi",420,320) title=查看、添加、删除你的好友名单>管理好友列表</span>&nbsp;</div><div class=menuitems>&nbsp;<span style=cursor:hand onClick=javascript:openScript("blocklist.cgi",420,320) title=查看、添加、删除你的黑名单>管理黑名单表</span>&nbsp;</div><div class=menuitems>&nbsp;<span style=cursor:hand onClick=javascript:openScript("recopr.cgi?action=new",420,320) title=显示论坛最新的帖子列表>论坛最新帖子</span>&nbsp;</div><div class=menuitems>&nbsp;<span style=cursor:hand onClick=javascript:openScript("recopr.cgi?action=post",420,320) title=我发表的、而且已经被别人回复过的主题列表>被回复的主题</span>&nbsp;</div><div class=menuitems>&nbsp;<span style=cursor:hand onClick=javascript:openScript("recopr.cgi?action=reply",420,320) title=我发表回复过的主题列表>我参与的主题</span>&nbsp;</div><div class=menuitems>&nbsp;<a href=delmycache.cgi title=清除我的缓存，确保个人所有资料都是最新的><font color=$menufontcolor>更新我的缓存</font></a>&nbsp;</div>'
</script>
$pluginadd$headmark$userskins~;
    if (($usesuperannounce eq "1")&&($thisprog eq "leobbs.cgi" || $thisprog eq "forums.cgi" || $thisprog eq "topic.cgi")) {
    	require "superannounce.pl";
    	&superanndo;
        $sann = qq~<span style=cursor:hand onClick=displayfadeinbox();><img src=$imagesurl/images/sann.gif height=16></span>　~;
    }

  eval{ require "${lbdir}data/myskin/${skin}.pl";};
  if ($@) { require "${lbdir}data/myskin/title.pl";}   # 调入头部 skin ，如果不存在或者错误，默认 title.pl 。

    if ($firstout eq "yemei") {
        $output .= $yemei if ($usetopm ne "no");
        $output .= $daohang;
    } else {
        $output .= $daohang;
        $output .= $yemei if ($usetopm ne "no");
    }

    $output .= qq~<base onmouseover="window.status='$statusbar';return true">~ if ($statusbar ne "");

    if ($forumlastvisit) {
	my $fulldate  = &fulldatetime($forumlastvisit+$timedifferencevalue*3600+$timezone*3600);
	$lastvisitdata = qq~ 最近访问论坛时间： $fulldate~;
    }
    else { $lastvisitdata = qq~ $forumname欢迎您的到来 ~; }
    $uservisitdata = qq~<a href=forums.cgi?forum=$inforum&action=resetposts title="$lastvisitdata">标记论坛所有内容为已读</a>&nbsp;~;
}

sub mischeader {
  local($misctype) = @_;

  if (-e "${lbdir}cache/forumstitle$inforum.pl") {
        eval{ require "${lbdir}cache/forumstitle$inforum.pl";};
        if ($@) { unlink ("${lbdir}cache/forumstitle$inforum.pl"); require "domischeader.pl"; }
  } else {
      require "domischeader.pl";
  }
  &title;
  if ($inforum eq "") { $titleoutput =~ s/\ →\ \<a href=forums.cgi\?forum=\>\<\/a\>//isg; $titleoutput =~ s/\>\>\>\ //isg; }
  $titleoutput =~ s/misctypehtc/$misctype/isg;
  $output .= qq~$titleoutput~;
}

sub getoneforum {
    local $inforum = shift;
    return if ($inforum eq "");
    if (-e "${lbdir}cache/forumsone$inforum.pl") {
        eval{ require "${lbdir}cache/forumsone$inforum.pl";};
        if ($@) { unlink ("${lbdir}cache/forumsone$inforum.pl"); require "dogetoneforum.pl"; }
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $no, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forums);
        unlink("${lbdir}cache/forumsone$inforum.pl") if ((-M "${lbdir}cache/forumsone$inforum.pl") *86400 > 600);
    } else {
    	require "dogetoneforum.pl";
    }
    $forummodnamestemp = ",$forummoderator,";
    my $tempinmembername = ",$inmembername,";
    $inmembmod = $forummodnamestemp =~ /\Q$tempinmembername\E/i || (($membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && ($forummodnamestemp =~ /,全体版主,/ || $forummodnamestemp =~ /,全体斑竹,/)) ? "yes" : "no";
    return;
}

sub moderator {
    local $inforum = shift;
    return if ($inforum eq "");
    if (-e "${lbdir}cache/forums$inforum.pl") {
        eval{ require "${lbdir}cache/forums$inforum.pl";};
        if ($@) { unlink ("${lbdir}cache/forums$inforum.pl"); require "domoderator.pl"; }
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $thisforums);

        if ($forummodnamestemp =~ /\Q\,$inmembername\,\E/i || (($membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && ($forummodnamestemp =~ /,全体版主,/ || $forummodnamestemp =~ /,全体斑竹,/))) { $inmembmod = "yes"; } else { $inmembmod = "no"; }
        unlink("${lbdir}cache/forums$inforum.pl") if ((-M "${lbdir}cache/forums$inforum.pl") *86400 > 600);
    } else {
    	require "domoderator.pl";
    }
    eval{ require "${lbdir}boarddata/forumposts$inforum.pl";} if ($thisprog eq "forums.cgi");
    return;
}

sub checkmemfile {
    my ($nametocheck, $namenumber) = @_;
    if (-e "${lbdir}$memdir/$nametocheck.cgi") {
        my @fileinfo = stat("${lbdir}$memdir/$nametocheck.cgi");
        my $filelength = $fileinfo[7];
    	if ($filelength <=50) { unlink("${lbdir}$memdir/$nametocheck.cgi"); }
    	else {
    	    if ($loadcopymo ne 1) { eval('use File::Copy;'); $loadcopymo = 1; }
    	    copy("${lbdir}$memdir/$nametocheck.cgi","${lbdir}$memdir/$namenumber/$nametocheck.cgi");
    	    unlink("${lbdir}$memdir/$nametocheck.cgi");
    	}
    }

    my @fileinfo = stat("${lbdir}$memdir/$namenumber/$nametocheck.cgi");
    my $filelength = $fileinfo[7];
    if ((!(-e "${lbdir}$memdir/$namenumber/$nametocheck.cgi"))||($filelength <=50)) {
    	if (-e "${lbdir}$memdir/old/$nametocheck.cgi") {
    	    if ($loadcopymo ne 1) { eval('use File::Copy;'); $loadcopymo = 1; }
    	    copy("${lbdir}$memdir/old/$nametocheck.cgi","${lbdir}$memdir/$namenumber/$nametocheck.cgi");
    	}
    }
}

sub getnamenumber {
    my $nametocheck = shift;
#    my $namenumber = int((ord(substr($nametocheck,0,1))+ord(substr($nametocheck,1,1)))/2);
    my $namenumber = ((ord(substr($nametocheck,0,1))&0x3c)<<3)|((ord(substr($nametocheck,1,1))&0x7c)>>2);
    mkdir ("${lbdir}$memdir/$namenumber", 0777) if (!(-e "${lbdir}$memdir/$namenumber"));
    chmod(0777,"${lbdir}$memdir/$namenumber");
    return $namenumber;
}

sub getmember {
    my ($nametocheck, $readtype) = @_;
    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck,$namenumber);
    $userregistered = "";
    undef $filedata;
    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";

    if ($readtype eq "check") {
	if ((-e $filetoopen)&&($nametocheck !~ /^客人/)&&($nametocheck ne "")) {
	    return 1;
	} else {
	    return 0;
	}
    }

    if ((-e $filetoopen)&&($nametocheck !~ /^客人/)&&($nametocheck ne "")) {
	&winlock($filetoopen) if (($OS_USED eq "Nt") && ($readtype ne "no"));
        open(FILE3,"$filetoopen");
        flock(FILE3, 1) if (($OS_USED eq "Unix") && ($readtype ne "no"));
        my $filedata = <FILE3>;
        close(FILE3);
	&winunlock($filetoopen) if (($OS_USED eq "Nt") && ($readtype ne "no"));
	chomp($filedata);
	($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount,$ebankdata,$onlinetime,$userquestion,$awards,$jifen,$userface,$soccerdata,$useradd5) = split(/\t/,$filedata);
	$mymoney = int($mymoney);
	$showemail = "no" if ($dispmememail eq "no");
	$membername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	$password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
	if (($password !~ /^lEO/)&&($password ne "")) {
	    eval {$password = md5_hex($password);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$password = md5_hex($password);');}
	    unless ($@) {$password = "lEO$password";}
	}
	$membercode ||= "me";
	$jhcount = "0" if ($jhcount <= 0);
	$jhcount ||= "0";
	$visitno ||= "0";
	$onlinetime = "3000" if ($onlinetime < 0);
	($signatureorigin, $signaturehtml) = split(/aShDFSiod/,$signature); 
	$signatureorigin =~ s/<br>/\n/g; 
	$timedifferencevalue = $timedifference;
	($numberofposts, $numberofreplys) = split(/\|/,$numberofposts);
	$numberofposts ||= "0";
	$numberofreplys ||= "0";
	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
	}

        chomp $privateforums;
        if ($privateforums) {
	    my @private = split(/&/,$privateforums);
	    foreach (@private) {
		chomp $_;
		($access, $value) = split(/=/,$_);
		$allowedentry{$access} = $value;
	    }
	}
	return 1;
    }
    else { $userregistered = "no"; $membercode =""; return 0;}
}

sub numerically { $a <=> $b }
sub alphabetically { lc($a) cmp lc($b) }
sub whosonline {
	my $instruct = shift;
	(local $tempusername, local $where, local $method, local $where2) = split(/\t/, $instruct);
	local $ipaddress  = $ENV{'REMOTE_ADDR'};
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	local $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
	local $ipall      = "$ipaddress=$trueipaddress";
	local $tempusername1=$tempusername;
	$tempusername = "客人($ipaddress)" if ($tempusername eq "客人");
	$totleonlineall = 0;
	$guests  = 0;
	$members = 0;
	$onlineuserlist       = "\_";
	$onlineuserlisthidden = "\_";
	undef @onlinedata;
	undef @onlinedata1;
	$currenttime = time;
	$membergone = 15 if (($membergone < 5)||($membergone > 180));
	my $userexpire = $currenttime - $membergone * 60;
	$memberprinted = "no";
	$screenmode=8 if ($screenmode eq "");
	local $firstcome = 'yes';
	
     my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
     my @fileinfo = stat("$filetoopen");
     my $filelength1 = $fileinfo[7];
        @fileinfo = stat("$filetoopen.cgi");
     my $filelength2 = $fileinfo[7];
     if ((($filelength1 <60)&&($filelength2 > 60))||(($filelength2-$filelength1>1200)&&($filelength2<3000))||(($filelength2 > $filelength1*1.2)&&($filelength2>=3000)&&($filelength2<80000))||(($filelength2 > $filelength1*1.5)&&($filelength2>=80000))) {
	if (open(FILE5,"$filetoopen.cgi")) {
  	  sysread(FILE5, $onlinedata1,(stat(FILE5))[7]);
	  close(FILE5);
	  $onlinedata1 =~ s/\r//isg;
	}
     }
     else {
        &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        if (open(FILE5,"$filetoopen")) {
	  flock (FILE5, 1) if ($OS_USED eq "Unix");
  	  sysread(FILE5, $onlinedata1,(stat(FILE5))[7]);
	  close(FILE5);
	  $onlinedata1 =~ s/\r//isg;
	}
        &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        unlink ("${lbdir}data/onlinedata.cgi.cgi") if ((-M "${lbdir}data/onlinedata.cgi.cgi") *86400 > 100);
     }

        @onlinedata1=split(/\n/,$onlinedata1);
        $onlinedatanumber=@onlinedata1;
	local @onlinefr = ();
	local $onlineprompt = $query->cookie('onlineprompt') if (defined($query));
        foreach my $line (@onlinedata1) {
                chomp $line;
                local ($savedusername, $savedcometime, $savedtime, $savedwhere, $savedipaddress, $saveosinfo, $savebrowseinfo, $savedwhere2, $fromwhere, $savemembercode, $savehidden, $savesex) = split(/\t/, $line);
 		my ($lookfor, $no) = split(/\(/,$savedusername);
                next if (((length($savedusername)>12)&&($lookfor ne "客人"))||($lookfor eq ""));
                $fromwhere = "未知" if (length($fromwhere) > 40);
#                $saveosinfo = "未知" if (length($saveosinfo) > 15);
#                $savebrowseinfo = "未知" if (length($savebrowseinfo) > 28);
		$lookfor =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/ /isg;
		$savedwhere =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/ /isg;
		$savedwhere2 =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/ /isg;
		$fromwhere =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/ /isg;

                $savedusername =~ s/\_/ /g;
                $tempusername =~ s/\_/ /g;

		if ($userexpire <= $savedtime) {
		    if ($savedusername !~ /^客人/) { if ($savehidden ne 1) { $onlineuserlist = "$onlineuserlist$savedusername\_"; } else { $onlineuserlisthidden = "$onlineuserlisthidden$savedusername\_"; } }
                    if ((lc($savedusername) eq lc($tempusername))||(($savedusername eq "客人($ipaddress)")&&($ipall eq $savedipaddress)&&($tempusername =~ /^客人/ || ($where eq "论坛登录" && $where2 eq "登录论坛" && $action eq "login")))) {
                         if ((($currenttime - $savedtime) <= $banfreshtime - 1)&&(($currenttime - $savedtime) >= 0)&&($savedwhere eq $where)&&($savedwhere2 eq $where2)&&(($thisprog eq "post.cgi")||($thisprog eq "leobbs.cgi")||($thisprog eq "forums.cgi")||($thisprog eq "topic.cgi")||($thisprog eq "printpage.cgi")||($thisprog eq "whosonline.cgi"))) {
                             print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
                             print "<BR>服务器忙，请 $banfreshtime 秒后按刷新键继续。<BR><BR>出错原因：你刷新页面过快，或者你打开了过多窗口来浏览本网站。";
                             exit;
                         }
                         $savedcometime = $currenttime if (lc($savedusername) ne lc($tempusername));
                         if ($memberprinted eq "no") {
                             $savehidden = $hidden if ($hidden ne "");
                             $tempdata = "$tempusername\t$savedcometime\t$currenttime\t$where\t$ipall\t$saveosinfo\t$savebrowseinfo\t$where2\t$fromwhere\t$membercode\t$savehidden\t$sex\t" ;
			     $osinfo=$saveosinfo;
	   		     $browseinfo=$savebrowseinfo;
                             $tempdata =~ s/[\a\f\n\e\0\r]//isg;
                             $fromwhere1 = $fromwhere;
                             push(@onlinedata,$tempdata);
                             $memberprinted = "yes";
			     $firstcome = 'no' if (lc($savedusername) eq lc($tempusername));
                             $onlinetimeadd = $currenttime - $savedcometime;
                         }
                    }
                    else {
                         $line =~ s/[\a\f\n\e\0\r]//isg;
                         push(@onlinedata,$line);
			 if ($tempusername !~ /^客人/ && $friendonlinepop ne 'no') {
			     $savedusernametemp = $savedusername;
			     $savedusernametemp =~ s/\\\|\(\)\[\]\*\+\?//isg;
			     if ($onlineprompt =~ /,$savedusername,/i) {
				push(@onlinefr, $savedusername);
				$onlineprompt =~ s/,$savedusername,/,/isg;
			     }
			 }
                    }
                }
                else {
                	if ($savedusername !~ /^客人/) { require "douplogintime.pl"; &uplogintime("$savedusername",""); }
                }
        }

	if ($tempusername !~ /^客人/ && $friendonlinepop ne 'no') {
	     require "doonlinepop.pl";
	}

        if ($memberprinted eq "no") {
            require "domemberprint.pl";
        }

my $filetoopens = "${lbdir}data/counter.cgi";
$filetoopens = &lockfilename($filetoopens);
if ((!(-e "$filetoopens.lck"))||($thisprog eq "leobbs.cgi")||($thisprog eq "index.cgi")) {
    require "docounter.pl";
}
$guesttotle = 0;

        if ($method ne "none") {
	    $memberoutput = qq~<script>
function OLO(img, name, name1, place, action, time, time1, os, browser, ip, where, xa, xb) {document.write("<td width=12 align=center><img src=$imagesurl/images/" + img + " border=0 width=12 align=absmiddle alt='发送一个短消息给 " + name + "' onClick=\\"javascript:openScript('messanger.cgi?action=new&touser=" + name1 + "', 600, 400)\\" style='cursor: hand'></td><td width=108><span onClick=\\"javascript:O9('" + name1 + "')\\" nowarp title=\\"目前位置：" + place + "\\n目前动作：" + action + "\\n来访时间：" + time + "\\n活动时间：" + time1 + "\\n操作系统：" + os + "\\n浏 览 器：" + browser + "\\nＩＰ地址：" + ip + "\\n来源鉴定：" + where + "\\" style='cursor: hand'>" + xa + name + xb + "</span></td>");}
function OHO(time, time1, ip, where, xa, xb) {document.write("<td width=12 align=center><img src=$imagesurl/images/$onlineguest width=12 align=absmiddle alt='请勿打扰！'></td><td width=108><a href=# nowarp title=\\"来访时间：" + time + "\\n活动时间：" + time1 + "\\nＩＰ地址：" + ip + "\\n来源鉴定：" + where + "\\">" + xa + "隐身会员" + xb + "</a></td>");}
~;
	    $memberoutput1 = qq~<script>
function OGO(place, action, time, time1, os, browser, ip, where, xa, xb) {document.write("<td width=12 align=center><img src=$imagesurl/images/$onlineguest border=0 width=12 align=absmiddle alt='快注册呀！'></td><td width=108><a href=# nowarp title=\\"目前位置：" + place + "\\n目前动作：" + action + "\\n来访时间：" + time + "\\n活动时间：" + time1 + "\\n操作系统：" + os + "\\n浏 览 器：" + browser + "\\nＩＰ地址：" + ip + "\\n来源鉴定：" + where + "\\">" + xa + "客人" + xb + "</a></td>");}
~;

            foreach my $line (@onlinedata) {
                chomp $line;
		$line =~ s/＊＃！＆＊//;
                my ($savedusername, $savedcometime, $savedtime, $savedwhere, $postipaddresstemp, $saveosinfo, $sa达5 ne "" ? $defrzonline5 : $onlinerz;}
		    else  {$mspic=$onlinemember;}

		($savedipaddress,$truepostipaddress) = split(/\=/,$postipaddresstemp);
		$totleonlineall++;

		$fromwhere = "�����ñ���" unless (($pvtip eq "on")||($membercode eq "ad")||(($membercode eq 'smo')&&($smocanseeip eq "no")));

			if ($membercode eq "smo") {
				$savedipaddress = "�����ñ���" unless ($pvtip eq "on" || $smocanseeip eq "no");
			}
			elsif ($membercode eq "cmo" || $membercode eq "mo") {
				if ($pvtip eq "on") {
					my ($ip1, $ip2, $ip3, $ip4) = split(/\./, $savedipaddress);
					$savedipaddress = "$ip1.$ip2.$ip3.*";
				} else {
					$savedipaddress = "�����ñ���";
				}
			}
			elsif ($membercode ne "ad") {
				if ($pvtip eq "on" && $inmembername ne "����") {
					my ($ip1, $ip2, $ip3, $ip4) = split(/\./, $savedipaddress);
					$savedipaddress = "$ip1.$ip2.*.*";
				} else {
					$savedipaddress = "�����ñ���";
				}
			}

		    my $savedcometime = &dateformatshort($savedcometime + ($timezone+$timedifferencevalue)*3600);
		    my $savedtime = &dateformatshort($savedtime + ($timezone+$timedifferencevalue)*3600);

		    $savedwhere2 =~s/\<a \s*(.*?)\s*\>\s*(.*)/��$2��/isg;
		    $savedwhere2=~s/<a href=(.*?)>//isg;
		    $savedwhere2 =~s/\<\/a\>//isg;
		    $savedwhere2 =~s/\<b\>//isg;
		    $savedwhere2 =~s/\<\/b\>//isg;
		    $savedwhere2 =~s/\<\/br\>//isg;
		    $savedwhere2 =~s/\"/\\\"/isg;
		    if ($method=~/\<\>/) {
			my @method=split(/\<\>/,$method);
			chomp @method;
			$method=$method[0];
			$method_b=$method[1];
		    }
		    my $check_of_method_b=1;
		    my $wherebaomi = $method . "(��)";
		    my $wherebaomi_b = $method_b . "(��)";
		    if ($method_b ne "") {
			$check_of_method_b=($savedwhere2 eq $method_b)?1:0;
			$check_of_method_b=($savedwhere2 eq $wherebaomi_b)?1:0 if(!$check_of_method_b);
		    }

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $screenmodes = 10; } elsif ($tablewidth > 770) { $screenmodes = 8; } else { $screenmodes = 6; }
} else {
    $screenmodes = $screenmode;
}

 
			if (($savedwhere eq $method && $check_of_method_b) || ($savedwhere eq $wherebaomi && $check_of_method_b) || $method eq "both")
			{
				if ((($hiddened eq 1 && $membercode ne "ad") || ($savedusername =~ /^����/)) && (lc($savedusername) ne lc($inmembername)))
				{
					$XA = $XB = "";
					if (lc($savedusername) eq lc($inmembername) || $savedusername eq "����($trueipaddress)") {
						$XA = "<font color=$onlineselfcolor>";
						$XB = "</font>";
					}
					if ($hiddened eq 1) {
						$members++;
						$memberoutput .= qq~\nOHO("$savedcometime","$savedtime","$savedipaddress","$fromwhere","$XA","$XB")~;
						$memberoutput .= qq~\n</script></tr><tr>\n<script>~ if ($members == int($members / $screenmodes) * $screenmodes);
					} else {
						$guests++;
						$memberoutput1 .= qq~\nOGO("$savedwhere ","$savedwhere2 ","$savedcometime","$savedtime","$saveosinfo","$savebrowseinfo","$savedipaddress","$fromwhere","$XA","$XB")~;
						$memberoutput1 .= qq~\n</script></tr><tr>\n<script>~ if ($guests == int($guests / $screenmodes) * $screenmodes);
					}
				} else {
					$members++;
					my $cleanmember = $savedusername;
					$cleanmember =~ s/ /\_/g;
					$cleanmember =~ tr/A-Z/a-z/;
					$cleanmember = uri_escape($cleanmember);
					$XA = $XB = "";
					$XA = "<font color=$mcolor>" if ($savesex eq "m");
					$XA = "<font color=$fcolor>" if ($savesex eq "f");
					if (lc($savedusername) eq lc($inmembername)) {
						$XA = "<font color=$onlineselfcolor>";
						$XB = "</font>";
					}
					if ($hiddened eq 1) { $hiddeninfo = "\\n-=> Ŀǰ��������״̬ <=-"; } else { $hiddeninfo = ""; }
					
					$memberoutput .= qq~\nOLO("$mspic","$savedusername","$cleanmember","$savedwhere ","$savedwhere2 ","$savedcometime","$savedtime","$saveosinfo","$savebrowseinfo","$savedipaddress","$fromwhere$hiddeninfo","$XA","$XB")~;
					$memberoutput .= qq~\n</script></tr><tr>\n<script>~ if ($members == int($members / $screenmodes) * $screenmodes);
				}
			}
		}
		$memberoutput  .= qq~\n<\/script>\n~;
		$memberoutput1 .= qq~\n<\/script>\n~;
		$memberoutput1 = "" if ($dispguest eq 3 || ($dispguest ne 2 && $members > 50 && $guests > 20));
		$memberoutput = "$memberoutput</tr><tr>" if ($memberoutput ne "" && $memberoutput1 ne "");
		$memberoutput .= $memberoutput1;
		undef $memberoutput1;
		my $totleonline = $members + $guests;
		$membertongji = $method eq "both" ? "Ŀǰ�ܹ��� <a href=whosonline.cgi><b>$totleonlineall</b></a> �����ߡ�����ע���û� <b>$members</b> �ˣ��ÿ� <b>$guests</b> �ˡ�" : "&nbsp;Ŀǰ��̳������ <b>$totleonlineall</b> �ˣ�������̳���� <b>$totleonline</b> �����ߡ�����ע���û� <b>$members</b> �ˣ��ÿ� <b>$guests</b> �ˡ�";
	}
	if (&checksearchbot) {
	  if ($maxguests > 0 && $memberprinted eq "no" && $tempusername =~ /^����/ && $thisprog ne "loginout.cgi") {
	    if ($guesttotle > $maxguests + 1) {
	    	$guesttotle --;
	    	&error("��������&����̳������������Ϊ $maxguests ����Ŀǰ������Ϊ $guesttotle �������㲻���Կ������ݷ��ʣ�<BR><BR><a href=register.cgi><font color=$fonthighlight>�밴��ע��</font></a>��<a href=loginout.cgi><font color=$fonthighlight>���˵�¼</font></a>���ٷ��ʱ���̳�����������Ĳ��㣬���Ǹ�⣡<BR><BR>&guestiii");
	    }
	  }
	}
        
        my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
        $filetoopens = &lockfilename($filetoopen);
  	if (!(-e "$filetoopens.lck")) {
            $onlinedata = join("\n",@onlinedata);
	    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            if (open(FILE4,">$filetoopen")) {
              flock(FILE4, 2) if ($OS_USED eq "Unix");
              print FILE4 "$onlinedata";
              close(FILE4);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            my $nowsize = length($onlinedata);
	    unlink ("${lbdir}data/onlinedata.cgi.cgi") if ((-M "${lbdir}data/onlinedata.cgi.cgi") *86400 >= 60);
            if ((!(-e "${lbdir}data/onlinedata.cgi.cgi"))&&($nowsize > 2000)) {
             if (open(FILE4,">${filetoopen}.cgi")) {
              print FILE4 "$onlinedata";
              close(FILE4);
             }
            }
        }
	else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 60);
	}

	undef @onlinedata if (($thisprog ne "whosonline.cgi")&&($thisprog ne "leobbs.cgi"));
	return;
}

sub output {
        my ($title, $output, $outtype) = @_;
        $title =~ s/\$/\&\#036\;/sg;

	if (-e "${lbdir}data/template/$skin.cgi") {
	    open(FILE,"${lbdir}data/template/$skin.cgi");
	} else {
	    open(FILE,"${lbdir}data/template/title.cgi");
	}
  	sysread(FILE, my $templatedata,(stat(FILE))[7]);
        close(FILE);
	$templatedata =~ s/\r//isg;

    	my $boardcopyright;
	my $copyright;
	if ($outtype ne "msg") {
 	    $procedurecopy = &HTML("$procedurecopy");
            if ($procedurecopy eq "") { $procedurecopy = qq~$cssprocedure~;}
 	    $boardcopyright = qq(&copy\; $copyrightinfo) if $copyrightinfo;
            $boardcopyright =~ s/&lt;/</g; $boardcopyright =~ s/&gt;/>/g; $boardcopyright =~ s/&quot;/\"/g;
            $copyright = qq~<center>~;

            if (($thisprog eq "topic.cgi")||($thisprog eq "forums.cgi")) {
		if ($useadfoot ne 0) {
		    $adfoot   = &HTML("$adfoot");
		    $adfoot   =~ s/\$imagesurl/$imagesurl/isg;
		    $adfoot   =~ s/\[br\]/\n/isg;
		}
		else { $adfoot =""; }
	    	$copyright .= $adfoot;
	    }

	$beian =~ s/\s//isg;
	if ($beian =~ /icp/i) {
		$boardcopyright = "$boardcopyright�� ��<a href=http://www.miibeian.gov.cn/ target=_blank>$beian</a>";
	}

	    $copyright .= qq~<hr width=390 size=1><table width=80% align=center cellpadding=0 cellspacing=0><tr><td align=center>~;
	    $boardlastinfo =qq~<BR>����̳���۴��������߸����������<font color=$fonthighlight><b> $boardname </b></font>�����޹�<br>~ if ($dispboardsm ne "no");
	    if ($noads ne "yes") { if ($regerid =~ m/^LEO/) {eval {$regerid = md5_hex($regerid);}; if ($@) {eval('use Digest::MD5 qw(md5_hex);$regerid = md5_hex($regerid);');};$regerid = "" if ($regerid =~ m/^LEO/);} else { $regerid = ""; }; $regerid = substr($regerid,8,16) if ($regerid ne ""); $copyright1 = qq~<BR><font color=$postfontcolorone>�����Ȩ���У�ɽӥ(��)������ȱ�� �汾��<a href="http://www.leobbs.com/download" target=_blank title="���˿����������°汾��̳����">$versionnumber</a></font></td><td width=10>&nbsp;</td><td width=28><a href=http://www.leobbs.com/leobbs/reg/reg.asp?id=$regerid target=_blank><img src=$imagesurl/images/leoca.gif width=32 height=24 border=0 title=�װ����ᳬ����̳��֤></a>~;}
       	    $copyright .= qq~<table cellpadding=0 cellspacing=0 align=center><tr><td align=center><font color=$fontcolormisc>$boardcopyright$copyright1</td></tr></table><img src=$imagesurl/images/none.gif width=0 height=3>$boardlastinfo</font></td></tr></table></center>\n$footmark~;
	}
	else { undef $copyright; }

if ($coolclickdisp eq "1") {
    $coolclick = qq~<script src="$imagesurl/images/adv.js"></SCRIPT>
<script>Adv("","","","<img src=$imagesurl/images/leobbs.gif alt=���ᳬ����̳ border=0>","���ᳬ����̳ -- ��ʾ��Ϣ");</script>
<script>Adv("","");</script>
~;
} else { $coolclick = ""; }
if (($thisprog eq "topic.cgi")||($thisprog eq "profile.cgi")) {
    $coolclick .= qq~<script src="$imagesurl/images/show.js"></SCRIPT>~;
}

$coolmeta = qq~<META http-equiv="Page-Enter" content="revealTrans(Transition=$cinoption,Duration=1)">
<META http-equiv="Page-Exit" content="revealTrans(Transition=$cinoption,Duration=1)">~ if ($pagechange eq "yes");

$coolmeta .= qq~
<link title="$title" type="application/rss+xml" rel="alternate" href="rss.cgi?/leo.xml"></link>
~ ;
study($templatedata);
$templatedata=~ s/\$lbbody/$lbbody/;
$templatedata=~ s/\$page_title/$title/;
$templatedata=~ s/\$coolmeta/$coolmeta/;
$templatedata=~ s/\$coolclick/$coolclick/;
$templatedata=~ s/\$tablewidth/$tablewidth/;
$templatedata=~ s/\$imagesurl/$imagesurl\/images/isg;
$templatedata=~ s/\$lbboard_main/$onlinepopup$$output\n\n$copyright\n/;
$templatedata=~ s/\<meta name=keywords content=\"/<meta name=\"description\" content=\"$newkeywords\">\n<meta name=keywords content=\"$title\,$newkeywords\,/i;

if (($usefake eq "yes") && ($thisprog eq "leobbs.cgi" || $thisprog eq "loginout.cgi" || $thisprog eq "forums.cgi" || $thisprog eq "category.cgi" || $thisprog eq "postings.cgi" || $thisprog eq "post.cgi" || $thisprog eq "poll.cgi" || $thisprog eq "recopr.cgi")) {
    $templatedata =~ s/profile.cgi\?action=show&member=([^\"\+\ ]+?)([\ \'\"\>])/profile-$1.htm$2/isg;

    $templatedata =~ s/forums.cgi\?forum=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/forums-$1-$2.htm$3/isg;
    $templatedata =~ s/forums.cgi\?forum=([0-9]+?)([\ \'\"\>])/forums-$1-0.htm$2/isg;

    $templatedata =~ s/leobbs.cgi\?action=(.+?)([\ \'\"\>])/leobbs-$1.htm$2/isg;
    $templatedata =~ s/([\=\'\"\/])leobbs.cgi/${1}leobbs.htm/isg;

    $templatedata =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)&start=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/topic-$1-$2-$3-$4-.htm$5/isg;
    $templatedata =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/topic-$1-$2-0-$3-.htm$4/isg;
    $templatedata =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)&replynum=([^\"\+\ ]+?)([\ \'\"\>])/topic-$1-$2-0-0-$3.htm$4/isg;
    $templatedata =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)([\ \'\"\>])/topic-$1-$2-0-0-.htm$3/isg;

    $templatedata =~ s/announcements.cgi\?forum=([0-9]+?)/announcements-$1.htm/isg;
    $templatedata =~ s/announcements.cgi/announcements.htm/isg;

}

print $templatedata;
if (($cpudisp eq "1")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo")) {
    $spenttime = sprintf("%.2f",((times)[0]+(times)[1]-$startingtime)*1000);
    print "<center><font color=$cpudispcolor>��ǰҳ��ִ������ʱ�䣺 $spenttime ���롡";
    unless ($usegzip ne 'yes' || $gzipused ne "1") { print "[Gzip: On, Level: $complevel]"; } else { print "[Gzip: Off]"; }
}
exit;
}

sub doonoff { #$mainoff ����$mainonoff������̳
    return if ($membercode eq "ad");
    if (($mainoff == 2)&&($mainonoff ne 2)) {
	$mainoff = 1;
	my (undef, undef, $hour, $mday, undef, undef, $wday, undef) = localtime(time + $timezone * 3600);
	$mainautovalue =~ s/[^\d\-]//sg;
	my ($starttime, $endtime) = split(/-/, $mainautovalue);
	if ($mainauto eq "day") {
	    $mainoff = 0 if ($hour == $starttime && $endtime eq "");
	    $mainoff = 0 if ($hour >= $starttime && $hour < $endtime);
	}
	elsif ($mainauto eq "week") {
	    $wday = 7 if ($wday == 0);
	    $mainoff = 0 if ($wday == $starttime && $endtime eq "");
	    $mainoff = 0 if ($wday >= $starttime && $wday <= $endtime);
	}
	elsif ($mainauto eq "month") {
	    $mainoff = 0 if ($mday == $starttime && $endtime eq "");
	    $mainoff = 0 if ($mday >= $starttime && $mday <= $endtime);
	}
    }
    if ($mainonoff == 2) {
	$mainonoff = 1;
	my (undef, undef, $hour, $mday, undef, undef, $wday, undef) = localtime(time + $timezone * 3600);
	$mainautovalue1 =~ s/[^\d\-]//sg;
	my ($starttime, $endtime) = split(/-/, $mainautovalue1);
	if ($mainauto1 eq "day") {
	    $mainonoff = 0 if ($hour == $starttime && $endtime eq "");
	    $mainonoff = 0 if ($hour >= $starttime && $hour < $endtime);
	}
	elsif ($mainauto1 eq "week") {
	    $wday = 7 if ($wday == 0);
	    $mainonoff = 0 if ($wday == $starttime && $endtime eq "");
	    $mainonoff = 0 if ($wday >= $starttime && $wday <= $endtime);
	}
	elsif ($mainauto1 eq "month") {
	    $mainonoff = 0 if ($mday == $starttime && $endtime eq "");
	    $mainonoff = 0 if ($mday >= $starttime && $mday <= $endtime);
	}
    }

    if (($mainoff == 1)||($mainonoff == 1)) { require "doinmaintenance.pl"; }
}

sub error {
    my $errorinfo = shift;
    (my $where, my $errormsg,my $ismsg) = split(/\&/, $errorinfo);
    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
    $inpassword = cookie("apasswordcookie");
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
    $sann = "";
    if ($ismsg ne "msg") {
	&title;
	$output =~ s/\<script src=\"$imagesurl\/images\/lbpopup.js\"><\/script>//isg if ($ismsg eq "guestiii");

	if ($indexforum ne "no") {
	    $output .= qq~<BR><table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> �� ���� $where</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>~;
	} else {
	    $output .= qq~<BR><table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font color=$navfontcolor>���� $where</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>~;
	}
    }
    else {
	$output = "";
    }
if ($catbackpic !~ /^background\=/)  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

    $output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellpadding=6 cellspacing=1 width=100%>~;
    
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>���� $where</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
<b>����$where����ϸԭ��</b>
<ul><li><b>$errormsg</b>
<li>���Ƿ���Ҫ�鿴<span style="cursor:hand" onClick="javascript:openScript('help.cgi',500,400)">�����ļ�</span>?
</ul><b>����$where����Ŀ���ԭ��</b>
<ul><li>�������<li>�û�������<li>������<a href="register.cgi" >ע��</a>�û�</ul>
<br><br><center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">������һҳ</a></center>
</tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
~;
    &output($boardname,\$output,"$ismsg");
    exit;
}

sub myip {
    my $ipaddress      = $ENV{'REMOTE_ADDR'};
    my $trueipaddress  = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress     = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress     = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i &&  $trueipaddress1 !~ m/^192\.168\./ &&  $trueipaddress1 !~ m/^10\./);
    return "$ipaddress=$trueipaddress";
}

1;
