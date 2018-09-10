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

(my $membername1, my $topictitle1, my $postipaddresstemp1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, my $posticon1) = split(/\t/, $threads[0]);

if ($jfmark eq "yes") {
    if ($post1 =~ m/\[jf=(.+?)\](.+?)\[\/jf\]/isg) {
        $jfpost = $1;
        if (($jfpost <= $jifen) || ($mymembercode eq "ad") || ($mymembercode eq "smo") || ($myinmembmod eq "yes") || (lc($membername) eq lc($inmembername))) {
        }
        else {
            $noviewthis = "yes" if ($noviewjf eq "yes");
        }
    }
}

if ($noviewthis ne "yes") {
    my @sortedthreads = reverse(@threads);
    my $threadsize = @sortedthreads;
    $listmy = 0 if ($listmy eq "");
    if ($listmy == 0) {
        $listmy = qq~[<a href=$thisprog?action=$action&forum=$inforum&topic=$intopic&postno=$inpostno&listmy=1>列出所有回复</a>]~;
        $listme = ",最多列出 $maxlistpost 个";
        $threadsize = $maxlistpost if ($threadsize > $maxlistpost);
    }
    else {
        $listmy = qq~[<a href=$thisprog?action=$action&forum=$inforum&topic=$intopic&postno=$inpostno&listmy=0>列出前 $maxlistpost 个回复</a>]~;
        $listme = "";
    }
    $output .= qq~<p><script language="javascript">function addquote(no){var membername = eval("membername" + no);var postdate = eval("postdate" + no);var post = eval("post" + no);var text = "[quote][b]下面引用由[u]" + membername.innerText + "[/u]在 [i]" + postdate.innerText + "[/i] 发表的内容：[/b]\\n" + post.innerText.substring(0, 200) + "\\n[/quote]\\n";if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos){var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? text + ' ' : text;}else{document.FORM.inpost.value += text;}document.FORM.inpost.focus();}</script>
<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100% >
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>帖子一览：$topictitle (新回复在最前$listme)</b>　 $listmy</td>
~;

    $postbackcolor = $miscbackone;
    for (my $i = 0; $i < $threadsize; $i++) {
        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/, $sortedthreads[$i]);
        &getmember($membername, "no");
        $post = "此用户的发言已经被屏蔽！" if ($membercode eq "masked");

        $postdate = $postdate + ($timedifferencevalue + $timezone) * 3600;
        $postdate = &dateformat("$postdate");
        $post =~ s/\[hide\](.*)\[\/hide\]/<font color=red>隐藏内容不能预览<\/font>/isg;
        $post = "<font color=red>加密帖子不能预览<\/font>" if (($post =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg) || ($post =~ /LBSALE\[(.*?)\]LBSALE/sg));
        $post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[加密连结\]/isg if ($usecurl ne "no");
        $post =~ s/\[USECHGFONTE\]//sg;
        $post =~ s/\[post=(.+?)\](.+?)\[\/post\]/<blockquote><font face=$font>文章内容 : <hr noshade size=1><font color=red>本内容已被隐藏 , 总发言数须有$1才能查看<\/font><hr noshade size=1><\/font><\/blockquote>/isg;
        $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]/<blockquote><font face=$font>文章内容 : <hr noshade size=1><font color=red>本内容已被隐藏 , 积分必须达到$1才能查看<\/font><hr noshade size=1><\/font><\/blockquote>/isg;

        if ($post =~ /\[POSTISDELETE=(.+?)\]/) {
            $postdelete = 1;
            if ($1 ne " ") {$presult = "<BR>屏蔽理由：$1<BR>";}
            else {$presult = "<BR>";}
            $post = "此帖子内容已经被单独屏蔽！$presult";
        }

        if ($idmbcodestate eq 'on') {
            &lbcode(\$post);
            if ($post =~ /<blockquote><font face=$font>代码/isg) {
                $post =~ s/\&amp\;/\&/ig;
                $post =~ s/\&lt\;br\&gt\;/<br>/ig;
            }
        }
        else {
            require "codeno.cgi";
            &lbnocode(\$inpost);
            $post =~ s/\[DISABLELBCODE\]//isg;
        }
        if (($emoticons eq 'on') && ($showemoticons eq 'yes')) {
            &doemoticons(\$post);
            &smilecode(\$post);
        }

        if ($magicface ne 'off') {
            $output .= qq~
<script>
function MM_showHideLayers() {var i,p,v,obj,args=MM_showHideLayers.arguments;obj=document.getElementById("MagicFace");for (i=0; i<(args.length-2); i+=3) if (obj) { v=args[i+2];if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }obj.visibility=v; }}
function ShowMagicFace(MagicID) {var MagicFaceUrl = "$imagesurl/MagicFace/swf/" + MagicID + ".swf";document.getElementById("MagicFace").innerHTML = '<object codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="500" height="350"><param name="movie" value="'+ MagicFaceUrl +'"><param name="menu" value="false"><param name="quality" value="high"><param name="play" value="false"><param name="wmode" value="transparent"><embed src="' + MagicFaceUrl +'" wmode="transparent" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="500" height="350"></embed></object>';document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";document.getElementById("MagicFace").style.visibility = 'visible';setTimeout("MM_showHideLayers('MagicFace','','hidden')",10000);}</script><DIV id=MagicFace style="Z-INDEX: 99; VISIBILITY: hidden; POSITION: absolute"></DIV>
~;
        }

        $output .= qq~<table style="TABLE-LAYOUT:fixed" cellpadding=8 cellspacing=1 width=100%>
<tr><td bgcolor=$miscbackone rowspan=2 valign="top" width=20%><font color=$fontcolormisc><b><span id=membername$i>$membername</span></b></font></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc><input type=button onClick="addquote($i)" value="引用"> <b>发表于： <span id=postdate$i>$postdate</span></b></td></tr>
<tr><td bgcolor="$miscbackone" style="LEFT:0px;WIDTH:100%;WORD-WRAP:break-word"><font color=$fontcolormisc><span id=post$i>$post</span></td></tr>
<tr><td colspan=2 bgcolor=$miscbacktwo>&nbsp;</td></tr></table>
        ~;
    }
}
$output .= qq~<SCRIPT>valignend()</SCRIPT></table></td></tr></table>~;
1;
