#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
use strict;
use warnings;
use diagnostics;

sub lbcode {
    my $post = shift;
    study($$post);
    $$post =~ s/\[UploadFile=(.*?)\]/(上传文件)<br>/ig;
    if ($wwjf ne "no") {
        if ($$post =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
            if ((lc($inmembername) eq lc($membername)) || ($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes") || ($myrating >= $1)) {
            }
            else {
                $$post = qq~（您没有权限看这个帖子，您的威望至少需要 <b>$1<\/b><br> ~;
                $addme = "(附件保密!)<br><br>" if ($addme);
            }
            $$post =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN/（此贴只有威望大于等于 <b>$1<\/b> 的才能查看）<br>/sg;
        }
    }
    else {$$post =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//;}
    $$post =~ s/\[Maiweb_leobbs(.+?)\]/(maiweb)巧嘴娃娃特效/g;
    $$post =~ s/(\[cimg=)(\S+?)(\,)(\S+?)(\])\s*(\S+?)\s*(\[\/cimg\])/(maiweb)涂鸦图片/isg;

    if ($cansale ne "no") {
        if ($$post =~ /LBSALE\[(.*?)\]LBSALE/sg) {
            require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");

            my $postno = $rn - 1;
            my $isbuyer = "";
            my $allbuyer = "";
            my $allbuyerno = "";
            undef @allbuyer;
            if (open(FILE, "${lbdir}$saledir/$in_forum\_$in_topic\_$postno.cgi")) {
                my $allbuyer = <FILE>;
                close(FILE);
                chomp $allbuyer;
                $allbuyer =~ s/\t\t/\t/isg;
                $allbuyer =~ s/\t$//gi;
                $allbuyer =~ s/^\t//gi;
                @allbuyer = split(/\t/, $allbuyer);
                $allbuyerno = @allbuyer;
                $allbuyerno2 = $allbuyerno - 1;

                $allbuyer = "\t$allbuyer\t";
                $isbuyer = "yes" if ($allbuyer =~ /\t$inmembername\t/i);
            }
            $allbuyerno = 0 if (($allbuyerno < 0) || ($allbuyerno eq ""));
            unless (($inmembername eq $membername) || ($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes") || ($isbuyer eq "yes")) {
                $$post = qq~(察看这个帖子需要 <b>$1<\/b> $moneyname，目前已有 <b>$allbuyerno<\/b> 人购买，<a href=\"buypost.cgi?inforum=$in_forum&amp;intopic=$in_topic&amp;postmast=$most&amp;postnumber=$postno&amp;salemembername=$membername&amp;moneynumber=$1\">\[购买\]<\/a>)~;
                $addme = "(附件保密!)<br><br>" if ($addme);
            }
            else {
                $$post =~ s/LBSALE\[(.*?)\]LBSALE/（此贴售价 <b>$1<\/b> $moneyname，目前已有 <b>$allbuyerno<\/b> 人购买。)<br><br>/sg;
            }
        }
    }
    else {$$post =~ s/LBSALE\[(.*?)\]LBSALE//;}

    if ($$post =~ /\[DISABLELBCODE\]/) {
        $$post =~ s/\[DISABLELBCODE\]//isg;
        return;
    }

    if (($arrawpostpic eq "on") || ($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
        $$post =~ s/\[url.+?\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]\[\/url\]/<img src=\'$1:\/\/$2\' alt=\'图片\' width=\'110\' \/>/isg;
        $$post =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=\'$1:\/\/$2\' alt=\'图片\' width=\'110\' \/>/isg;
        $$post =~ s/\[img\,(.+?)\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=\'$2:\/\/$3\' align=\'$1\' alt=\'图片\' width=\'110\' \/>/isg;
        $$post =~ s/(^|\s|\>|\\|\;)(http|https|ftp):\/\/(\S+?\.)(png|bmp|gif|jpg|jpeg)(\s|$|\<|\[)/$1<img src=\'$2:\/\/$3$4\' width=\'110\' alt=\'图片\' \/>$5/isg;
    }

    $$post =~ s/(^|\s|\>|\\|\;)www\.(\S+?)(\s|$|\<|\[)/$1www.$2$3/isg;
    $$post =~ s/(^|\s|\>|\\|\;)(\w+\@\w+\.\w+)(\s|$|\<|\[)/$1$2$3/isg;
    $$post =~ s/\<p>/<br><br>/isg;
    $$post =~ s/\[br\]/<br>/isg;
    $$post =~ s/(<br>){10,}/<br><br><br>/ig;

    if (($$post =~ /\[curl=(http|https|ftp):\/\/(.*?)\]/i) && ($usecurl ne "no")) {
        $$post =~ s/\[curl=(http|https|ftp):\/\/(.*?)\]/\(加密链接\)/ig;
    }
    unless ($$post =~ /\[\/.{1,12}]/) {
        $$post =~ s/\{br\}/<br>/sg;
        return;
    }

    $$post =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/$1$2$3/isg;
    $$post =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/$2/isg;
    $$post =~ s/\[url\]\s*(.*?)\s*\[\/url\]/$1/isg;
    $$post =~ s/(\[email\])(\S+?\@\S+?)(\[\/email\])/Email:$2)/isg;
    $$post =~ s/\[email=(\S+?\@\S+?)\]\s*(.*?)\s*\[\/email\]/Email:$2/isg;
    ## 指定帖子给特殊会员看
    if ($$post =~ m/\[qqh=(.+?)\](.+?)\[\/qqh\]/isg) {
        $cenviewer = "$1";
        if ((lc($cenviewer) eq lc($inmembername)) || (lc($membername) eq lc($inmembername))) {
            $$post =~ s/\[qqh=(.+?)\](.+?)\[\/qqh\]/\(这是$membername给你的悄悄话，请注意保密:$2\)<br>/isg;
        }
        else {
            $$post =~ s/\[qqh=(.+?)\](.+?)\[\/qqh\]/\(你不能查看本文章的内容，本文只给$1查看。抱歉\)/isg;
        }
    }
    ## By maiweb end
    if ($jfmark eq "yes") {
        if ($$post =~ m/\[jf=(\d+?)\](.+?)\[\/jf\]/isg) {
            $jfpost = $1;
            if (($jfpost <= $jifen) || ($mymembercode eq "ad") || ($mymembercode eq "smo") || ($myinmembmod eq "yes") || (lc($membername) eq lc($inmembername))) {
                $$post =~ s/\[jf=(\d+?)\](.*)\[\/jf\]/文章内容：（积分必须达到 $jfpost 才能查看本内容）$2/isg;
            }
            else {
                #   &error("有问题&积分必须达到 $jfpost 才能查看，你目前的积分是 $jifen ！") if (($editpostnumber eq "1")&&($noviewjf eq "yes"));
                $$post =~ s/(\[jf=(\d+?)\])(.*)(\[\/jf\])/文章内容： 本内容已被隐藏 , 积分必须达到 $jfpost 才能查看/isg;
                $addme = "附件保密!<br><br>" if (($addme) && ($1 =~ m/^\[jf/));
            }
        }
    }
    if ($hidejf eq "yes") {
        if ($$post =~ m/(\[hide\])(.*)(\[\/hide\])/isg) {
            if ($viewhide ne "1") {
                $$post =~ s/(\[hide\])(.*)(\[\/hide\])/\(本部分内容已经隐藏，必须回复后，才能查看\)<br>/isg;
                $addme = "(附件保密!)<br><br>" if (($addme) && ($1 eq "[hide]"));
            }
            else {
                $$post =~ s/\[hide\](.*)\[hide\](.*)\[\/quote](.*)\[\/hide\]/\(隐藏：$1<br>$2<br>$3\)/isg;
                $$post =~ s/\[hide\]\s*(.*?)\s*\[\/hide\]/\(隐藏：$1\)/isg;
            }
        }
    }
    # 支付宝
    if ($$post =~ m/\[payto\](.*?)\[\/payto\]/) {
        $$post =~ s/\[payto\](.*?)\[\/payto\]/<b>\(这是支付宝交易。\)<\/b>/g;
    }
    # 隐藏帖
    if ($postjf eq "yes") {
        if ($$post =~ m/\[post=(.+?)\](.+?)\[\/post\]/isg) {
            $viewusepost = $1;
            if ($StartCheck >= $viewusepost) {$Checkpost = 'ok';}
            else {$Checkpost = 'not';}
            if (($Checkpost eq 'ok') || ($mymembercode eq "ad") || ($mymembercode eq "smo") || ($myinmembmod eq "yes") || (lc($membername) eq lc($inmembername))) {
                $$post =~ s/\[post=(.+?)\](.*)\[\/post\]/$2/isg;
            }
            else {
                $$post =~ s/(\[post=(.+?)\])(.*)(\[\/post\])/\(本内容已被隐藏 , 发言总数须有 <b>$viewusepost<\/b> 才能查看\)/isg;
                $addme = "(附件保密!)<br><br>" if (($addme) && ($1 =~ m/^\[post/));
            }
        }
    }
    $$post =~ s/\[hr\]/<br>/isg;
    $$post =~ s/\[b\](.+?)\[\/b\]/<b>$1<\/b>/isg;
    $$post =~ s/\[i\](.+?)\[\/i\]/<i>$1<\/i>/isg;
    $$post =~ s/\[u\](.+?)\[\/u\]/<u>$1<\/u>/isg;
    $$post =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/$2/isg;
    $$post =~ s/\[color=(\S+?)\]\s*(.*?)\s*\[\/color\]/$2/isg;
    $$post =~ s/(\[list\])(.+?)(\[\/list\])/$2/isg;
    $$post =~ s/(\[list=s\])(.+?)(\[\/list\])/$2/isg;
    $$post =~ s/(\[list=)(A|1|I)(\])(.+?)(\[\/list\])/$4/isg;
    $$post =~ s/(\[list=)(\S+?)(])(.+?)(\[\/list\])/$4/isg;
    $$post =~ s/\[\*\]//isg;
    $$post =~ s/(\[fly\])(.+?)(\[\/fly\])/$2/isg;
    $$post =~ s/(\[s\])(.+?)(\[\/s\])/$2/isg;
    $$post =~ s/(\[sup\])(.+?)(\[\/sup\])/$2/isg;
    $$post =~ s/(\[sub\])(.+?)(\[\/sub\])/$2/isg;
    $$post =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/$4/isg;
    $$post =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/$8/isg;
    $$post =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/$8/isg;
    $$post =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/$8/isg;
    $$post =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/$2/isg;
    $$post =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/$2/isg;
    $$post =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/$2/isg;
    $$post =~ s/(\[xray\])(.+?)(\[\/xray\])/$2/isg;
    $$post =~ s/(\[MOVE\])(.+?)(\[\/Move\])/$2/isg;
    $$post =~ s/\[code(=.*?)?\](.+?)\[\/code\]/<br>(代码：$2<br>/isg;
    $$post =~ s/\[(.+?)\]//g;
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
    #	$$post =~ s/\&/\&amp;/isg;
    #	$$post =~ s/\&amp;nbsp;/\&nbsp;/isg;
    $$post =~ s/\$/\&#36;/isg;
    #	$$post =~ s/\#/\\\#/isg;
    #	$$post =~ s/\&amp;\\\#/\&\#/g;
    #	$$post =~ s/\<p\>/\<br\/\>\<br\/\>/isg;
    #   $$post =~ s/\<br\>/\<br\/\>/isg;
    return;
}
sub waplbhz {
    my ($str, $start, $len) = @_;
    $strlen = $start + $len;
    my $tmpstr;
    for (my $i = 0; $i < $strlen; $i++) {
        if (ord(substr($str, $i, 1)) > 0xa0) {
            if ($i >= $start && $i < ($start + $len)) {
                $tmpstr .= substr($str, $i, 2);
            }
            $i++;
        }
        else {
            if ($i >= $start && $i < ($start + $len)) {
                $tmpstr .= substr($str, $i, 1);
            }
        }
    }
    return $tmpstr;
}
sub waplbhz1 {
    # by bbser
    my ($str, $strbegin, $strlength) = @_;
    my $strtmp = "";
    my $strtmp1 = "";
    my $ended = 0; # 取得的字符串是否是原始字符串的最后一段

    return -1 if (length($str) < $strbegin); # 参数有错误，起始字符数比整个字符串还要长
    if (length($str) <= $strbegin + $strlength) {
        #参数中长度过大，自动调整一下
        $strlength = length($str) - $strbegin;
        $ended = 1;
    }

    $strtmp = substr($str, $strbegin, $strlength);

    if ($strbegin > 0) {
        # 不是最开头的一段，所以要判断第一个字符是不是中文

        $strtmp1 = substr($str, 0, $strbegin);

        if ($strtmp1 =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/) { #前面一段字符串是完整的汉字
            $strtmp = $strtmp;
        }
        else {
            $strtmp = substr($str, $strbegin - 1, 1) . $strtmp;
            chop($strtmp);
        }

    }

    if ($ended == 0) { # 不是最后一段，所以要判断最后一个字符是不是中文
        if ($strtmp =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/) {
            $strtmp = $strtmp;
        }
        else {
            chop($strtmp);
        }

    }

    return $strtmp;

}

1;