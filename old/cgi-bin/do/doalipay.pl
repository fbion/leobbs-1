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

my ($no, $alipayid, $warename, $oldpost, $wareprice, $wareurl, $postage_mail, $postage_express, $postage_ems) = split(/\[ALIPAYE\]/, $$post);

my $zanshi;
my $youfei;
$wareurl = "http://$wareurl" if ($wareurl ne "");
if ($wareurl ne "") {$zanshi = " 　[<a href=\"$wareurl\">商品展示</a>]";}
if ($postage_mail ne "" || $postage_express ne "" || $postage_ems ne "") {
    $youfei = "买家承担邮费，";
    $youfei .= "平邮 $postage_mail 元 / " if ($postage_mail ne "");
    $youfei .= "快递 $postage_express 元 / " if ($postage_express ne "");
    $youfei .= "EMS $postage_ems 元 / " if ($postage_ems ne "");
    chop $youfei;
    chop $youfei;
    chop $youfei;
}
else {
    $youfei = "卖家承担邮费";
}

my $firstline = $oldpost;
$firstline =~ s/(\[这个贴子最后由.+?在.+?次编辑\])/$1/isg;
$firstline = $1;
$oldpost =~ s/\[这个贴子最后由.+?在.+?次编辑\]<br>//isg;

my $post1 = qq~$firstline<BR><BR>
<B>卖家名称：</B> $alipayid 　[<a href=https://www.alipay.com/trade/i_credit.do?email=$alipayid target=_blank>查看该卖家信用</a>] <BR><BR>
<B>商品名称：</B> $warename$zanshi<BR><BR>
<B>商品价格：</B> $wareprice 元<BR><BR>
<B>邮费情况：</B> $youfei<BR><BR>
<B>商品描述：</B><BR>
$oldpost<BR><BR>
~;
$warename = uri_escape($warename);
$oldpost =~ s/\[UploadFile.{0,6}=.+?\]//isg;
$oldpost = &temppost($oldpost);
$oldpost = uri_escape($oldpost);
$wareurl = uri_escape($wareurl);
$$post = qq~
<a href=https://www.alipay.com/payto:$alipayid?subject=$warename&body=$oldpost&price=$wareprice&url=$wareurl&ordinary_fee=$postage_mail&express_fee=$postage_express&ems_fee=$postage_ems&readonly=true target=_blank><img src=http:\/\/img.alipay.com\/pimg\/button_alipaybutton_o.gif border=0><\/a><BR>
$post1<BR>
<a href=https://www.alipay.com/payto:$alipayid?subject=$warename&body=$oldpost&price=$wareprice&url=$wareurl&ordinary_fee=$postage_mail&express_fee=$postage_express&ems_fee=$postage_ems&readonly=true target=_blank><img src=http:\/\/img.alipay.com\/pimg\/button_alipaybutton_o.gif border=0><\/a><BR>
~;
1;