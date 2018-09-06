#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

	   if (($onlinedatanumber >= $arrowonlinemax)&&($arrowonlinemax > 0)&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")) {
       	      print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
              print "<BR>服务器忙，已经超出论坛允许的最大在线人数。<BR><BR>目前论坛在线 $onlinedatanumber 人，最大允许同时在线 $arrowonlinemax 人。";
              exit;
           }
	   use testinfo qw(ipwhere osinfo browseinfo);
	   eval { $osinfo=&osinfo(); };
    	   if ($@) { $osinfo="Unknow"; }
	   eval { $browseinfo=&browseinfo(); };
    	   if ($@) { $browseinfo="Unknow"; }
           my $fromwhere = &ipwhere("$trueipaddress");
           my $tempdata = "$tempusername\t$currenttime\t$currenttime\t$where\t$ipall\t$osinfo\t$browseinfo\t$where2\t$fromwhere\t$membercode\t$hidden\t$sex\t" ;
           $fromwhere1 = $fromwhere;
           if ($tempusername !~ /^客人/) { require "douplogintime.pl"; &uplogintime("$tempusername","T"); }
           $tempdata =~ s/[\a\f\n\e\0\r]//isg;
           push(@onlinedata,$tempdata);
1;
