#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use warnings;
use strict;
use diagnostics;
open(FILE, "${lbdir}data/allforums.cgi");
@forums = <FILE>;
close(FILE);
$totle1 = 0;
$totle2 = 0;
foreach $forum (@forums) {
    chomp $forum;
    next if (length("$forum") < 30);
    (my $tempno, my $no) = split(/\t/, $forum);
    next if ($tempno !~ /^[0-9]+$/);
    eval {require "${lbdir}boarddata/forumposts$tempno.pl";};
    $totle1 += $threads;
    $totle2 += $posts;
}
opendir(DIRS, "$lbdir");
my @memdir = readdir(DIRS);
closedir(DIRS);
@memdir = grep (/^\w+?$/i, @memdir);
@memdir = grep (/^members/i, @memdir);
my $memdir = $memdir[0];

opendir(DIR, "${lbdir}$memdir/old");
my @filedata = readdir(DIR);
closedir(DIR);
my @countvar = grep (/\.cgi$/i, @filedata);
$newtotalmembers = @countvar;
open(FILE, ">${lbdir}data/boardstats.cgi");
print FILE "\$lastregisteredmember = \'nodisplay\'\;\n";
print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
print FILE "\$totalthreads = \'$totle1\'\;\n";
print FILE "\$totalposts = \'$totle2\'\;\n";
print FILE "\n1\;";
close(FILE);
1;
