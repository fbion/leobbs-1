#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

package BTINFO;
use strict;
use warnings;
use diagnostics;

use diagnostics;
use Socket;

use vars qw(@ISA @EXPORT);
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(process_file output_torrent_data);

sub process_file {
    my $body = shift;
    my $result = process_torrent_data($body);
    return "" if (!defined($result));

    my $allfileinfo = "";
    foreach my $file (@{$result->{'files'}}) {
        my $size = $file->{'size'};
        my $name = $file->{'name'};
        $allfileinfo .= "$name\|$size\t";
    }
    return "$allfileinfo\n$result->{'hash'}\n$result->{'announce'}";
}

sub output_torrent_data {
    my $hash = shift;
    my $announce = shift;
    return "" if ($announce eq "");
    my $randno = 0;
    $randno = LBCGI::myrand(2);
    return "δ֪|δ֪|δ֪" if ($randno ne 1);
    my $tracker_status = "";
    my $scrape_url = get_tracker_status_url($announce);
    my ($header, $content) = gethtml("$scrape_url?info_hash=$hash");
    ($header, $content) = gethtml("$scrape_url/?info_hash=$hash") if ($header =~ /Location:\s*(.+)\r?\n/i);
    return "δ֪|δ֪|δ֪" if ($content eq "");
    eval {$tracker_status = get_tracker_status(\$content);};
    if ($@) {return "δ֪|δ֪|δ֪";}
    if (defined($tracker_status)) {
        my %status = %{$tracker_status};
        if (exists $status{$hash}) {
            my $seeds = $status{$hash}->{'complete'};
            my $leeches = $status{$hash}->{'incomplete'};
            my $downloaded = $status{$hash}->{'downloaded'};
            return "$seeds|$leeches|$downloaded";
        }
    }

    return "δ֪|δ֪|δ֪";
}

sub process_torrent_data {
    my $body = shift;

    my %result;
    my $t = bdecode(\$body);
    my $info = $t->{'info'};
    my $s = substr($body, $t->{'_info_start'}, $t->{'_info_length'});
    my $hash = sha1_hex($s);
    my $announce = $t->{'announce'};

    $result{'hash'} = $hash;
    $result{'announce'} = $announce;
    $result{'files'} = [];
    my $tsize = 0;
    if (defined($info->{'files'})) {
        foreach my $f (@{$info->{'files'}}) {
            my %file_record = ('size' => $f->{'length'});

            $tsize += $f->{'length'};
            my $path = $f->{'path'};
            $file_record{'name'} = ref($path) eq 'ARRAY' ? $info->{'name'} . '/' . $path->[0] : $info->{'name'} . '/' . $path;
            push(@{$result{'files'}}, \%file_record);
        }
    }
    else {
        $tsize += $info->{'length'};
        push(@{$result{'files'}}, { 'size' => $info->{'length'}, 'name' => $info->{'name'} });
    }
    $result{'total_size'} = $tsize;
    return \%result;
}

sub get_tracker_status_url {
    my $url = shift;
    $url =~ s|/announce$|/scrape|ig;
    return $url;
}

sub get_tracker_status {
    my $status_body = shift;
    my $s;
    eval {$s = bdecode($status_body);};

    if ($@) {
        print STDERR "Invalid tracker response $@";
        return;
    }

    if (not exists $s->{'files'}) {
        print STDERR "Tracker returned odd results (no files)<br>";
        return undef;
    }

    my %results;
    foreach my $f (%{$s->{'files'}}) {
        my $v = $s->{'files'}{$f};
        my $fhash = bin2hex($f);
        my $seeds = $v->{'complete'} || "0";
        my $leeches = $v->{'incomplete'} || "0";
        my $downloaded = $v->{'downloaded'} || "0";

        if (exists $results{$fhash}) {
            print STDERR "Tracker has hash $fhash multiple times<br>";
        }
        $results{$fhash} = { 'complete' => $seeds, 'incomplete' => $leeches, 'downloaded' => $downloaded };
    }
    return \%results;

}

sub commify {
    local $_ = shift;
    1 while (s/^([-+]?\d+)(\d{3})/$1,$2/);
    return $_;
}

sub bin2hex {
    my $d = shift;
    $d =~ s/(.)/sprintf("%02x", ord($1))/egs;
    $d = lc($d);
    return $d;
}

sub bdecode {
    my $dataref = shift;
    die('Function bdecode takes a scalar ref!') unless (ref($dataref) eq 'SCALAR');
    my $p = 0;
    return benc_parse_hash($dataref, \$p);
}

sub benc_parse_hash {
    my ($data, $p) = @_;
    my $c = substr($$data, $$p, 1);
    my $r = undef;

    if ($c eq 'd') {
        %{$r} = ();
        ++$$p;
        while ($$p < length($$data) && substr($$data, $$p, 1) ne 'e') {
            my $k = benc_parse_string($data, $p);
            my $start = $$p;
            %{$r}->{'_' . $k . '_start'} = $$p if ($k eq 'info');
            my $v = benc_parse_hash($data, $p);
            %{$r}->{'_' . $k . '_length'} = $$p - $start if ($k eq 'info');
            %{$r}->{$k} = $v;
        }
        ++$$p;
    }
    elsif ($c eq 'l') {
        @{$r} = \();
        ++$$p;
        while (substr($$data, $$p, 1) ne 'e') {
            push(@{$r}, benc_parse_hash($data, $p));
        }
        ++$$p;
    }
    elsif ($c eq 'i') {
        $r = 0;
        my $c;
        ++$$p;
        while (($c = substr($$data, $$p, 1)) ne 'e') {
            $r *= 10;
            $r += int($c);
            ++$$p;
        }
        ++$$p;
    }
    elsif ($c =~ /\d/) {
        $r = benc_parse_string($data, $p);
    }
    else {
        die("Unknown token '$c' at $p!");
    }

    return $r;
}

sub benc_parse_string {
    my ($data, $p) = @_;
    my $l = 0;
    my $c = undef;
    my $s;
    while (($c = substr($$data, $$p, 1)) ne ':') {
        $l *= 10;
        $l += int($c);
        ++$$p;
    }
    ++$$p;
    $s = substr($$data, $$p, $l);
    $$p += $l;
    return $s;
}

sub sha1_hex {
    my $string = shift;
    my @A = (1732584193, 4023233417, 2562383102, 271733878, 3285377520, 1518500249, 1859775393, 2400959708, 3395469782);
    my @K = @A[5 .. 8];
    my ($l, $p, $r);
    my @a;

    do
    {
        my $tmp = substr($string, $a[8]++ * 64, 64);
        $r = length($tmp);
        $l += $r;

        if ($r < 64 && !$p++) {
            $r++;
            $tmp .= "\x80";
        }
        my @W = unpack('N16', $tmp . "\0" x 7);
        ($r < 57) && ($W[15] = $l * 8);

        for (16 .. 79) {
            my $tmp = $W[$_ - 3] ^ $W[$_ - 8] ^ $W[$_ - 14] ^ $W[$_ - 16];
            push(@W, ($tmp << 1) | 1 & ($tmp >> 31));
        }

        local ($a[0], $a[1], $a[2], $a[3], $a[4]) = @A;
        for (0 .. 79) {
            my $t = $_ / 20;
            $t = ($t < 1) ? ($a[1] & ($a[2] ^ $a[3]) ^ $a[3]) : ((($t < 2) || ($t >= 3)) ? ($a[1] ^ $a[2] ^ $a[3]) : (($a[1] | $a[2]) & $a[3] | $a[1] & $a[2]));
            $t += $a[4] + $W[$_] + $K[$_ / 20] + (($a[0] << 5) | (2 ** 5 - 1) & ($a[0] >> 27));
            $t -= 4294967296 * int($t / 4294967296);

            $a[4] = $a[3];
            $a[3] = $a[2];
            $a[2] = ($a[1] << 30) | (2 ** 30 - 1) & ($a[1] >> 2);
            $a[1] = $a[0];
            $a[0] = $t;
        }

        my $j = 0;
        foreach my $A (@A) {
            $A += $a[$j++];
            $A = $A - (4294967296 * int($A / 4294967296));
        }
    } while ($r > 56);

    return(sprintf('%.8x%.8x%.8x%.8x%.8x', @A));
}

sub gethtml {
    my $url = shift;
    $url =~ s/^http:\/\///isg;
    (my $host, undef) = split(/\//, $url);
    my $path = $url;
    $path =~ s/^$host//iso;
    ($host, my $port) = split(/:/, $host);
    $port = 80 if ($port eq "");
    $path = "/$path" if ($path !~ /^\//);

    my ($name, $aliases, $type, $len, @thataddr, $a, $b, $c, $d, $that);

    my ($name, $aliases, $type, $len, @thataddr) = gethostbyname($host);
    my ($a, $b, $c, $d) = unpack("C4", $thataddr[0]);
    my $that = pack('S n C4 x8', 2, $port, $a, $b, $c, $d);

    return "" unless (socket(S, 2, 1, 0));
    select(S);
    $| = 1;
    select(STDOUT);
    return "" unless (connect(S, $that));

    print S "GET $path HTTP/1.1\r\n";
    print S "Host: $host\r\n";
    print S "Accept: */*\r\n";
    print S "User-Agent: 94Cool.Net BitTorrent Agent\r\n";
    print S "Connection: close\r\n";
    print S "\r\n";

    binmode(S);
    my @results = <S>;
    close(S);
    undef $|;

    my $result = join("", @results);
    return split(/\r?\n\r?\n/, $result, 2);
}
1;