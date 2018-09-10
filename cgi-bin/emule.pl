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

sub doemule {
    $codecount = 1 if ($codecount <= 0);
    $$post .= "<script src=$imagesurl/images/emu.js></script>" if ($codecount == 1);
    while ($$post =~ /\[emule\](.+?)\[\/emule\]/is) {
        my $view = "<br><table width=94% align=center cellspacing=1 cellpadding=5 bgColor=$tablebordercolor><tr bgColor=$titlecolor><td colspan=2 align=center><font color=$titlefontcolor><B>下面是 eMule 专用的下载链接，您必须安装 eMule 才能点击下载</B></font></td></tr>";
        my $post1 = $1;
        $post1 =~ s/<p>/<br>/isg;
        $post1 =~ s/<br><br>/<br>/isg;
        my @lines = split(/<br>/i, $post1);
        $post1 = "";
        my $counters = 0;
        my $total = 0;
        my $totalper = 0;
        my $postbackcolor1 = "";
        my $postfontcolor1 = "";
        foreach (@lines) {
            chomp $_;
            $_ =~ s/[\a\f\e\0\r\t]//isg;
            $_ =~ s/</\&lt;/g;
            $_ =~ s/>/\&gt;/g;
            next if ($_ eq "");
            next if ($_ !~ /^ed2k:\/\//i);
            my @emu = split(/\|/i, $_);
            next if ($emu[3] eq "");
            my $emuchg = &unescape($emu[2]);
            if ($emuchg ne $emu[2]) {
                if ($loaduftmo ne 1) {
                    use strict;
                    use warnings;

                    use UTF8simple;
                    $loaduftmo = 1;
                }
                my $uref = new UTF8simple;
                $emu[2] = $uref->fromUTF8("UTF-8", $emuchg);
            }

            $counters++;
            if ($counters % 2 == 1) {
                $postbackcolor1 = $postcolorone;
                $postfontcolor1 = $postfontcolorone;
            }
            else {
                $postbackcolor1 = $postcolortwo;
                $postfontcolor1 = $postfontcolortwo;
            }

            $total += $emu[3];
            $totalper = $emu[3];
            if ($totalper > (1024 * 1024 * 1024 * 1024)) {
                $totalper = int($totalper * 100 / 1024 / 1024 / 1024 / 1024 + 0.5) / 100;
                $totalper .= "TB";
            }
            elsif ($totalper > (1024 * 1024 * 1024)) {
                $totalper = int($totalper * 100 / 1024 / 1024 / 1024 + 0.5) / 100;
                $totalper .= "GB";
            }
            elsif ($totalper > (1024 * 1024)) {
                $totalper = int($totalper * 100 / 1024 / 1024 + 0.5) / 100;
                $totalper .= "MB";
            }
            else {
                $totalper = int($totalper * 100 / 1024 + 0.5) / 100;
                $totalper .= "KB";
            }
            $view .= "<tr bgColor=$postbackcolor1><td width=88%><font color=$postfontcolor1><input type=\"checkbox\" name=\"emulefile$codecount\" value=\"$_\" onclick=\"em_size('emulefile$codecount');\" checked=\"checked\"><a href=\"$_\">$emu[2]</a></font></td><td align=center><font color=$postfontcolor1 title=$filename>$totalper</font></td></tr>";
        }

        if ($total > (1024 * 1024 * 1024 * 1024)) {
            $total = int($total * 100 / 1024 / 1024 / 1024 / 1024 + 0.5) / 100;
            $total .= "TB";
        }
        elsif ($total > (1024 * 1024 * 1024)) {
            $total = int($total * 100 / 1024 / 1024 / 1024 + 0.5) / 100;
            $total .= "GB";
        }
        elsif ($total > (1024 * 1024)) {
            $total = int($total * 100 / 1024 / 1024 + 0.5) / 100;
            $total .= "MB";
        }
        else {
            $total = int($total * 100 / 1024 + 0.5) / 100;
            $total .= "KB";
        }

        $view .= "<tr bgColor=$titlecolor><td align=left><input type=\"checkbox\" id=\"checkall_emulefile$codecount\" onclick=\"checkAll('emulefile$codecount',this.checked)\" checked=\"checked\"/> 全选 　　 <input type=\"button\" value=\"下载选中的文件\" onclick=\"download('emulefile$codecount',0,1)\"> 　<input type=\"button\" value=\"复制选中的链接\" onclick=\"copy('emulefile$codecount')\"><div id=\"ed2kcopy_emulefile$codecount\" style=\"position:absolute;height:0px;width:0px;overflow:hidden;\"></div></td><td align=center id=\"size_emulefile$codecount\">$total</td></tr></table>";

        $$post =~ s/\[emule\](.+?)\[\/emule\]/$view/is;
        $codecount++;
    }
}
1;
