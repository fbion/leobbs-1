use strict;
use warnings;
use diagnostics;
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("发帖&你的积分为 $jifen，而本论坛只有积分大于等于 $postminjf 的才能发言！") if ($postminjf > 0 && $jifen < $postminjf);
    }

    if ($payopen eq "no") { &error("发表交易帖&对不起，本论坛不允许发表交易帖！"); }

    &error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    for ('alipayid','warename','wareurl','wareprice','transport','postage_mail','postage_express','postage_ems') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
if(length($inpost)>400){
&error("错误&商品描述不能超出400个字符");
}
&error("错误&明显不符合规定的价格")if($wareprice!~/^[0-9\.]+$/i);
&error("错误&明显不符合规定的价格")if($postage_mail!~/^[0-9\.]+$/i && $postage_mail ne '');
&error("错误&明显不符合规定的价格")if($postage_express!~/^[0-9\.]+$/i && $postage_express ne '');
&error("错误&明显不符合规定的价格")if($postage_ems!~/^[0-9\.]+$/i && $postage_ems ne '');

$transport = 's' if ($postage_mail eq "" && $postage_express eq "" && $postage_ems eq "");

if ($transport eq 's') {
    $postage_mail = "";
    $postage_express = "";
    $postage_ems = "";
}

    $alipayid  = lc($alipayid);
    $alipayid =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    if($alipayid !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &error("错误&支付宝账号错误！"); }

    $wareurl =~ s/[\a\f\n\e\0\r\t]//isg;
    $wareurl =~ s/^http:\/\///isg;

    $k="\[ALIPAYE\]$alipayid\[ALIPAYE\]$warename\[ALIPAYE\]$inpost\[ALIPAYE\]$wareprice\[ALIPAYE\]$wareurl\[ALIPAYE\]$postage_mail\[ALIPAYE\]$postage_express\[ALIPAYE\]$postage_ems\[ALIPAYE\]";
    $inpost = $k;
    
    require "doaddnewtopic.pl";

1;
