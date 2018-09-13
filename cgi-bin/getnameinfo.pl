#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use warnings;
use strict;
use diagnostics;

$onloadinfopl = 1;

sub getmemberinfo {
    $membername = shift;

    require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
    require "data/membertitles.cgi" if ($mtitlemax eq "" || $mpostmarkmax eq "");

    $userregistered = "";
    undef $filedata;
    my $namenumber = &getnamenumber($membername);
    &checkmemfile($membername, $namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$membername.cgi";
    if ((-e $filetoopen) && ($membername !~ /^客人/) && ($membername ne "")) {
        unlink("${lbdir}cache/meminfo/$membername.pl") if ((-M "${lbdir}cache/meminfo/$membername.pl") * 86400 > 60 * 5);
        open(FILE3, "$filetoopen");
        my $filedata = <FILE3>;
        close(FILE3);
        chomp($filedata);
        ($membername{$membername}, undef, $membertitle{$membername}, $membercode{$membername}, $numberofposts{$membername}, my $emailaddress, my $showemail, undef, my $homepage, my $oicqnumber, my $icqnumber, $location{$membername}, undef, $joineddate{$membername}, undef, $signature{$membername}, undef, undef, $useravatar{$membername}, $userflag{$membername}, $userxz, $usersx, my $personalavatar, my $personalwidth, my $personalheight, $rating{$membername}, $lastgone{$membername}, my $visitno, my $useradd04, $useradd02{$membername}, $mymoney{$membername}, my $postdel, my $sex, undef, undef, undef, undef, undef, undef, $jhmp{$membername}, $jhcount{$membername}, my $ebankdata, my $onlinetime, my $userquestion, $awards{$membername}, $jifen{$membername}, $userface, my $soccerdata, my $useradd5) = split(/\t/, $filedata);
        $mymoney{$membername} = int($mymoney{$membername});
        #	($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount,$ebankdata,$onlinetime,$userquestion,$awards,$jifen,$userface,$soccerdata,$useradd5) = split(/\t/,$filedata);

        $membername{$membername} = $tempmname if ($membername{$membername} eq "");
        $lastgone{$membername} = $joineddate{$membername} if ($lastgone{$membername} eq ""); # 最后访问时间
        $lastgone{$membername} = &dateformat($lastgone{$membername} + $addtimes);
        $showemail = "no" if ($dispmememail eq "no");
        $membercode{$membername} ||= "me";
        $jhcount{$membername} = "0" if ($jhcount{$membername} <= 0);
        $onlinetime = "3000" if ($onlinetime < 0);
        ($signatureorigin{$membername}, $signaturehtml{$membername}) = split(/aShDFSiod/, $signature{$membername});
        $signatureorigin{$membername} =~ s/<br>/\n/g;
        ($numberofposts, $numberofreplys) = split(/\|/, $numberofposts{$membername});
        $numberofposts ||= "0";
        $numberofreplys ||= "0";
        $postdel ||= "0";
        $location{$membername} = "保密" if ($location{$membername} eq "");

        if ($joineddate{$membername}) {$joineddate{$membername} = &dateformat($joineddate{$membername} + $addtimes);}
        else {$joineddate{$membername} = "未知";}

        $jifen{$membername} = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf if ($jifen{$membername} eq "");

        $numberofposts{$membername} = $numberofposts + $numberofreplys;
        if (!$numberofposts{$membername}) {$numberofposts{$membername} = 0;}

        if ($jifen{$membername} >= $mpostmarkmax) {
            $mtitle{$membername} = $mtitlemax;
            $membergraphic{$membername} = $mgraphicmax;
        }
        elsif ($jifen{$membername} >= $mpostmark19) {
            $mtitle{$membername} = $mtitle19;
            $membergraphic{$membername} = $mgraphic19;
        }
        elsif ($jifen{$membername} >= $mpostmark18) {
            $mtitle{$membername} = $mtitle18;
            $membergraphic{$membername} = $mgraphic18;
        }
        elsif ($jifen{$membername} >= $mpostmark17) {
            $mtitle{$membername} = $mtitle17;
            $membergraphic{$membername} = $mgraphic17;
        }
        elsif ($jifen{$membername} >= $mpostmark16) {
            $mtitle{$membername} = $mtitle16;
            $membergraphic{$membername} = $mgraphic16;
        }
        elsif ($jifen{$membername} >= $mpostmark15) {
            $mtitle{$membername} = $mtitle15;
            $membergraphic{$membername} = $mgraphic15;
        }
        elsif ($jifen{$membername} >= $mpostmark14) {
            $mtitle{$membername} = $mtitle14;
            $membergraphic{$membername} = $mgraphic14;
        }
        elsif ($jifen{$membername} >= $mpostmark13) {
            $mtitle{$membername} = $mtitle13;
            $membergraphic{$membername} = $mgraphic13;
        }
        elsif ($jifen{$membername} >= $mpostmark12) {
            $mtitle{$membername} = $mtitle12;
            $membergraphic{$membername} = $mgraphic12;
        }
        elsif ($jifen{$membername} >= $mpostmark11) {
            $mtitle{$membername} = $mtitle11;
            $membergraphic{$membername} = $mgraphic11;
        }
        elsif ($jifen{$membername} >= $mpostmark10) {
            $mtitle{$membername} = $mtitle10;
            $membergraphic{$membername} = $mgraphic10;
        }
        elsif ($jifen{$membername} >= $mpostmark9) {
            $mtitle{$membername} = $mtitle9;
            $membergraphic{$membername} = $mgraphic9;
        }
        elsif ($jifen{$membername} >= $mpostmark8) {
            $mtitle{$membername} = $mtitle8;
            $membergraphic{$membername} = $mgraphic8;
        }
        elsif ($jifen{$membername} >= $mpostmark7) {
            $mtitle{$membername} = $mtitle7;
            $membergraphic{$membername} = $mgraphic7;
        }
        elsif ($jifen{$membername} >= $mpostmark6) {
            $mtitle{$membername} = $mtitle6;
            $membergraphic{$membername} = $mgraphic6;
        }
        elsif ($jifen{$membername} >= $mpostmark5) {
            $mtitle{$membername} = $mtitle5;
            $membergraphic{$membername} = $mgraphic5;
        }
        elsif ($jifen{$membername} >= $mpostmark4) {
            $mtitle{$membername} = $mtitle4;
            $membergraphic{$membername} = $mgraphic4;
        }
        elsif ($jifen{$membername} >= $mpostmark3) {
            $mtitle{$membername} = $mtitle3;
            $membergraphic{$membername} = $mgraphic3;
        }
        elsif ($jifen{$membername} >= $mpostmark2) {
            $mtitle{$membername} = $mtitle2;
            $membergraphic{$membername} = $mgraphic2;
        }
        elsif ($jifen{$membername} >= $mpostmark1) {
            $mtitle{$membername} = $mtitle1;
            $membergraphic{$membername} = $mgraphic1;
        }
        else {
            $mtitle{$membername} = $mtitle0;
            $mgraphic0 = "none.gif" if ($mgraphic0 eq "");
            $membergraphic{$membername} = $mgraphic0;
        } #显示默认等级
        $membergraphic{$membername} = "<img src=$imagesurl/images/$membergraphic{$membername} border=0>";

        $numberofposts{$membername} = qq~<font title='发表数：$numberofposts\n回复数：$numberofreplys\n被删数：$postdel'>$numberofposts{$membername}</font>~;

        if ($avatars eq "on") {
            if (($personalavatar) && ($personalwidth) && ($personalheight)) {
                #自定义头像存在
                $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
                if (($personalavatar =~ /\.swf$/i) && ($flashavatar eq "yes")) {
                    $personalavatar = uri_escape($personalavatar);
                    $useravatar{$membername} = qq(&nbsp;<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
                    $vheight{$membername} = $personalheight + 190;
                }
                else {
                    $personalavatar = uri_escape($personalavatar);
                    $useravatar{$membername} = qq(&nbsp;<img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
                    $vheight{$membername} = $personalheight + 190;
                }
            }
            elsif (($useravatar{$membername} ne "noavatar") && ($useravatar{$membername})) {
                $vheight{$membername} = $defaultheight + 190;
                $defaultwidth = "width=$defaultwidth" if ($defaultwidth ne "");
                $defaultheight = "height=$defaultheight" if ($defaultheight ne "");
                $useravatar{$membername} = uri_escape($useravatar{$membername});
                $useravatar{$membername} = qq(&nbsp;<img src=$imagesurl/avatars/$useravatar{$membername}.gif $defaultwidth $defaultheight>);
            }
            else {
                if (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) {
                    $vheight{$membername} = 310;
                    $useravatar{$membername} = qq~&nbsp;<img src=http://qqshow-user.tencent.com/$oicqnumber/11/00/ title="QQ 秀形象" border=0 width=70 height=113>~;
                }
                else {
                    $useravatar{$membername} = "<BR>";
                    $vheight{$membername} = 190;
                }
            }
            if ($userface ne '') {
                my ($currequip, $x, $loadface) = split(/\|/, $userface);
                if ($loadface eq 'y') {
                    $useravatar{$membername} = qq~<SCRIPT>Face_Info("$currequip","$imagesurl");</SCRIPT>~;
                    $vheight{$membername} = 410;
                }
            }
        }

        $sxall = "子鼠丑牛寅虎卯兔辰龙巳蛇午马未羊申猴酉鸡戌狗亥猪";
        $xzall = "白羊金牛双子巨蟹狮子处女天秤天蝎射手魔羯水瓶双鱼";

        my $tempmembername = uri_escape($membername);
        $pvmsggraphic{$membername} = qq~<span style=cursor:hand onClick="javascript:openScript('messanger.cgi?action=new&touser=$tempmembername&actionto=msg',600,400)" title="发送一个短消息给$membername{$membername}"><img src=$imagesurl/images/message.gif border=0 width=16 align=absmiddle>消息</span>　~;
        $searchgraphic{$membername} = qq~<a href="search.cgi?action=startsearch&TYPE_OF_SEARCH=username_search&NAME_SEARCH=topictitle_search&FORUMS_TO_SEARCH=$in_forum&SEARCH_STRING=$tempmembername" target=_blank title="搜索$membername{$membername}在本分论坛的全部贴子"><img src=$imagesurl/images/find.gif border=0 width=16 align=absmiddle>搜索</a>　~;
        $profilegraphic{$membername} = qq~<a href=profile.cgi?action=show&member=$tempmembername title="查看$membername{$membername}的个人资料" target=_blank><img src=$imagesurl/images/profile.gif border=0 width=16 align=absmiddle>查看</a>　~;
        $friendgraphic{$membername} = qq~<span style=cursor:hand onClick="javascript:openScript('friendlist.cgi?action=adduser&adduser=$tempmembername',420,320)" title="加$membername{$membername}为我的好友"><img src=$imagesurl/images/friend.gif border=0 width=16 align=absmiddle>好友</span>　~;
        $emailaddress = &encodeemail($emailaddress);
        if ($showemail eq "yes") {$emailgraphic{$membername} = "<a href=mailto:$emailaddress title=电子邮件地址><img src=$imagesurl/images/email.gif border=0 width=16 align=absmiddle></a>　";}
        elsif ($showemail eq "msn") {$emailgraphic{$membername} = "<a href=mailto:$emailaddress title=\"MSN 地址\"><img src=$imagesurl/images/msn.gif border=0 width=16 align=absmiddle></a>　";}
        elsif ($showemail eq "popo") {$emailgraphic{$membername} = "<a href=mailto:$emailaddress title=网易泡泡><img src=$imagesurl/images/popo.gif border=0 width=16 align=absmiddle></a>　";}
        else {$emailgraphic{$membername} = "";}
        $homepage =~ s/http\:\/\///sg;

        if ($homepage) {$homepagegraphic{$membername} = qq~<a href=http://$homepage target=_blank title="访问 $membername{$membername} 的主页"><img src=$imagesurl/images/homepage.gif border=0 width=16 align=absmiddle></a>　~;}
        else {$homepagegraphic{$membername} = "";}
        #    if (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) { $oicqgraphic{$membername} = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicqnumber target=_blank title="查看 QQ:$oicqnumber的资料" atta="<img src=http://qqshow-user.tencent.com/$oicqnumber/10/00/>"><img src=$imagesurl/images/oicq.gif border=0 width=16 align=absmiddle> </a>&nbsp;~; } else { $oicqgraphic=""; }
        if (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) {$oicqgraphic{$membername} = qq~<a target=blank href=http://wpa.qq.com/msgrd?V=1&Uin=$oicqnumber&Site=$boardname&Menu=yes><img border="0" SRC=http://wpa.qq.com/pa?p=1:$oicqnumber:4 alt="发送即时消息给$membername" width=16></a> ~;}
        else {$oicqgraphic = "";}
        if (($icqnumber) && ($icqnumber =~ /[0-9]/)) {$icqgraphic{$membername} = qq~<span style="cursor:hand" onClick="javascript:openScript('misc.cgi?action=icq&UIN=$icqnumber',450,300)" title="给 ICQ:$icqnumber 发个消息"><img src=$imagesurl/images/icq.gif border=0 width=16 align=absmiddle></span>　~;}
        else {$icqgraphic = "";}

        if ($membercode{$membername} eq "ad") {
            $posterfontcolor{$membername} = "$adminnamecolor";
            $glowing{$membername} = $adminglow;
            $membernameimg{$membername} = "<img src=$imagesurl/images/teamad.gif alt=此人为坛主 width=16 align=absmiddle>";
            $membergraphic{$membername} = "<img src=$imagesurl/images/$admingraphic width=100 border=0>" if ($admingraphic ne "");
            $mtitle{$membername} = $adtitle if ($adtitle ne "");
            if (($membertitle{$membername} eq "Member") || ($membertitle{$membername} eq "member")) {$membertitle{$membername} = "论坛坛主";}
        }
        elsif ($membercode{$membername} eq "mo") {
            $posterfontcolor{$membername} = "$teamnamecolor";
            $glowing{$membername} = $teamglow;
            $membernameimg{$membername} = "<img src=$imagesurl/images/teammo.gif alt=此人为版主 width=16 align=absmiddle>";
            $membergraphic{$membername} = "<img src=$imagesurl/images/$modgraphic width=100 border=0>" if ($modgraphic ne "");
            $mtitle{$membername} = $motitle if ($motitle ne "");
            if (($membertitle{$membername} eq "Member") || ($membertitle{$membername} eq "member")) {$membertitle{$membername} = "论坛版主";}
        }
        elsif ($membercode{$membername} eq "cmo") {
            $posterfontcolor{$membername} = "$cmonamecolor";
            $glowing{$membername} = $cmoglow;
            $membernameimg{$membername} = "<img src=$imagesurl/images/teamcmo.gif alt=此人为分类区版主 width=16 align=absmiddle>";
            $membergraphic{$membername} = "<img src=$imagesurl/images/$cmodgraphic width=100 border=0>" if ($cmodgraphic ne "");
            $mtitle{$membername} = $cmotitle if ($cmotitle ne "");
            if (($membertitle{$membername} eq "Member") || ($membertitle{$membername} eq "member")) {$membertitle{$membername} = "分类区版主";}
        }
        elsif ($membercode{$membername} eq "amo") {
            $posterfontcolor{$membername} = "$amonamecolor";
            $glowing{$membername} = $amoglow;
            $membernameimg{$membername} = "<img src=$imagesurl/images/teamamo.gif alt=此人为论坛副版主 width=16 align=absmiddle>";
            $membergraphic{$membername} = "<img src=$imagesurl/images/$amodgraphic width=100 border=0>" if ($amodgraphic ne "");
            $mtitle{$membername} = $amotitle if ($amotitle ne "");
            if (($membertitle{$membername} eq "Member") || ($membertitle{$membername} eq "member")) {$membertitle{$membername} = "论坛副版主";}
        }
        elsif ($membercode{$membername} eq "smo") {
            $posterfontcolor{$membername} = "$smonamecolor";
            $glowing{$membername} = $smoglow;
            $membernameimg{$membername} = "<img src=$imagesurl/images/teamsmo.gif alt=此人为总版主 width=16 align=absmiddle>";
            $membergraphic{$membername} = "<img src=$imagesurl/images/$smodgraphic width=100 border=0>" if ($smodgraphic ne "");
            $mtitle{$membername} = $smotitle if ($smotitle ne "");
            if (($membertitle{$membername} eq "Member") || ($membertitle{$membername} eq "member")) {$membertitle{$membername} = "总版主";}
        }
        elsif ($membercode{$membername} =~ /^rz/) {
            $posterfontcolor{$membername} = $rznamecolor;
            $glowing{$membername} = $rzglow;
            my $teampic = $membercode{$membername} eq "rz1" && $defrz1 ne "" && $defrzpic1 ne "" ? $defrzpic1 : $membercode{$membername} eq "rz2" && $defrz2 ne "" && $defrzpic2 ne "" ? $defrzpic2 : $membercode{$membername} eq "rz3" && $defrz3 ne "" && $defrzpic3 ne "" ? $defrzpic3 : $membercode{$membername} eq "rz4" && $defrz4 ne "" && $defrzpic4 ne "" ? $defrzpic4 : $membercode{$membername} eq "rz5" && $defrz5 ne "" && $defrzpic5 ne "" ? $defrzpic5 : "teamrz.gif";
            my $teamname = $membercode{$membername} eq "rz1" && $defrz1 ne "" ? $defrz1 : $membercode{$membername} eq "rz2" && $defrz2 ne "" ? $defrz2 : $membercode{$membername} eq "rz3" && $defrz3 ne "" ? $defrz3 : $membercode{$membername} eq "rz4" && $defrz4 ne "" ? $defrz4 : $membercode{$membername} eq "rz5" && $defrz5 ne "" ? $defrz5 : "认证用户";
            $membernameimg{$membername} = qq~<img src=$imagesurl/images/$teampic alt="此人为$teamname" width=16 align=absmiddle>~;
        }
        elsif ($membercode{$membername} eq "banned") {
            $posterfontcolor{$membername} = "$posternamecolor";
            $glowing{$membername} = $banglow;
            $membergraphic{$membername} = "";
            $jhmp{$membername} = "";
            $membertitle{$membername} = "&nbsp;<b>已被禁止发言</b><BR>";
            $membernameimg{$membername} = "";
        }
        elsif ($membercode{$membername} eq "masked") {
            $posterfontcolor{$membername} = "$posternamecolor";
            $glowing{$membername} = $banglow;
            $membergraphic{$membername} = "";
            $jhmp{$membername} = "";
            $membertitle{$membername} = "&nbsp;<b>发言已被屏蔽</b><BR>";
            $membernameimg{$membername} = "";
        }
        else {
            $posterfontcolor{$membername} = "$posternamecolor";
            $membernameimg{$membername} = "";
            $glowing{$membername} = $memglow;
        }

        if ($membertitle{$membername} eq "member" || $membertitle{$membername} eq "Member" || $membertitle{$membername} eq "") {$membertitle{$membername} = "";}
        else {$membertitle{$membername} = "&nbsp;头衔: $membertitle{$membername}<br>" if (($membercode{$membername} ne "banned") && ($membercode{$membername} ne "masked"));}

        $membertitle{$membername} =~ s/&lt;/</g;
        $membertitle{$membername} =~ s/&gt;/>/g;
        $membertitle{$membername} =~ s/&quot;/"/g;

        if (($rating{$membername} !~ /^[0-9\-]+$/) || ($rating{$membername} eq "")) {$rating{$membername} = 0;}
        if ($rating{$membername} > 0) {$rating{$membername} = "+$rating{$membername}";}

        if ($jhmp{$membername} eq "无门无派" || $jhmp{$membername} eq "") {$jhmp{$membername} = "<BR>";}
        else {$jhmp{$membername} = "&nbsp;门派: $jhmp{$membername}<br>";}

        my $tempuseradd3 = $awards{$membername};
        $tempuseradd3 =~ s/://isg;
        if ($tempuseradd3 ne "") {
            my $showaward1 = $showaward2 = $showaward3 = $showaward4 = $showaward5 = $showaward6 = "";
            my ($tuseradd1, $tuseradd2, $tuseradd3, $tuseradd4, $tuseradd5, $tuseradd6) = split(/:/, $awards{$membername});
            if ((open(FILE2, "${lbdir}data/cityawards.cgi")) && ($loadawards ne 1)) {
                @tempawards = <FILE2>;
                close(FILE2);
                $loadawards = 1;
            }
            foreach $tempaward (@tempawards) {
                chomp $tempaward;
                next if ($tempaward eq "");
                my ($tempawardname, $tempawardurl, $tempawardinfo, $tempawardorder, $tempawardpic) = split(/\t/, $tempaward);
                if ($tuseradd1 eq $tempawardname) {
                    $tempawardname1 = $tempawardname;
                    $tempawardinfo1 = $tempawardinfo;
                    $tempawardpic1 = $tempawardpic;
                }
                if ($tuseradd2 eq $tempawardname) {
                    $tempawardname2 = $tempawardname;
                    $tempawardinfo2 = $tempawardinfo;
                    $tempawardpic2 = $tempawardpic;
                }
                if ($tuseradd3 eq $tempawardname) {
                    $tempawardname3 = $tempawardname;
                    $tempawardinfo3 = $tempawardinfo;
                    $tempawardpic3 = $tempawardpic;
                }
                if ($tuseradd4 eq $tempawardname) {
                    $tempawardname4 = $tempawardname;
                    $tempawardinfo4 = $tempawardinfo;
                    $tempawardpic4 = $tempawardpic;
                }
                if ($tuseradd5 eq $tempawardname) {
                    $tempawardname5 = $tempawardname;
                    $tempawardinfo5 = $tempawardinfo;
                    $tempawardpic5 = $tempawardpic;
                }
                if ($tuseradd6 eq $tempawardname) {
                    $tempawardname6 = $tempawardname;
                    $tempawardinfo6 = $tempawardinfo;
                    $tempawardpic6 = $tempawardpic;
                }
                last if ($tempaward eq "");
            }
            if ($tuseradd1 ne "") {$showaward1 = "<IMG height=15 src=$imagesurl/awards/$tempawardpic1 alt=$tempawardname1,$tempawardinfo1 align=absmiddle>"}
            if ($tuseradd2 ne "") {$showaward2 = "<IMG height=15 src=$imagesurl/awards/$tempawardpic2 alt=$tempawardname2,$tempawardinfo2 align=absmiddle>"}
            if ($tuseradd3 ne "") {$showaward3 = "<IMG height=15 src=$imagesurl/awards/$tempawardpic3 alt=$tempawardname3,$tempawardinfo3 align=absmiddle>"}
            if ($tuseradd4 ne "") {$showaward4 = "<IMG height=15 src=$imagesurl/awards/$tempawardpic4 alt=$tempawardname4,$tempawardinfo4 align=absmiddle>"}
            if ($tuseradd5 ne "") {$showaward5 = "<IMG height=15 src=$imagesurl/awards/$tempawardpic5 alt=$tempawardname5,$tempawardinfo5 align=absmiddle>"}
            if ($tuseradd6 ne "") {$showaward6 = "<IMG height=15 src=$imagesurl/awards/$tempawardpic6 alt=$tempawardname6,$tempawardinfo6 align=absmiddle>"}
            $showawards{$membername} = "&nbsp;<font color=$postfontcolortwo>勋章:</font> $showaward1 $showaward2 $showaward3 $showaward4 $showaward5 $showaward6<br>";
            $vheight{$membername} = $vheight{$membername} + 15;
        }
        else {
            $showawards{$membername} = "";
        }

        $mymoney{$membername} = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney{$membername} - $postdel * $delmoney + $jhcount{$membername} * $addjhhb;
        $mymoney{$membername} = "<font title=$mymoney>>9999999999999" if ($mymoney{$membername} > 9999999999999);
        $mymoney{$membername} = "$mymoney{$membername} $moneyname";

        $userflag{$membername} = "blank" if ($userflag{$membername} eq "");
        $userflag{$membername} = qq~　<img src=$imagesurl/flags/$userflag{$membername}.gif height=14 alt=$userflag{$membername} align=absmiddle>~;

        if ($usersx !~ /^sx/i) {$showsx{$membername} = "";}
        else {
            $usersx =~ s/sx//i;
            $showsx{$membername} = substr($sxall, ($usersx - 1) * 4, 4);
            $showsx{$membername} = "<IMG src=$imagesurl/sx/sx${usersx}s.gif height=15 alt=$showsx{$membername} align=absmiddle>";
        }
        if ($userxz !~ /^z/i) {$showxz{$membername} = "";}
        else {
            $userxz =~ s/z//i;
            $showxz{$membername} = substr($xzall, ($userxz - 1) * 4, 4);
            $showxz{$membername} = "<IMG src=$imagesurl/star/z$userxz.gif height=15 alt=$showxz{$membername}座 align=absmiddle>";
        }

        if ($sex eq "m") {$seximages{$membername} = "<img src=$imagesurl/images/mal.gif width=20 alt=帅哥 align=absmiddle>";}
        elsif ($sex eq "f") {$seximages{$membername} = "<img src=$imagesurl/images/fem.gif width=20 alt=美女 align=absmiddle>";}
        else {$seximages{$membername} = "";}

        $onlinetimehour{$membername} = int($onlinetime / 3600);
        $onlinetimemin{$membername} = int(($onlinetime % 3600) / 60);
        $onlinetimesec{$membername} = int(($onlinetime % 3600) % 60);
        $onlinetimehour{$membername} = "0$onlinetimehour{$membername}" if ($onlinetimehour{$membername} < 10);
        $onlinetimemin{$membername} = "0$onlinetimemin{$membername}" if ($onlinetimemin{$membername} < 10);
        $onlinetimesec{$membername} = "0$onlinetimesec{$membername}" if ($onlinetimesec{$membername} < 10);

        ($mystatus, $mysaves{$membername}, $mysavetime, $myloan{$membername}, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
        unless ($mystatus eq "1" || $mystatus eq "-1" || $ebankdata eq "") {
            $mysaves{$membername} = "没开户";
            $myloan{$membername} = "没贷款";
        }
        else {
            if ($mystatus) {
                $mysaves{$membername} .= " $moneyname";
                if ($myloan{$membername}) {
                    $myloan{$membername} .= " $moneyname";
                }
                else {
                    $myloan{$membername} = "没贷款";
                }
            }
            else {
                $mysaves{$membername} = "没开户";
                $myloan{$membername} = "没贷款";
            }
        }
        $mysaves{$membername} = "<font title=$mysaves>>9999999999999" if ($mysaves{$membername} > 9999999999999);
        $myloan{$membername} = "<font title=$myloan>>9999999999999" if ($myloan{$membername} > 9999999999999);
        if ($signaturehtml{$membername}) {$signature{$membername} = $signaturehtml{$membername};}
        else {if ($idmbcodestate eq 'on') {
            require "dosignlbcode.pl";
            $signature{$membername} = &signlbcode($signatureorigin{$membername});
        }}
        #    $signature{$membername} =~ s/"/\'/isg;
        $saveinfofile++;

        my ($mywin, $mydraw, $mylose, $myplay, $myget) = split(/:/, $soccerdata);
        $mywin = 0 if ($mywin eq "");
        $mydraw = 0 if ($mydraw eq "");
        $mylose = 0 if ($mylose eq "");
        $myplay = 0 if ($myplay eq "");
        $myget = 0 if ($myget eq "");
        my $soccerwinrate = 0;
        $soccerwinrate = sprintf("%.2f", $mywin * 100 / ($mywin + $mydraw + $mylose)) if (($mywin + $mydraw + $mylose) > 0);
        $soccerinfo{$membername} = "";
        if (($mywin + $mydraw + $mylose) > 0) {
            $soccerinfo{$membername} = "<span title='胜率: $soccerwinrate%\n历史投注: $myplay $moneyname\n历史收益: $myget $moneyname'><b>$mywin</b> 胜 <b>$mydraw</b> 平 <b>$mylose</b> 负</span>";
            $vheight{$membername} = $vheight{$membername} + 15;
        }

        if ((!(-e "${lbdir}cache/meminfo/$membername.pl")) && ($saveinfofile <= 3) && ($inselectstyle eq $skinselected)) {

            my $homepagegraphic = $homepagegraphic{$membername};
            my $membernameimg = $membernameimg{$membername};
            my $membertitle = $membertitle{$membername};
            my $useravatar = $useravatar{$membername};
            my $mtitle = $mtitle{$membername};
            my $location = $location{$membername};
            my $jhmp = $jhmp{$membername};
            my $signature = $signature{$membername};

            $homepagegraphic =~ s/\\/\\\\/isg;
            $membernameimg =~ s/\\/\\\\/isg;
            $membertitle =~ s/\\/\\\\/isg;
            $useravatar =~ s/\\/\\\\/isg;
            $mtitle =~ s/\\/\\\\/isg;
            $location =~ s/\\/\\\\/isg;
            $jhmp =~ s/\\/\\\\/isg;
            $signature =~ s/\\/\\\\/isg;

            $homepagegraphic =~ s/~/\\\~/isg;
            $membernameimg =~ s/~/\\\~/isg;
            $membertitle =~ s/~/\\\~/isg;
            $useravatar =~ s/~/\\\~/isg;
            $mtitle =~ s/~/\\\~/isg;
            $location =~ s/~/\\\~/isg;
            $jhmp =~ s/~/\\\~/isg;
            $signature =~ s/~/\\\~/isg;

            $homepagegraphic =~ s/\$/\\\$/isg;
            $membernameimg =~ s/\$/\\\$/isg;
            $membertitle =~ s/\$/\\\$/isg;
            $useravatar =~ s/\$/\\\$/isg;
            $mtitle =~ s/\$/\\\$/isg;
            $location =~ s/\$/\\\$/isg;
            $jhmp =~ s/\$/\\\$/isg;
            $signature =~ s/\$/\\\$/isg;

            $homepagegraphic =~ s/\@/\\\@/isg;
            $membernameimg =~ s/\@/\\\@/isg;
            $membertitle =~ s/\@/\\\@/isg;
            $useravatar =~ s/\@/\\\@/isg;
            $mtitle =~ s/\@/\\\@/isg;
            $location =~ s/\@/\\\@/isg;
            $jhmp =~ s/\@/\\\@/isg;
            $signature =~ s/\@/\\\@/isg;
            $signature =~ s/^aShDFSiod//isg;
            $signature =~ s/aShDFSiod$//isg;

            if (-e "${lbdir}pet.cgi") {
                eval {require "${lbdir}petdata/config.pl";} if ($pet_open eq "");
                if ($pet_open eq 'open') {
                    if (-e "${lbdir}petdata/pet/$membername.cgi" || -e "${lbdir}petdata/pet/$membername{$membername}.cgi") {
                        my $file = "";
                        if (-e "${lbdir}petdata/pet/$membername.cgi") {
                            open(file, "${lbdir}petdata/pet/$membername.cgi");
                            $file = <file>;
                            close(file);
                        }
                        elsif (-e "${lbdir}petdata/pet/$membername{$membername}.cgi") {
                            open(file, "${lbdir}petdata/pet/$membername{$membername}.cgi");
                            $file = <file>;
                            close(file);
                        }

                        my $pet_zt;
                        my $pet_style;
                        my ($pet_name, $pet_jb, $x, $pet_sx, $pet_born, $pet_win, $pet_lose, $pet_gjl, $pet_fyl, $pet_exp, $pet_hp, $pet_sp, $x, $x, $x, $x, $x, $x, $x, $x, $pet_die, $x, $x, $pet_xz_time) = split(/\t/, $file);
                        $pet_xz_time or $pet_xz_time = $pet_born;
                        $pet_born = int((time - $pet_born) / 86400) + 1;
                        if (time - $pet_xz_time > 86400 * 3) {$pet_xz_time = "身上痒痒的，快给我洗澡吧";}
                        else {$pet_xz_time = '很舒服，不用洗澡了';}
                        if ($pet_sp < 0) {$pet_zt .= '(我好久没吃东西了)';}
                        elsif ($pet_sp < 500) {$pet_zt .= '(我快饿死了)';}
                        elsif ($pet_sp < 1000) {$pet_zt .= '(我好饿啊)';}
                        elsif ($pet_sp < 2000) {$pet_zt .= '(我好想吃东西)';}
                        else {$pet_zt .= '(我好饱哦)';}

                        my $pet_exp1 = int(sqrt($pet_exp) / 6);
                        $pet_exp1 = 110 if ($pet_exp1 > 110);
                        $pet_exp1 = qq~<img src=$imagesurl/images/jy_left.gif width=2 height=8><img src=$imagesurl/images/jy_0.gif width=$pet_exp1 height=8 alt="经验: $pet_exp"><img src=$imagesurl/images/jy_right.gif width=4 height=8>~;

                        my $pet_hp1 = int(sqrt($pet_hp));
                        $pet_hp1 = 110 if ($pet_hp1 > 110);
                        $pet_hp1 = qq~<img src=$imagesurl/images/vi_left.gif width=2 height=8><img src=$imagesurl/images/vi_0.gif width=$pet_hp1 height=8 alt="体力: $pet_hp"><img src=$imagesurl/images/vi_right.gif width=4 height=8>~;

                        my $pet_sp1 = int(sqrt($pet_sp) / 6);
                        $pet_sp1 = 110 if ($pet_sp1 > 110);
                        $pet_sp1 = qq~<img src=$imagesurl/images/jy_left.gif width=2 height=8><img src=$imagesurl/images/jy_0.gif width=$pet_sp1 height=8 alt="食物: $pet_sp"><img src=$imagesurl/images/jy_right.gif width=4 height=8>~;

                        $pet_jb1 = $pet_jb;
                        $pet_jb = int($pet_jb / 10);

                        if ($pet_die eq 'die') {
                            $pet_name .= '(已经死亡)';
                            $pet_zt = '';
                            $pet_xz_time = '已经死亡...';
                            $pet_style = qq~ style="filter:xray"~;
                        }

                        $pet{$membername} = qq~<br><table border="1" width="320" style="border-collapse: collapse" bordercolor="$tablebordercolor" cellPadding=2 cellSpacing=0 align=right><tr><td colspan="2" height="23" bgcolor="$miscbacktwo">&nbsp;<img src=$imagesurl/pet_maiweb/cw.gif> 昵称： <a href=pet.cgi?action=myspet&petname=$tempmembername target=_blank><b>$pet_name</b></a> $pet_zt　　年龄： $pet_born 天</td></tr><tr><td width="110" align=center $pet_style><img src=$imagesurl/pet_maiweb/pet/$pet_sx/$pet_sx$pet_jb.gif border=0></td><td width="*">&nbsp;胜利 $pet_win 次 / 失败 $pet_lose 次<br>&nbsp;攻击力 $pet_gjl 点 / 防御力 $pet_fyl 点<br>&nbsp;经验： $pet_exp1<br>&nbsp;体力： $pet_hp1<br>&nbsp;食物： $pet_sp1<BR>&nbsp;状态： $pet_xz_time</td></tr></table>~;
                    }
                    else {$pet{$membername} = '';}
                }
                else {$pet{$membername} = '';}
            }
            else {$pet{$membername} = '';}

            open(FILE, ">${lbdir}cache/meminfo/$membername.pl");
            print FILE qq(
\$membername{"$membername"}      = qq~$membername{$membername}~;
\$membercode{"$membername"}      = qq~$membercode{$membername}~;
\$rating{"$membername"}          = qq~$rating{$membername}~;
\$membergraphic{"$membername"}   = qq~$membergraphic{$membername}~;
\$posterfontcolor{"$membername"} = qq~$posterfontcolor{$membername}~;
\$joineddate{"$membername"}      = qq~$joineddate{$membername}~;
\$numberofposts{"$membername"}   = qq~$numberofposts{$membername}~;
\$seximages{"$membername"}       = qq~$seximages{$membername}~;
\$mymoney{"$membername"}         = qq~$mymoney{$membername}~;
\$jifen{"$membername"}           = qq~$jifen{$membername}~;
\$mysaves{"$membername"}         = qq~$mysaves{$membername}~;
\$myloan{"$membername"}          = qq~$myloan{$membername}~;
\$userflag{"$membername"}        = qq~$userflag{$membername}~;
\$pvmsggraphic{"$membername"}    = qq~$pvmsggraphic{$membername}~;
\$profilegraphic{"$membername"}  = qq~$profilegraphic{$membername}~;
\$friendgraphic{"$membername"}   = qq~$friendgraphic{$membername}~;
\$emailgraphic{"$membername"}    = qq~$emailgraphic{$membername}~;
\$oicqgraphic{"$membername"}     = qq~$oicqgraphic{$membername}~;
\$icqgraphic{"$membername"}      = qq~$icqgraphic{$membername}~;
\$searchgraphic{"$membername"}   = qq~$searchgraphic{$membername}~;
\$showxz{"$membername"}          = qq~$showxz{$membername}~;
\$showsx{"$membername"}          = qq~$showsx{$membername}~;
\$onlinetimehour{"$membername"}  = qq~$onlinetimehour{$membername}~;
\$onlinetimemin{"$membername"}   = qq~$onlinetimemin{$membername}~;
\$onlinetimesec{"$membername"}   = qq~$onlinetimesec{$membername}~;
\$glowing{"$membername"}         = qq~$glowing{$membername}~;
\$jhcount{"$membername"}         = qq~$jhcount{$membername}~;
\$showawards{"$membername"}      = qq~$showawards{$membername}~;
\$lastgone{"$membername"}        = qq~$lastgone{$membername}~;

\$homepagegraphic{"$membername"} = qq~$homepagegraphic~;
\$membernameimg{"$membername"}   = qq~$membernameimg~;
\$membertitle{"$membername"}     = qq~$membertitle~;
\$useravatar{"$membername"}      = qq~$useravatar~;
\$mtitle{"$membername"}          = qq~$mtitle~;
\$location{"$membername"}        = qq~$locat$membername"}      = qq~$showawards{$membername}~;
\$lastgone{"$membername"}        = qq~$lastgone{$membername}~;

\$homepagegraphic{"$membername"} = qq~$homepagegraphic~;
\$membernameimg{"$membername"}   = qq~$membernameimg~;
\$membertitle{"$membername"}     = qq~$membertitle~;
\$useravatar{"$membername"}      = qq~$useravatar~;
\$mtitle{"$membername"}          = qq~$mtitle~;
\$location{"$membername"}        = qq~$locatername = "客人";
	require "guestinfo.pl" if ($membercode{"客人"} eq "");
    }
}
1;
