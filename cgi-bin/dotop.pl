#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

if (open(FILE, "${lbdir}boarddata/jinghua$inforum.cgi")) {
    sysread(FILE, $jhdata,(stat(FILE))[7]);
    close(FILE);
    $jhdata =~ s/\r//isg;
    $jhdata =~ s/\n/\_/isg;
    $jhdata = "\_$jhdata\_";
    $jhdata =~ s/\W//isg;
} else { $jhdata = ""; }

if (open(FILE, "${lbdir}boarddata/highlight$inforum.cgi")) {
    sysread(FILE, $highlight,(stat(FILE))[7]);
    close(FILE);
    $highlight =~ s/\r//isg;
    $highlight =~ s/\n/\_/isg;
    $highlight = "\_$highlight\_";
    $highlight =~ s/[^\w\-\_]//isg;
} else { $highlight = ""; }
  
if (open(FILE, "${lbdir}boarddata/absontop.cgi")) {
    sysread(FILE, $absontopdata,(stat(FILE))[7]);
    close(FILE);
    $absontopdata =~ s/\r//isg;
    $absontopdata =~ s/\n/\_/isg;
    $absontopdata =~ s/[^\w\|]//isg;
} else { $absontopdata = ""; }

if (open(FILE, "${lbdir}boarddata/catontop$categoryplace.cgi")) {
    sysread(FILE, $catontopdata,(stat(FILE))[7]);
    close(FILE);
    $catontopdata =~ s/\r//isg;
    $catontopdata =~ s/\n/\_/isg;
    $catontopdata =~ s/[^\w\|]//isg;
} else { $catontopdata = ""; }

if (open(FILE, "${lbdir}boarddata/ontop$inforum.cgi")) {
    sysread(FILE, $ontopdata,(stat(FILE))[7]);
    close(FILE);
    $ontopdata =~ s/\r//isg;
    $ontopdata =~ s/\n/\_/isg;
    $ontopdata =~ s/\W//isg;
} else { $ontopdata = ""; }

if (!(-e "${lbdir}cache/forumstop$inforum.pl")) {
    open (FILE, ">${lbdir}cache/forumstop$inforum.pl");
    print FILE qq~\$jhdata=qq($jhdata);\n~;
    print FILE qq~\$highlight=qq($highlight);\n~;
    print FILE qq~\$absontopdata=qq($absontopdata);\n~;
    print FILE qq~\$catontopdata=qq($catontopdata);\n~;
    print FILE qq~\$ontopdata=qq($ontopdata);\n~;
    print FILE "1;\n";
    close(FILE);
}
$jhdata = "" if ($usejhpoint ne "yes");
1;
