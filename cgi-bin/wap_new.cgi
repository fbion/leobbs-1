#!/usr/bin/perl
#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
BEGIN {
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}
use strict;
use warnings;
use diagnostics;

use LBCGI;
$query = new LBCGI;
require "data/boardinfo.cgi";
require "wap.pl";
$lid = $query->param('lid');
&waptitle;
$show .= qq~<card  title="最新文章"><p>$boardname-最新文章<br/>~;
open(file, "${lbdir}data/recentpost.cgi");
my @file = <file>;
close(file);
foreach (@file[0 .. 14]) {
    chomp;
    next if ($_ eq '');
    $i++;
    my ($f, $t, $ti) = split(/\t/, $_);
    $show .= "<a href=\"wap_topic.cgi?f=$f&amp;t=$t&amp;lid=$lid\">$i,$ti</a><br/>";
}
$show .= '</p>';
$show .= "<p>---------<br/><a href=\"wap_index.cgi?lid=$lid\">返回首页</a></p>";
&wapfoot;
