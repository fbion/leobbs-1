#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use strict;
use warnings;
use diagnostics;

if ($firstcome ne 'yes') {
    if (@onlinefr) {
        my $onlinefriend = join('　　', @onlinefr);
        $onlinepopup = "你下面这些好友刚刚上线了！<p>$onlinefriend";
        require 'onlinepop.pl';
    }
    $onlineprompt = uri_escape($onlineprompt);
    $output .= qq~<script>var exp = new Date(); exp.setTime(exp.getTime() + ($membergone*60*1000)); document.cookie="onlineprompt=$onlineprompt; expires=" + exp.toGMTString();</script>~;
}
else {
    my $temptempuser = $tempusername;
    $temptempuser =~ s/ /\_/g;
    $temptempuser =~ tr/A-Z/a-z/;
    $temptempuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\|\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    if (open(FRD, "${lbdir}memfriend/$temptempuser.cgi")) {
        sysread(FRD, my $friendlist, (stat(FRD))[7]);
        close(FRD);
        $friendlist =~ s/\r//isg;
        my @friendlist = split($/, $friendlist);
        my @noonlinefr = ();
        my @onlinefr = ();
        foreach my $friend (@friendlist) {
            $friend =~ s/^＊＃！＆＊//;
            $friend =~ s/[\r\n]*$//;
            next if ($friend eq '');
            if (grep (/^$friend\t/i, @onlinedata) > 0) {
                push(@onlinefr, $friend);
            }
            else {
                push(@noonlinefr, $friend);
            }
        }
        if (@onlinefr) {
            my $onlinefriend = join('　　', @onlinefr);
            $onlinepopup = "你下面这些好友正在线上！<p>$onlinefriend";
            require 'onlinepop.pl';
        }
        if (@noonlinefr) {
            my $onlineprompt = join(',', @noonlinefr);
            $onlineprompt = uri_escape($onlineprompt);
            $output .= qq~<script>var exp = new Date(); exp.setTime(exp.getTime() + ($membergone*60*1000)); document.cookie="onlineprompt=,$onlineprompt,; expires=" + exp.toGMTString();</script>~;
        }
    }
}
1;
