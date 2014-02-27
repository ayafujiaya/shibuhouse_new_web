package MIME;
# Copyright (C) 1993-94,1997 Noboru Ikuta <noboru@ikuta.ichihara.chiba.jp>
#
# mimew.pl: MIME encoder library Ver.2.02 (1997/12/30)

$main'mimew_version = "2.02";

# $B%$%s%9%H!<%k(B : @INC $B$N%G%#%l%/%H%j!JDL>o$O(B /usr/local/lib/perl$B!K$K%3%T!<(B
#                $B$7$F2<$5$$!#(B
#
# $B;HMQNc(B1 : require 'mimew.pl';
#           $from = "From: $B@8ED(B $B>:(B <noboru\@ikuta.ichihara.chiba.jp>";
#           print &mimeencode($from);
#
# $B;HMQNc(B2 : # UNIX$B$G(BBase64$B%(%s%3!<%I$9$k>l9g(B
#           require 'mimew.pl';
#           undef $/;
#           $body = <>;
#           print &bodyencode($body);
#           print &benflush;
#
# &bodyencode($data,$coding):
#   $B%G!<%?$r(BBase64$B7A<0$^$?$O(BQuoted-Printable$B7A<0$G%(%s%3!<%I$9$k!#(B
#   $BBh(B2$B%Q%i%a!<%?$K(B"qp"$B$^$?$O(B"b64"$B$r;XDj$9$k$3$H$K$h$j%3!<%G%#%s%07A<0(B
#   $B$r;X<($9$k$3$H$,$G$-$k!#Bh(B2$B%Q%i%a!<%?$r>JN,$9$k$H(BBase64$B7A<0$G%(%s(B
#   $B%3!<%I$9$k!#(B
#   Base64$B7A<0$N%(%s%3!<%I$N>l9g$O!"(B$foldcol*3/4 $B%P%$%HC10L$GJQ49$9$k(B
#   $B$N$G!"EO$5$l$?%G!<%?$N$&$AH>C<$JItJ,$O%P%C%U%!$KJ]B8$5$l<!$K8F$P$l(B
#   $B$?$H$-$K=hM}$5$l$k!#:G8e$K%P%C%U%!$K;D$C$?%G!<%?$O(B&benflush$B$r8F$V(B
#   $B$3$H$K$h$j=hM}$5$l%P%C%U%!$+$i%/%j%"$5$l$k!#(B
#   Quoted-Printable$B7A<0$N%(%s%3!<%I$N>l9g$O!"9TC10L$GJQ49$9$k$?$a!"(B
#   $B%G!<%?$N:G8e$K2~9TJ8;z$,L5$$>l9g!":G8e$N2~9TJ8;z$N8e$m$N%G!<%?$O(B
#   $B%P%C%U%!$KJ]B8$5$l!"<!$K8F$P$l$?$H$-$K=hM}$5$l$k!#:G8e$K%P%C%U%!(B
#   $B$K;D$C$?%G!<%?$O(B&benflush("qp")$B$r8F$V$3$H$K$h$j=hM}$5$l%P%C%U%!(B
#   $B$+$i%/%j%"$5$l$k!#(B
#
# &benflush($coding):
#   $BBh(B1$B%Q%i%a!<%?$K(B"b64"$B$^$?$O(B"qp"$B$r;XDj$9$k$3$H$K$h$j!"$=$l$>$l(BBase64
#   $B7A<0$^$?$O(BQuoted-Printable$B7A<0$N%(%s%3!<%I$r;XDj$9$k$3$H$,$G$-$k!#(B
#   $BBh(B1$B%Q%i%a!<%?$K2?$b;XDj$7$J$1$l$P(BBase64$B7A<0$G%(%s%3!<%I$5$l$k!#(B
#   Base64$B$N%(%s%3!<%I$N>l9g!"(B&bodyencode$B$,=hM}$7;D$7$?%G!<%?$r=hM}$7(B
#   pad$BJ8;z$r=PNO$9$k!#(BQuoted-Printable$B$N>l9g!"9TC10L$G$J$/%V%m%C%/C1(B
#   $B0L$G(B&bodyencode$B$r8F$V>l9g!"(B&bodyencode$B$,=hM}$7;D$7$?%G!<%?$,$b$7(B
#   $B%P%C%U%!$K;D$C$F$$$l$P$=$l$r=hM}$9$k!#(B
#   $B0l$D$N%G!<%?$r(B(1$B2s$^$?$O2?2s$+$KJ,$1$F(B)&bodyencode$B$7$?8e$KI,$:(B1$B2s(B
#   $B8F$VI,MW$,$"$k!#(B
#
# &mimeencode($text):
#   $BBh(B1$B%Q%i%a!<%?$,F|K\8lJ8;zNs$r4^$s$G$$$l$P!"$=$NItJ,$r(BISO-2022-JP$B$K(B
#   $BJQ49$7$?$"$H!"(BMIME encoded-word(RFC2047$B;2>H(B)$B$KJQ49$9$k!#I,MW$K1~$8(B
#   $B$F(Bencoded-word$B$NJ,3d$H(Bencoded-word$B$NA08e$G$N9TJ,3d$r9T$&!#(B
#
#   $BJ8;z%3!<%I$N<+F0H=Dj$O!"F10l9T$K(BShiftJIS$B$H(BEUC$B$,:.:_$7$F$$$k>l9g$r(B
#   $B=|$$$F4A;z%3!<%I$N:.:_$K$bBP1~$7$F$$$k!#(BShiftJIS$B$+(BEUC$B$+$I$&$7$F$b(B
#   $BH=CG$G$-$J$$$H$-$O(B$often_use_kanji$B$K@_Dj$5$l$F$$$k%3!<%I$HH=Dj$9$k!#(B
#   ISO-2022-JP$B$N%(%9%1!<%W%7!<%1%s%9$O(B$jis_in$B$H(B$jis_out$B$K@_Dj$9$k$3$H(B
#   $B$K$h$jJQ992DG=$G$"$k!#(B

$often_use_kanji = 'EUC'; # or 'SJIS'

$jis_in  = "\x1b\$B"; # ESC-$-B ( or ESC-$-@ )
$jis_out = "\x1b\(B"; # ESC-(-B ( or ESC-(-J )

# $BG[I[>r7o(B : $BCx:n8"$OJ|4~$7$^$;$s$,!"G[I[!&2~JQ$O<+M3$H$7$^$9!#2~JQ$7$F(B
#            $BG[I[$9$k>l9g$O!"%*%j%8%J%k$H0[$J$k$3$H$rL@5-$7!"%*%j%8%J%k(B
#            $B$N%P!<%8%g%s%J%s%P!<$K2~JQHG%P!<%8%g%s%J%s%P!<$rIU2C$7$?7A(B
#            $BNc$($P(B Ver.2.02-XXXXX $B$N$h$&$J%P!<%8%g%s%J%s%P!<$rIU$1$F2<(B
#            $B$5$$!#$J$*!"(BCopyright$BI=<($OJQ99$7$J$$$G$/$@$5$$!#(B
#
# $BCm0U(B : &mimeencode$B$r(Bjperl1.X($B$N(B2$B%P%$%HJ8;zBP1~%b!<%I(B)$B$G;HMQ$9$k$H!"(BSJIS
#        $B$H(BEUC$B$r$&$^$/(B7bit JIS(ISO-2022-JP)$B$KJQ49$G$-$^$;$s!#(B
#        $BF~NO$K4^$^$l$kJ8;z$,(B7bit JIS(ISO-2022-JP)$B$H(BASCII$B$N$_$G$"$k$3$H(B
#        $B$,J]>Z$5$l$F$$$k>l9g$r=|$-!"I,$:(Boriginal$B$N1Q8lHG$N(Bperl$B!J$^$?$O(B
#        jperl1.4$B0J>e$r(B -Llatin $B%*%W%7%g%sIU$-!K$GF0$+$7$F$/$@$5$$!#(B
#        $B$J$*!"(BPerl5$BBP1~$N(Bjperl$B$O;n$7$?$3$H$,$J$$$N$G$I$N$h$&$JF0:n$K$J$k(B
#        $B$+$o$+$j$^$;$s!#(B
#
# $B;2>H(B : RFC1468, RFC2045, RFC2047

## MIME base64 $B%"%k%U%!%Y%C%H%F!<%V%k!J(BRFC2045$B$h$j!K(B
%mime = (
"000000", "A",  "000001", "B",  "000010", "C",  "000011", "D",
"000100", "E",  "000101", "F",  "000110", "G",  "000111", "H",
"001000", "I",  "001001", "J",  "001010", "K",  "001011", "L",
"001100", "M",  "001101", "N",  "001110", "O",  "001111", "P",
"010000", "Q",  "010001", "R",  "010010", "S",  "010011", "T",
"010100", "U",  "010101", "V",  "010110", "W",  "010111", "X",
"011000", "Y",  "011001", "Z",  "011010", "a",  "011011", "b",
"011100", "c",  "011101", "d",  "011110", "e",  "011111", "f",
"100000", "g",  "100001", "h",  "100010", "i",  "100011", "j",
"100100", "k",  "100101", "l",  "100110", "m",  "100111", "n",
"101000", "o",  "101001", "p",  "101010", "q",  "101011", "r",
"101100", "s",  "101101", "t",  "101110", "u",  "101111", "v",
"110000", "w",  "110001", "x",  "110010", "y",  "110011", "z",
"110100", "0",  "110101", "1",  "110110", "2",  "110111", "3",
"111000", "4",  "111001", "5",  "111010", "6",  "111011", "7",
"111100", "8",  "111101", "9",  "111110", "+",  "111111", "/",
);

## JIS$B%3!<%I(B(byte$B?t(B)$B"*(Bencoded-word $B$NJ8;z?tBP1~(B
%mimelen = (
 8,30, 10,34, 12,34, 14,38, 16,42,
18,42, 20,46, 22,50, 24,50, 26,54,
28,58, 30,58, 32,62, 34,66, 36,66,
38,70, 40,74, 42,74,
);

## $B%X%C%@%(%s%3!<%I;~$N9T$ND9$5$N@)8B(B
$limit=74; ## $B!vCm0U!v(B $limit$B$r(B75$B$h$jBg$-$$?t;z$K@_Dj$7$F$O$$$1$J$$!#(B

## $B%\%G%#(Bbase64$B%(%s%3!<%I;~$N9T$ND9$5$N@)8B(B
$foldcol=72; ## $B!vCm0U!v(B $foldcol$B$O(B76$B0J2<$N(B4$B$NG\?t$K@_Dj$9$k$3$H!#(B

## $B%\%G%#(BQuoted-Printable$B%(%s%3!<%I;~$N9T$ND9$5$N@)8B(B
$qfoldcol=75; ## $B!vCm0U!v(B $foldcol$B$O(B76$B0J2<$K@_Dj$9$k$3$H!#(B

## null bit$B$NA^F~$H(B pad$BJ8;z$NA^F~$N$?$a$N%F!<%V%k(B
@zero = ( "", "00000", "0000", "000", "00", "0" );
@pad  = ( "", "===",   "==",   "=" );

## ASCII, 7bit JIS, Shift-JIS $B5Z$S(B EUC $B$N3F!9$K%^%C%A$9$k%Q%?!<%s(B
$match_ascii = '\x1b\([BHJ]([\t\x20-\x7e]*)';
$match_jis = '\x1b\$[@B](([\x21-\x7e]{2})*)';
$match_sjis = '([\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc])+';
$match_euc  = '([\xa1-\xfe]{2})+';

## MIME Part 2(charset=`ISO-2022-JP',encoding=`B') $B$N(B head $B$H(B tail
$mime_head = '=?ISO-2022-JP?B?';
$mime_tail = '?=';

## &bodyencode $B$,;H$&=hM};D$7%G!<%?MQ%P%C%U%!(B
$benbuf = "";

## &bodyencode $B$N=hM}C10L!J%P%$%H!K(B
$bensize = int($foldcol/4)*3;

## &mimeencode interface ##
sub main'mimeencode {
    local($_) = @_;
    s/$match_jis/$jis_in$1/go;
    s/$match_ascii/$jis_out$1/go;
    $kanji = &checkkanji;
    s/$match_sjis/&s2j($&)/geo if ($kanji eq 'SJIS');
    s/$match_euc/&e2j($&)/geo if ($kanji eq 'EUC');
    s/(\x1b[\$\(][BHJ@])+/$1/g;
    1 while s/(\x1b\$[B@][\x21-\x7e]+)\x1b\$[B@]/$1/;
    1 while s/$match_jis/&mimeencode($&,$`,$')/eo;
    s/$match_ascii/$1/go;
    $_;
}

## &bodyencode interface ##
sub main'bodyencode {
    local($_,$coding) = @_;
    if (!defined($coding) || $coding eq "" || $coding eq "b64"){
	$_ = $benbuf . $_;
	local($cut) = int((length)/$bensize)*$bensize;
	$benbuf = substr($_, $cut+$[);
	$_ = substr($_, $[, $cut);
	$_ = &base64encode($_);
	s/.{$foldcol}/$&\n/g;
    }elsif ($coding eq "qp"){
	# $benbuf $B$,6u$G$J$1$l$P%G!<%?$N:G=i$KDI2C$9$k(B
	$_ = $benbuf . $_;

	# $B2~9TJ8;z$r@55,2=$9$k(B
	s/\r\n/\n/g;
	s/\r/\n/g;

	# $B%G!<%?$r9TC10L$KJ,3d$9$k(B($B:G8e$N2~9TJ8;z0J9_$r(B $benbuf $B$KJ]B8$9$k(B)
	@line = split(/\n/,$_,-1);
	$benbuf = pop(@line);

	local($result) = "";
	foreach (@line){
	    $_ = &qpencode($_);
	    $result .= $_ . "\n";
	}
	$_ = $result;
    }
    $_;
}

## &benflush interface ##
sub main'benflush {
    local($coding) = @_;
    local($ret) = "";
    if ((!defined($coding) || $coding eq "" || $coding eq "b64")
	&& $benbuf ne ""){
        $ret = &base64encode($benbuf) . "\n";
        $benbuf = "";
    }elsif ($coding eq "qp" && $benbuf ne ""){
	$ret = &qpencode($benbuf) . "\n";
	$benbuf = "";
    }
    $ret;
}

## MIME $B%X%C%@%(%s%3!<%G%#%s%0(B
sub mimeencode {
    local($_, $befor, $after) = @_;
    local($back, $forw, $blen, $len, $flen, $str);
    $befor = substr($befor, rindex($befor, "\n")+1);
    $after = substr($after, 0, index($after, "\n")-$[);
    $back = " " unless ($befor eq ""
                     || $befor =~ /[ \t\(]$/);
    $forw = " " unless ($after =~ /^\x1b\([BHJ]$/
                     || $after =~ /^\x1b\([BHJ][ \t\)]/);
    $blen = length($befor);
    $flen = length($forw)+length($&)-3 if ($after =~ /^$match_ascii/o);
    $len = length($_);
    return "" if ($len <= 3);
    if ($len > 39 || $blen + $mimelen{$len+3} > $limit){
        if ($limit-$blen < 30){
            $len = 0;
        }else{
            $len = int(($limit-$blen-26)/4)*2+3;
        }
        if ($len >= 5){
            $str = substr($_, 0, $len).$jis_out;
            $str = &base64encode($str);
            $str = $mime_head.$str.$mime_tail;
            $back.$str."\n ".$jis_in.substr($_, $len);
        }else{
            "\n ".$_;
        }
    }else{
        $_ .= $jis_out;
        $_ = &base64encode($_);
        $_ = $back.$mime_head.$_.$mime_tail;
        if ($blen + (length) + $flen > $limit){
            $_."\n ";
        }else{
            $_.$forw;
        }
    }
}

## MIME base64 $B%(%s%3!<%G%#%s%0(B
sub base64encode {
    local($_) = @_;
    $_ = unpack("B".((length)<<3), $_);
    $_ .= $zero[(length)%6];
    s/.{6}/$mime{$&}/go;
    $_.$pad[(length)%4];
}

## Quoted-Printable $B%(%s%3!<%G%#%s%0(B
sub qpencode {
    local($_) = @_;

    # `=' $BJ8;z$r(B16$B?JI=8=$KJQ49$9$k(B
    s/=/=3D/g;

    # $B9TKv$N%?%V$H%9%Z!<%9$r(B16$B?JI=8=$KJQ49$9$k(B
    s/\t$/=09/;
    s/ $/=20/;

    # $B0u;z2DG=J8;z(B(`!'$B!A(B`~')$B0J30$NJ8;z$r(B16$B?JI=8=$KJQ49$9$k(B
    s/([^!-~ \t])/&qphex($1)/ge;

    # 1$B9T$,(B$qfoldcol$BJ8;z0J2<$K$J$k$h$&$K%=%U%H2~9T$r$$$l$k(B
    local($folded, $line) = "";
    while (length($_) > $qfoldcol){
	$line = substr($_, 0, $qfoldcol-1);
	if ($line =~ /=$/){
	    $line = substr($_, 0, $qfoldcol-2);
	    $_ = substr($_, $qfoldcol-2);
	}elsif ($line =~ /=[0-9A-Fa-f]$/){
	    $line = substr($_, 0, $qfoldcol-3);
	    $_ = substr($_, $qfoldcol-3);
	}else{
	    $_ = substr($_, $qfoldcol-1);
	}
	$folded .= $line . "=\n";
    }
    $folded . $_;
}

sub qphex {
    local($_) = @_;
    $_ = '=' . unpack("H2", $_);
    tr/a-f/A-F/;
    $_;
}

## Shift-JIS $B$H(B EUC $B$N$I$A$i$N4A;z%3!<%I$,4^$^$l$k$+$r%A%'%C%/(B
sub checkkanji {
    local($sjis,$euc);
    $sjis += length($&) while(/$match_sjis/go);
    $euc  += length($&) while(/$match_euc/go);
    return 'NONE' if ($sjis == 0 && $euc == 0);
    return 'SJIS' if ($sjis > $euc);
    return 'EUC'  if ($sjis < $euc);
    $often_use_kanji;
}

## EUC $B$r(B 7bit JIS $B$KJQ49(B
sub e2j {
    local($_) = @_;
    tr/\xa1-\xfe/\x21-\x7e/;
    $jis_in.$_.$jis_out;
}

## Shift-JIS $B$r(B 7bit JIS $B$KJQ49(B
sub s2j {
    local($string);
    local(@ch) = split(//, $_[0]);
    while(($j1,$j2)=unpack("CC",shift(@ch).shift(@ch))){
        if ($j2 > 0x9e){
            $j1 = (($j1>0x9f ? $j1-0xb1 : $j1-0x71)<<1)+2;
            $j2 -= 0x7e;
        }
        else{
            $j1 = (($j1>0x9f ? $j1-0xb1 : $j1-0x71)<<1)+1;
            $j2 -= ($j2>0x7e ? 0x20 : 0x1f);
        }
        $string .= pack("CC", $j1, $j2);
    }
    $jis_in.$string.$jis_out;
}
1;
