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
use diagnostics;

use LBCGI;
$query = new LBCGI;
require "data/boardinfo.cgi";
require "wap.pl";
require "data/styles.cgi";
&waptitle;
$show .= qq~<card  title="$boardname">~;
$lid = $query->param('lid');
$in_forum = $query->param('f');
$in_topic = $query->param('t');
$show .= qq~<p><b>回复内容：</b><br/><input type="text" name="inpost" value=""/><br/>换行标签：[br]</p><p><anchor>回复<go href="wap_reply.cgi" method="post">
<postfield name="inpost" value="\$(inpost)"/>
<postfield name="lid" value="$lid"/>
<postfield name="f" value="$in_forum"/>
<postfield name="t" value="$in_topic"/>
</go>
</anchor></p>~;
$show .= qq~<p><br/><br/><a href="wap_forum.cgi?forum=$in_forum&amp;lid=$lid&amp;paGe=$pa">返回列表</a></p><p><a href="wap_topic.cgi?f=$in_forum&amp;lid=$lid&amp;t=$in_topic">返回帖子</a></p>~;
&wapfoot;