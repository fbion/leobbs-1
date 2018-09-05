#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

opendir (DIR, "${lbdir}data/skin"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @skinselectdata = grep(/\.(cgi)$/i,@dirdata);
map(s/\.cgi$//is, @skinselectdata);
$skincount = @skinselectdata;
my $userskin = qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin=leobbs"><font color=#000000>默认风格</font></a>&nbsp;</div>~;
for (my $i=0;$i<$skincount;$i++) {
    eval{ require "${lbdir}data/skin/$skinselectdata[$i].cgi"; };
    next if ($@);
    if ($cssname ne "") { $skinnames = $cssname; } else { $skinnames = $skinselectdata[$i]; }
    $skinselectdata[$i] = uri_escape($skinselectdata[$i]);
    $userskin.= qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin=$skinselectdata[$i]"><font color=#000000>$skinnames</font></a>&nbsp;</div>~ if (lc($skinselectdata[$i]) ne "leobbs");
    $cssname = "";
}
eval{ require "${lbdir}data/skin/leobbs.cgi"; };
$userskins = qq~
<script>
var url = new String (window.document.location);
url = url.replace (/&/g, "%26");
url = url.replace (/\\\\//g, "%2F");
url = url.replace (/:/g, "%3A");
url = url.replace (/\\\\?/g, "%3F");
url = url.replace (/=/g, "%3D");
linkset[3]='$userskin'</script>~;
$skinselect = qq~<img src=\$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[3])" onMouseout="delayhidemenu()">论坛风格&nbsp;</span>~;
open(FILE, ">${lbdir}data/skinselect.pl");
print FILE qq(\$userskins = qq~$userskins~;\n);
print FILE qq(\$skinselect = qq~$skinselect~;\n);
print FILE "1;\n";
close(FILE);
1;
