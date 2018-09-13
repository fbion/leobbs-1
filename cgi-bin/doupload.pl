#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use strict;
use warnings;
use diagnostics;
sub doupload {
    if ($abslink ne "yes") {
        if (($nodispphoto ne 'yes' && $arrawpostpic eq 'on') || $member_code{$membername} eq 'mo' || $member_code{$membername} eq 'amo' || $member_code{$membername} eq 'cmo' || $member_code{$membername} eq 'ad' || $inmembmod eq 'yes' || $member_code{$membername} eq 'smo') {
            if ($imgslt eq "Disp") {
                $defaultsltwidth = 60 if ($defaultsltwidth eq "");
                $defaultsltheight = 60 if ($defaultsltheight eq "");
                $sltnoperline = 5 if ($sltnoperline eq "");

                my $jsq = 0;
                while ($$post =~ /\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/i) {
                    $jsq++;
                    if (($jsq eq $sltnoperline) && ($sltnoperline ne 0)) {
                        $$post =~ s/\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a><BR><BR>/i;
                        $jsq = 0;
                    }
                    else {
                        $$post =~ s/\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a>　/i;
                    }
                }
            }
            else {
                $$post =~ s/\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a>/isg;
            }
            if ($thisprog eq "post.cgi") {
                $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><BR>/isg;
            }
            else {
                $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')><img id=followImg$1 src=$imagesurl\/images\/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> 按此查看图片详细信息<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$1 style=DISPLAY:none><tr><td id=followTd$1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')>正在读取此图片的详细信息，请稍候 ...<\/DIV><\/td><\/tr><\/table><\/span><BR><BR>/isg;
            }
        }
        else {
            $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=$imagesurl\/icon\/$2.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 target=_blank>点击显示此主题相关图片<\/a><br>/isg;
        }
    }
    else {
        my $tmptopic = $in_topic % 100;
        if (($nodispphoto ne 'yes' && $arrawpostpic eq 'on') || $member_code{$membername} eq 'mo' || $member_code{$membername} eq 'amo' || $member_code{$membername} eq 'cmo' || $member_code{$membername} eq 'ad' || $inmembmod eq 'yes' || $member_code{$membername} eq 'smo') {
            if ($imgslt eq "Disp") {
                $defaultsltwidth = 60 if ($defaultsltwidth eq "");
                $defaultsltheight = 60 if ($defaultsltheight eq "");
                $sltnoperline = 5 if ($sltnoperline eq "");

                my $jsq = 0;
                while ($$post =~ /\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/i) {
                    $jsq++;
                    if (($jsq eq $sltnoperline) && ($sltnoperline ne 0)) {
                        $$post =~ s/\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a><BR><BR>/i;
                        $jsq = 0;
                    }
                    else {
                        $$post =~ s/\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a>　/i;
                    }
                }
            }
            else {
                $$post =~ s/\[UploadFileDisp=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a>/isg;
            }
            if ($thisprog eq "post.cgi") {
                $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><BR>/isg;
            }
            else {
                $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')><img id=followImg$1 src=$imagesurl\/images\/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> 按此查看图片详细信息<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$1 style=DISPLAY:none><tr><td id=followTd$1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')>正在读取此图片的详细信息，请稍候 ...<\/DIV><\/td><\/tr><\/table><\/span><BR><BR>/isg;
            }
        }
        else {
            $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/icon\/$2.gif border=0 width=16><\/a> <a href=$imagesurl\/$usrdir\/$in_forum\/$tmptopic\/$1\.$2 target=_blank>点击显示此主题相关图片<\/a><br>/isg;
        }
    }

    if (($arrawpostflash eq "on") || ($member_code{$membername} eq 'mo' || $member_code{$membername} eq 'amo' || $member_code{$membername} eq 'cmo' || $member_code{$membername} eq 'ad' || $inmembmod eq 'yes' || $member_code{$membername} eq 'smo')) {
        $$post =~ s/\[UploadFileDisp=(\w+?)\.swf\]/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.swf\]/<br><img src=$imagesurl\/icon\/swf.gif border=0 width=16> 该主题有一个 swf 格式 Flash 动画<br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed><br>&nbsp;<img src=$imagesurl\/images\/fav.gif width=16> <a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.swf target=_blank>全屏观看<\/a> (按右键下载)<br><BR>/isg;
    }
    else {
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.swf\]/<br><a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.swf target=_blank><img src=$imagesurl\/icon\/swf.gif border=0 width=16 height=16>点击欣赏 Flash 动画<\/a><BR>/isg;
    }

    if (($arrawpostsound eq "on") || ($member_code{$membername} eq 'mo' || $member_code{$membername} eq 'amo' || $member_code{$membername} eq 'cmo' || $member_code{$membername} eq 'ad' || $inmembmod eq 'yes' || $member_code{$membername} eq 'smo')) {
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.wav\]/<br><img src=$imagesurl\/icon\/wav.gif border=0 width=16> 该主题有一个 wave 格式音乐<br><bgsound src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.wav border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(mid|midi)\]/<br><img src=$imagesurl\/icon\/mid.gif border=0 width=16> 该主题有一个 MIDI 格式音效<br><bgsound src=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2 border=0><img src=$imagesurl\/images\/mid.gif width=16 height=16 alt=MIDI音乐>/isg;
    }

    if (($arrawpostreal eq "on") || ($member_code{$membername} eq 'mo' || $member_code{$membername} eq 'amo' || $member_code{$membername} eq 'cmo' || $member_code{$membername} eq 'ad' || $inmembmod eq 'yes' || $member_code{$membername} eq 'smo')) {
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(mp3|mp2)\]/<br><img src=$imagesurl\/icon\/mp3.gif border=0 width=16> 该主题有一个 MP3 格式音乐<br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(ra)\]/<br><img src=$imagesurl\/icon\/ra.gif border=0 width=16> 该主题有一个 RealPlayer 格式音乐<br><object classid="clsid:CFCDAA03-8BE4-11CF-B84B-0020AFBBCCFA" id="RAOCX" width="480" height="70"><param name="_ExtentX" value="6694"><param name="_ExtentY" value="1588"><param name="AUTOSTART" value=$arrawautoplay><param name="SHUFFLE" value="0"><param name="PREFETCH" value="0"><param name="NOLABELS" value="0"><param name="SRC" value="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2"><param name="CONTROLS" value="StatusBar,ControlPanel"><param name="LOOP" value="0"><param name="NUMLOOP" value="0"><param name="CENTER" value="0"><param name="MAINTAINASPECT" value="0"><param name="BACKGROUNDCOLOR" value="#000000"><embed src="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2" width="320" autostart=$arrawautoplay height="70"><\/object><BR>/isg;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(ram|rmm|rm|rmvb|mpg|mpv|mpeg|dat|avi|mpga)\]/<br><img src=$imagesurl\/icon\/ra.gif border=0 width=16> 该主题有一个 RealPlayer 格式影片<br><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" HEIGHT=300 ID=Player WIDTH=480 VIEWASTEXT><param NAME="_ExtentX" VALUE="12726"><param NAME="_ExtentY" VALUE="8520"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="ImageWindow"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><\/object><br><object CLASSID=clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA HEIGHT=32 ID=Player WIDTH=480 VIEWASTEXT><param NAME="_ExtentX" VALUE="18256"><param NAME="_ExtentY" VALUE="794"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="controlpanel"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="0"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><param NAME="SRC" VALUE="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2"><\/object><BR>/isg;
    }

    if (($arrawpostmedia eq "on") || ($member_code{$membername} eq 'mo' || $member_code{$membername} eq 'amo' || $member_code{$membername} eq 'cmo' || $member_code{$membername} eq 'ad' || $inmembmod eq 'yes' || $member_code{$membername} eq 'smo')) {
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(mp3|mp2)\]/<br><img src=$imagesurl\/icon\/mp3.gif border=0 width=16> 该主题有一个 MP3 格式音乐<br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(wma|wm|mpa|mpga)\]/<br><img src=$imagesurl\/icon\/movie.gif border=0 width=16> 该主题有一个 Windows Media Player 格式音乐<br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.(asf|asx|avi|wmv|mpg|mpeg|dat|mpv)\]/<br><img src=$imagesurl\/icon\/movie.gif border=0 width=16> 该主题有一个 Windows Media Player 格式影片<br><object id="videowindow1" width="480" height="330" classid="CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95"><param NAME="Filename" value="$boardurl\/attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.$2"><param name="AUTOSTART" value=$arrawautoplay><\/object><BR>/isg;
    }

    if ($$post =~ /\[UploadFile.{0,6}=(\w+?)\.torrent\]/) {
        require "newbt.pl" if ($loadnewbt ne 1);
        $loadnewbt = 1;
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>该主题有一个 BitTorrent 格式的文件，按此可直接下载<\/a><br>btfileinfolist/i;
        newbt();
        $$post =~ s/<br>btfileinfolist/<br>$addme/i;
        $addme = "";
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>这个是上传的 BitTorrent 文件，按此可直接下载<\/a><br>/isg;
    }

    while ($$post =~ /\[UploadFile.{0,6}=(\w+?)(\.(\w+?))\]/i) {
        $file_type = (-e "${imagesdir}icon/$3.gif") ? $3 : "unknow";
        $$post =~ s/\[UploadFile.{0,6}=(\w+?)(\.(\w+?))\]/<br><img src=$imagesurl\/icon\/$file_type.gif border=0 width=16> 这个是上传的 $3 格式文件 [<a href=attachment.cgi?forum=$in_forum&topic=$in_topic&postno=$editpostnumber&name=$1&type=$2 target=_blank><B>点击查看<\/b><\/a>]<br>/isg;
    }
}
1;
