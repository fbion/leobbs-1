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

unlink("${lbdir}cache/id/$infilemembername.cgi");
if (($in_member_name ne "") && ($in_member_name ne "客人")) {
    if (open(FILE, "${lbdir}data/idbans.cgi")) {
        $term_idbannedmembers = <FILE>;
        close(FILE);
        $term_idbannedmembers =~ s/\t/\_/isg;
        $term_idbannedmembers = "\_$term_idbannedmembers\_";
        $term_idbannedmembers =~ s/\_\_/\_/isg;
        $term_idbannedmembers =~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
        $tempinmembername = "\_$in_member_name\_";
        $tempinmembername =~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
        if ($term_idbannedmembers =~ /$tempinmembername/i) {&error(" ID 被禁止&由于你没遵守本站规定！你的 ID ($in_member_name) 被禁止！如有疑问，请联系管理员。");}
    }
}

if ($arrowformwhere ne "") {
    $arrowwhere = "no";
    use testinfo qw(ipwhere);
    $fromwhere = &ipwhere("$trueipaddress");
    if ($fromwhere ne "") {
        $arrowformwhere =~ s/ ,/,/isg;
        $arrowformwhere =~ s/, /,/isg;
        my @arrowformwhere = split(/\,/, $arrowformwhere);
        foreach (@arrowformwhere) {
            next if ($_ eq "");
            if (($fromwhere =~ m/$_/) || ($_ =~ m/$fromwhere/)) {
                #允许此地区
                $arrowwhere = "yes";
                last;
            }
        }
    }

}

if (open(FILE, "${lbdir}data/ipbans.cgi")) {
    my @term_bannedmembers = <FILE>;
    close(FILE);
    my @term_vipmembers = grep (/^[0-9]/, @term_bannedmembers);
    @term_bannedmembers = grep (/^\-/, @term_bannedmembers);
    my $ipallow = "yes";

    foreach (@term_bannedmembers) {
        s/\r//sg;
        s/^\-//sg;
        chomp;
        next if ($_ eq "");
        if ($trueipaddress =~ /^$_/ || $ipaddress =~ /^$_/) {
            $ipallow = $_;
            last;
        }
    }
    foreach (@term_vipmembers) {
        s/\r//sg;
        chomp;
        next if ($_ eq "");
        if ($trueipaddress =~ /^$_/ || $ipaddress =~ /^$_/) {
            $ipallow = "yes";
            $arrowwhere = "yes";
            last;
        }
    }
    &error("地区被禁止&由于坛主规定，你的来自地区 ( $fromwhere) 被禁止访问本论坛！如有疑问，请联系管理员。") if ($arrowwhere eq "no");
    #            if ($arrowwhere eq "no") { print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES"); exit; }
    &error(" IP 被禁止&由于你没遵守本站规定！你的 IP ($ipallow) 被禁止！如有疑问，请联系管理员。") if ($ipallow ne "yes");
}

#写入缓存标志
$infilemembername =~ s/\.\.//g;
$infilemembername =~ s/[\\\/]//isg;
open(FILE, ">${lbdir}cache/id/$infilemembername.cgi");
print FILE "exit;";
close(FILE);
1;
