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

my $x = &myrand(1000000000);
$x = crypt($x, aun);
$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$x =~ s/[^\w\d]//g;
$x = substr($x, 2, 9);
my $memdir = "members$x" if (rename("$lbdir$memdir", "${lbdir}members$x"));
my $msgdir = "messages$x" if (rename("$lbdir$msgdir", "${lbdir}messages$x"));

opendir(DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir(DIRS);
@files = grep (/^\w+?$/i, @files);
my @ftpdir = grep (/^ftpdata/i, @files);
$ftpdir = $ftpdir[0];
my @memfavdir = grep (/^memfav/i, @files);
$memfavdir = $memfavdir[0];
my @saledir = grep (/^sale/i, @files);
$saledir = $saledir[0];
my @searchdir = grep (/^search/i, @files);
$searchdir = $searchdir[0];
my @recorddir = grep (/^record/i, @files);
$recorddir = $recorddir[0];
my $x = &myrand(1000000000);
$x = crypt($x, aun);
$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$x =~ s/[^\w\d]//g;
$x = substr($x, 2, 9);
$searchdir = "search$x" if (rename("$lbdir$searchdir", "${lbdir}search$x"));
$ftpdir = "ftpdata$x" if (rename("$lbdir$ftpdir", "${lbdir}ftpdata$x"));
$memfavdir = "memfav$x" if (rename("$lbdir$memfavdir", "${lbdir}memfav$x"));
$recorddir = "record$x" if (rename("$lbdir$recorddir", "${lbdir}record$x"));
$saledir = "sale$x" if (rename("$lbdir$saledir", "${lbdir}sale$x"));

1;
