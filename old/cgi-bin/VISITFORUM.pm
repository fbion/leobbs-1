#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

package VISITFORUM;
use strict;

use vars qw(@ISA @EXPORT);
use warnings;
use diagnostics;
use diagnostics;

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(getlastvisit setlastvisit);

sub getlastvisit {
    my $lv = $main::query->cookie("templastvisit");
    unless ($lv) {
        $lv = $main::query->cookie("lastvisit");
        $lv = "${main::inforum}-${main::currenttime}--" unless ($lv);
        $main::tempvisitcookie = main::cookie(-name => "templastvisit", -path => "${main::cookiepath}/", -expires => "+30d", -value => $lv);
    }
    my @pairs = split(/\--/, $lv);
    foreach (@pairs) {
        my ($n, $val) = split(/\-/, $_);
        $main::lastvisitinfo{$n} = $val;
    }
    return;
}

sub setlastvisit {
    my $tinfo = shift;
    my ($tid, $tv, $mv) = split(/\,/, $tinfo);
    my @newv = ();
    my $u = "0";
    my @pairs = split(/\--/, $main::query->cookie("lastvisit"));
    foreach (@pairs) {
        my ($n, $val) = split(/\-/, $_);
        if ($tid eq $n) {
            $u = "1";
            $val = $tv;
        }
        push(@newv, "$n-$val--");
    }

    push(@newv, "$tid-$tv--") if ($u eq "0" && $tinfo ne "");
    my $nfo = join("", @newv);
    $main::permvisitcookie = main::cookie(-name => "lastvisit", -value => $nfo, -path => "${main::cookiepath}/", -expires => "+30d");
    $main::tempvisitcookie = main::cookie(-name => "templastvisit", -value => $nfo, -expires => "+30d", -path => "${main::cookiepath}/") if ($mv eq "1");
    return;
}

1;