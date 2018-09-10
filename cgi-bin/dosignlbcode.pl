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

sub signlbcode {
    my $signature = shift;
    study($signature);
    $signature =~ s/javascript/\&\#106\;avascript/isg;
    $signature =~ s/FORM/\&\#102\;orm/isg;
    $signature =~ s/value/\&\#118\;alue/isg;
    $signature =~ s/about:/about\&\#58\;/isg;
    $signature =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $signature =~ s/adminpass/admin\&\#112\;ass/isg;
    $signature =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $signature =~ s/file:/file\&\#58\;/isg;
    $signature =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
    $signature =~ s/title/\&\#116\;itle/isg;
    $signature =~ s/style/\&\#115\;tyle/isg;
    $signature =~ s/membercode/memberc\&\#111\;de/isg;
    $signature =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;
    $signature =~ s/<p>/\n\n/isg;
    $signature =~ s/<br>/\n/isg;

    $signature =~ s/(^|\s|\>|\\|\;)(http|https|ftp):\/\/(\S+?)(\s|$|\<|\[)/$1<a href=$2:\/\/$3\ target=_blank>$2\:\/\/$3<\/a>$4/isg;

    if (($arrawsignpic eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	$signature =~ s/\[url.+?\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]\[\/url\]/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333\"><\/a>/isg;
	$signature =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=$1:\/\/$2 border=0 onload=\"javascript:x=this.width;y=this.height;limity=screen.height\/3;if(this.height>limity)this.height=limity; if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333\" onClick=\"this.width=x;this.height=y\">/isg;
	$signature =~ s/(^|\s|\>|\\|\;)(http|https|ftp):\/\/(\S+?\.)(png|bmp|gif|jpg|jpeg)(\s|$|\<|\[)/$1<a href=$2:\/\/$3$4 target=_blank title=开新窗口浏览><img src=$2:\/\/$3$4 border=0 onload=\"javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333\"><\/a>$5/isg;
    }
    if (($arrawsignflash eq "on")||($membercode{$membername} eq 'mo'|| $membercode{$membername} eq 'amo'  || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	$signature =~ s/(\[swf\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/swf\])/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$2:\/\/$3 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash" WIDTH=$defaultflashwidth height=$defaultflashheight><\/embed>/isg;
	$signature =~ s/(\[FLASH=)(\S+?)(\,)(\S+?)(\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/FLASH\])/<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$2 HEIGHT=$4><PARAM NAME=MOVIE VALUE=$6:\/\/$7><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$6:\/\/$7 WIDTH=$2 HEIGHT=$4 PLAY=TRUE LOOP=TRUE QUALITY=HIGH><\/EMBED><\/OBJECT>/isg;
        $signature =~ s/(^|\s|\>)(http|https|ftp):\/\/(\S+?\.swf)(\s|$|\<)/$1<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$2:\/\/$3 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash" WIDTH=$defaultflashwidth height=$defaultflashheight><\/embed>$4/isg;
    }

    $signature =~ s/(^|\s|\>|\\|\;)www\.(\S+?)(\s|$|\<|\[)/$1<a href=http:\/\/www.$2 target=_blank>www.$2<\/a>$3/isg;
    $signature =~ s/(^|\s|\>|\\|\;)(\w+\@\w+\.\w+)(\s|$|\<|\[)/$1<A HREF=mailto:$2>$2<\/A>$3/isg;

    if ($signature =~ /\[\/.{1,12}]/) {
        $signature =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/<a href=$2 target=_blank>$1$2$3<\/a>/isg;
        $signature =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$2<\/a>/isg;
        $signature =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$1<\/a>/isg;
        $signature =~ s/(\[email\])(\S+\@\S+?)(\[\/email\])/<A HREF="mailto:$2">$2<\/A>/isg;
        $signature =~ s/\[email=(\S+?\@\S+?)\]\s*(.*?)\s*\[\/email\]/<a href=mailto:$1>$2<\/a>/isg;
    
        if (($arrawsignfontsize eq "on")||($membercode{$membername} eq 'mo'|| $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
    	    $signature =~ s/\[size=\s*([1-6])\s*\]\s*(.*?)\s*\[\/size\]/<font size=$1>$2<\/font>/isg;
        }
        if ($arrawsignsound eq "on") {
	    $signature =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.wav)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/mid.gif width=16 height=16 alt=WAVE音乐>/isg;
	    $signature =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.mid)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=MIDI音乐>/isg;
	    $signature =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.midi)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=MIDI音乐>/isg;
        }

        $signature =~ s/\[b\](.+?)\[\/b\]/<b>$1<\/b>/isg;
        $signature =~ s/\[i\](.+?)\[\/i\]/<i>$1<\/i>/isg;
        $signature =~ s/\[u\](.+?)\[\/u\]/<u>$1<\/u>/isg;
        $signature =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/<font face=$1>$2<\/font>/isg;
        $signature =~ s/\[color=(\S+?)\]\s*(.*?)\s*\[\/color\]/<font color=$1>$2<\/font>/isg;
        $signature =~ s/(\[s\])(.+?)(\[\/s\])/<s>$2<\/s>/isg;
        $signature =~ s/(\[sup\])(.+?)(\[\/sup\])/<sup>$2<\/sup>/isg;
        $signature =~ s/(\[sub\])(.+?)(\[\/sub\])/<sub>$2<\/sub>/isg;
        $signature =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/<DIV Align=$2>$4<\/DIV>/isg;
        $signature =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/<table width=$2 style="filter:shadow\(color=$4\, direction=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/<table width=$2 style="filter:glow\(color=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/<table width=$2 style="filter:blur\(Add=0, direction=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/<table style="filter:flipH"><tr><td>$2<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/<table style="filter:flipV"><tr><td>$2<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/<table style="filter:invert"><tr><td>$2<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[xray\])(.+?)(\[\/xray\])/<table style="filter:xray"><tr><td>$2<\/td><\/tr><\/table>/isg;
        $signature =~ s/(\[MOVE\])(.+?)(\[\/Move\])/<MARQUEE>$2<\/MARQUEE>/isg;
        $signature =~ s/(\[fly\])(.+?)(\[\/fly\])/<marquee width=90% behavior=alternate scrollamount=3>$2<\/marquee>/isg;
#	$signature =~ s/<\/MARQUEE>(.{1,40})<\/td><\/tr><\/table>/<\/MARQUEE>$1/isg;
    }
    $signature =~ s/\n\n/<p>/isg;
    $signature =~ s/\n/<br>/isg;
    $signature =~ s|\n\[|\[|g;
    $signature =~ s|\]\n|\]|g;
    $signature =~ s|\[hr\]| |g;
    $signature =~ s/\[br\]/<br>/isg;
    $signature =~ s/<p>/<br><br>/isg;
    $signature =~ s|<br>| <br>|g;
    $signature =~ s/\&amp;/\&/isg;
    $signature =~ s/&quot\;/\"/isg;
    $signature =~ s/\&amp;/\&/isg;
    $signature =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
    $signature =~ s/ \&nbsp;/　/isg;
    return $signature;
}
1;
