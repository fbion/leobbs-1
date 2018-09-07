#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

    $line1 = &HTML($line1);
    $line1 =~ s/\n/<BR>/isg;
    $output .= qq~
    <BR><BR>
    <center><img src="$imagesurl/myimages/$boardlogo" border=0><BR><BR><BR>
    <TABLE cellSpacing=0 cellPadding=0 width=400 height=350><TR><TD><IMG src=$imagesurl/images/top_l.gif></TD><TD background=$imagesurl/images/top_c.gif></TD><TD><IMG src=$imagesurl/images/top_r.gif></TD></TR><TR><TD vAlign=top background=$imagesurl/images/center_l.gif></TD><TD bgcolor=#fffff1 width=100% height=100% valign=top>
    <b><font color=#FF0000>$boardname正在维护中，请稍后再访问...</b></font>
    <BR><BR>$line1<BR><br>
    <TD vAlign=top background=$imagesurl/images/center_r.gif></TD></TR><TR><TD vAlign=top><IMG src=$imagesurl/images/foot_l1.gif ></TD><TD background=$imagesurl/images/foot_c.gif></TD><TD align=right><IMG src=$imagesurl/images/foot_r.gif></TD></TR></TABLE><BR>
    <br><br><br>
~;
    print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    &output("$boardname正在维护中，请稍后再访问...",\$output);
    exit;
1;
