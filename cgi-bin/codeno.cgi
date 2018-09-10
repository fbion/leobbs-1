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

sub lbnocode {
    my $post = shift;
    study($$post);

    $$post =~ s/javascript/\&\#106\;avascript/isg;
    $$post =~ s/value/\&\#118\;alue/isg;
    $$post =~ s/FORM/\&\#102\;orm/isg;
    $$post =~ s/about:/about\&\#58\;/isg;
    $$post =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $$post =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $$post =~ s/adminpass/admin\&\#112\;ass/isg;
    $$post =~ s/file:/file\&\#58\;/isg;
    $$post =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
    $$post =~ s/title/\&\#116\;itle/isg;
    $$post =~ s/membercode/memberc\&\#111\;de/isg;
    $$post =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;
    $$post =~ s/\[DISABLELBCODE\]//isg;

    if ($$post =~ /\[ADMINOPE=(.+?)\]/) {
	while ($$post =~ /\[ADMINOPE=(.+?)\]/g) {
	    my ($inmembername1,$editmembername1,$ratingname1,$reason1,$thistime1) = split(/\|/,$1);
	    $thistime1 = $thistime1 + ($timedifferencevalue*3600) + ($timezone*3600);
	    $thistime1 = &dateformatshort($thistime1);
	    $$post =~ s/\[ADMINOPE=(.+?)\]/<font color=$fonthighlight>-------------------------------------------------------------------<br>$inmembername1 在 $thistime1 由于此帖对 $editmembername1　进行如下操作：<BR>$ratingname1<BR>理由： $reason1<br>-------------------------------------------------------------------<\/font><br><br>/is;
	}
    }

    if ($$post =~ /\[POSTISDELETE=(.+?)\]/) {
    	$postdelete = 1;
    	if ($1 ne " ") { $presult = "<BR>屏蔽理由：$1<BR>"; } else { $presult = "<BR>"; }
    	if (($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")) {
    	    $$post =~ s/\[POSTISDELETE=(.+?)\]//;
            $$post = "--------------------------<br><font color=$posternamecolor>此帖子内容已经被单独屏蔽！$presult内容如下（只有管理员可视）：</font><br>--------------------------<br><br>" . $$post;
    	} else {
            $$post = qq(<br>--------------------------<br><font color=$posternamecolor>此帖子内容已经被单独屏蔽！$presult如有疑问，请联系管理员！</font><br>--------------------------<BR>);
            return;
        }
    }

if ($$post=~m/\[ALIPAYE\]/){
    my ($no,$alipayid,$warename,$oldpost,$wareprice,$wareurl,$postage_mail,$postage_express,$postage_ems) = split(/\[ALIPAYE\]/,$$post);
    
    my $zanshi; my $youfei;
    $wareurl = "http://$wareurl" if ($wareurl ne "");
    if ($wareurl ne "") { $zanshi = " 　[<a href=\"$wareurl\">商品展示</a>]"; }
    if ($postage_mail ne "" || $postage_express ne "" || $postage_ems ne "") {
	$youfei = "买家承担邮费，"; $youfei .= "平邮 $postage_mail 元 / " if ($postage_mail ne ""); $youfei .= "快递 $postage_express 元 / " if ($postage_express ne ""); $youfei .= "EMS $postage_ems 元 / " if ($postage_ems ne "");
	chop $youfei;chop $youfei;chop $youfei;
    } else {
	$youfei = "卖家承担邮费";
    }

    my $firstline = $oldpost;
    $firstline =~ s/(\[这个贴子最后由.+?在.+?次编辑\])/$1/isg;
    $firstline = $1;
    $oldpost=~ s/\[这个贴子最后由.+?在.+?次编辑\]<br>//isg;

    my $post1 = qq~$firstline<BR><BR>
<B>卖家名称：</B> $alipayid 　[<a href=https://www.alipay.com/trade/i_credit.do?email=$alipayid target=_blank>查看该卖家信用</a>] <BR><BR>
<B>商品名称：</B> $warename$zanshi<BR><BR>
<B>商品价格：</B> $wareprice 元<BR><BR>
<B>邮费情况：</B> $youfei<BR><BR>
<B>商品描述：</B><BR>
$oldpost<BR><BR>
~;
$warename=uri_escape($warename);
$oldpost=~ s/\[UploadFile.{0,6}=.+?\]//isg; $oldpost = &temppost($oldpost);
$oldpost=uri_escape($oldpost);
$wareurl=uri_escape($wareurl);
$$post = qq~
<a href=https://www.alipay.com/payto:$alipayid?subject=$warename&body=$oldpost&price=$wareprice&url=$wareurl&ordinary_fee=$postage_mail&express_fee=$postage_express&ems_fee=$postage_ems&readonly=true target=_blank><img src=http:\/\/img.alipay.com\/pimg\/button_alipaybutton_o.gif border=0><\/a><BR>
$post1<BR>
<a href=https://www.alipay.com/payto:$alipayid?subject=$warename&body=$oldpost&price=$wareprice&url=$wareurl&ordinary_fee=$postage_mail&express_fee=$postage_express&ems_fee=$postage_ems&readonly=true target=_blank><img src=http:\/\/img.alipay.com\/pimg\/button_alipaybutton_o.gif border=0><\/a><BR>
~;
}
#buyer_msg=您对本商品有什么疑问和意见可以在此留言

   if ($$post =~ /\[UploadFile.{0,6}=.+?\]/) {
     if ($abslink ne "yes") {
        if (($nodispphoto ne 'yes' && $arrawpostpic eq 'on') || $membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo') {
            if ($imgslt eq "Disp") {
            	$defaultsltwidth = 60 if ($defaultsltwidth eq "");
            	$defaultsltheight = 60 if ($defaultsltheight eq "");
            	$sltnoperline = 5 if ($sltnoperline eq "");
            	my $jsq = 0;
            	while ($$post =~ /\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/i) {
            	    $jsq ++;
            	    if (($jsq eq $sltnoperline)&&($sltnoperline ne 0)) {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a><BR><BR>/i;
                        $jsq = 0;
                    } else {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a>　/i;
                    }
                }
            } else {
                $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a>/isg;
            }
            if ($thisprog eq "post.cgi") {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><BR>/isg;
            } else {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')><img id=followImg$1 src=$imagesurl\/images\/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> 按此查看图片详细信息<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$1 style=DISPLAY:none><tr><td id=followTd$1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')>正在读取此图片的详细信息，请稍候 ...<\/DIV><\/td><\/tr><\/table><\/span><BR><BR>/isg;
            }
	} else{
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=$imagesurl\/icon\/$2.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank>点击显示此主题相关图片<\/a><br>/isg;
	}
    } else {
     	my $tmptopic = $intopic%100;
        if (($nodispphoto ne 'yes' && $arrawpostpic eq 'on') || $membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo') {
            if ($imgslt eq "Disp") {
            	$defaultsltwidth = 60 if ($defaultsltwidth eq "");
            	$defaultsltheight = 60 if ($defaultsltheight eq "");
            	$sltnoperline = 5 if ($sltnoperline eq "");

            	my $jsq = 0;
            	while ($$post =~ /\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/i) {
            	    $jsq ++;
            	    if (($jsq eq $sltnoperline)&&($sltnoperline ne 0)) {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a><BR><BR>/i;
                        $jsq = 0;
                    } else {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a>　/i;
                    }
                }
            } else {
                $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a>/isg;
            }
            if ($thisprog eq "post.cgi") {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><BR>/isg;
            } else {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')><img id=followImg$1 src=$imagesurl\/images\/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> 按此查看图片详细信息<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$1 style=DISPLAY:none><tr><td id=followTd$1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')>正在读取此图片的详细信息，请稍候 ...<\/DIV><\/td><\/tr><\/table><\/span><BR><BR>/isg;
            }
	} else{
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank><img src=$imagesurl\/icon\/$2.gif border=0 width=16><\/a> <a href=$imagesurl\/$usrdir\/$inforum\/$tmptopic\/$1\.$2 target=_blank>点击显示此主题相关图片<\/a><br>/isg;
	}
      }	
	if (($arrawpostflash eq "on") ||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/\[UploadFileDisp=([^\]]+?)\.swf\]/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.swf\]/<br><img src=$imagesurl\/icon\/swf.gif border=0 width=16> 该主题有一个 swf 格式 Flash 动画<br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed><br>&nbsp;<img src=$imagesurl\/images\/fav.gif width=16> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf target=_blank>全屏观看<\/a> (按右键下载)<br><BR>/isg;
	} else {
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.swf\]/<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf target=_blank><img src=$imagesurl\/icon\/swf.gif border=0 width=16 height=16>点击欣赏 Flash 动画<\/a><BR>/isg;
	}

	if ($$post =~ /\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/) {
	    require "newbt.pl" if ($loadnewbt ne 1);
	    $loadnewbt = 1;
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>该主题有一个 BitTorrent 格式的文件，按此可直接下载<\/a><br>btfileinfolist/i;
            newbt();
	    $$post =~ s/<br>btfileinfolist/<br>$addme/i;
	    $addme = "";
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>这个是上传的 BitTorrent 文件，按此可直接下载<\/a><br>/isg;
	}

	while ($$post =~ /\[UploadFile.{0,6}=([^\\\]]+?)(\.(.*?))\]/i) {
   	    $file_type = (-e "${imagesdir}icon/$3.gif") ? $3 : "unknow";
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)(\.(.*?))\]/<br><img src=$imagesurl\/icon\/$file_type.gif border=0 width=16> 这个是上传的 $3 格式文件 [<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=$2 target=_blank><B>点击查看<\/b><\/a>]<br>/isg;
	}
    }
    return;
}
1;
