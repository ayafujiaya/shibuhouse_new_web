#=====================================================================
#   DATE.pm : DATE/TIME conversion functions
#
#   Copyright(c) 2001, Nobuchika Oishi (BSC CONSULTING).
#
#   e-mail : bigstone@my.email.ne.jp
#   support: http://www.din.or.jp/~bigstone/cgilab/index.html
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND
#   ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.
#
#   ver 1.0.2 : updated last on 2001/11/25
#
#=====================================================================
package DATE;

use strict;
use vars qw(
    @ISA @EXPORT_OK %EXPORT_TAGS $VERSION $TIMEZONE
    $ZONESTR @DAY_OF_WEEK @MON_OF_YEAR %MON_OF_YEAR
);
require   Exporter;
@ISA = qw(Exporter);
@EXPORT_OK = qw(
    str2time
    time2str
    time2local
    str2local
    time2iso
    time2isoz
    date2time
    date2local
    time2date
    prev_mday
    next_mday
    prev_month
    next_month
    end_of_month
    is_leap_year
);
%EXPORT_TAGS = (
    all => [ @EXPORT_OK ],
);

$VERSION  = '1.0.2';
$TIMEZONE = 9 * 60 * 60;    # Japan is GMT+0900
$ZONESTR  = '+0900';

@DAY_OF_WEEK = qw(Sun Mon Tue Wed Thu Fri Sat);
@MON_OF_YEAR = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
@MON_OF_YEAR{ @MON_OF_YEAR } = (1..12);


sub time2date (;$$$) {
    my($pat, $time, $zone) = @_;
    $time ||= time;
    $zone = $TIMEZONE unless defined $zone;
    my @t = gmtime($time + $zone);
    $t[5] += 1900;
    $t[4] += 1;
    if($pat){
        my %time = (
            'Y' => sprintf("%04d", $t[5]),
            'M' => sprintf("%02d", $t[4]),
            'D' => sprintf("%02d", $t[3]),
            'h' => sprintf("%02d", $t[2]),
            'm' => sprintf("%02d", $t[1]),
            's' => sprintf("%02d", $t[0]),
            'd' => sprintf("%03d", $t[7]),
            'W' => $DAY_OF_WEEK[$t[6]],
        );
        $time{'y'} = substr($time{'Y'}, 2);
        $pat =~ s/%([DMYWdhmsy])/$time{$1}/g;
    }
    return $pat || (@t[5, 4, 3, 2, 1, 0, 6, 7]);
}

sub str2time ($) {
    my $str = shift || return undef;
    eval 'require Time::Local;';
    if($@){
        return undef;
    }
    if($str =~ /^[SMTWF][a-z][a-z], (\d+) ([JFMAJSOND][a-z][a-z]) (\d+) (\d+):(\d+):(\d+) GMT$/o){
        return eval {
            my $t = Time::Local::timegm($6, $5, $4, $1, $MON_OF_YEAR{$2}-1, $3-1900);
            $t < 0 ? undef : $t;
        };
    }
    return undef;
}

sub time2str (;$) {
    my $time = shift; $time ||= time;
    my @t = gmtime($time);
    sprintf("%s, %02d %s %04d %02d:%02d:%02d GMT",
        $DAY_OF_WEEK[$t[6]],
        $t[3],
        $MON_OF_YEAR[$t[4]],
        $t[5]+1900,
        $t[2],
        $t[1],
        $t[0]);
}

sub time2local (;$$$) {
    my($time, $zone, $expr) = @_;
    $time ||= time;
    $zone = $TIMEZONE unless defined $zone;
    $expr = $ZONESTR  unless defined $expr;
    my @t = gmtime($time + $zone);
    sprintf("%s, %02d %s %04d %02d:%02d:%02d $expr",
        $DAY_OF_WEEK[$t[6]],
        $t[3],
        $MON_OF_YEAR[$t[4]],
        $t[5]+1900,
        $t[2],
        $t[1],
        $t[0]);
}

sub str2local ($;$$) {
    my $str = shift || return undef;
    my($zone, $expr) = @_;
    time2local(str2time($str), $zone, $expr);
}

sub time2iso (;$$) {
    my($time, $zone) = @_;
    $time ||= time;
    $zone = $TIMEZONE unless defined $zone;
    my @t = gmtime($time + $zone);
    sprintf("%04d-%02d-%02d %02d:%02d:%02d",
        $t[5]+1900,
        $t[4]+1,
        $t[3],
        $t[2],
        $t[1],
        $t[0]);
}

sub time2isoz (;$) {
    my $time = shift; $time ||= time;
    my @t = gmtime($time);
    sprintf("%04d-%02d-%02d %02d:%02d:%02dZ",
        $t[5]+1900,
        $t[4]+1,
        $t[3],
        $t[2],
        $t[1],
        $t[0]);
}

sub local2time ($) {
    my $str = shift || return undef;
    eval 'require Time::Local;';
    if($@){
        return undef;
    }
    if($str =~ /^[SMTWF][a-z][a-z], (\d+) ([JFMAJSOND][a-z][a-z]) (\d+) (\d+):(\d+):(\d+) ([\+\-])(\d\d)(\d\d)/o){
        my $day  = $1;
        my $mon  = $MON_OF_YEAR{$2},
        my $year = $3;
        my $hour = $4;
        my $min  = $5;
        my $sec  = $6;
        if($7 eq '-'){
            $min  += $9; if($min  >= 60){ $min  = $min  - 60; $hour += 1; }
            $hour += $8; if($hour >= 24){ $hour = $hour - 24; $day = next_mday($year, $mon, $day); }
        } else {
            $min  -= $9; if($min  < 0){ $min  = $min  + 60; $hour -= 1; }
            $hour -= $8; if($hour < 0){ $hour = $hour + 24; $day = prev_mday($year, $mon, $day); }
        }
        return eval {
            my $t = Time::Local::timegm($sec, $min, $hour, $day, $mon-1, $year-1900);
            $t < 0 ? undef : $t;
        };
    }
    return undef;
}

sub local2local ($;$$) {
    my $str = shift || return undef;
    my($zone, $expr) = @_;
    time2local(local2time($str), $zone, $expr);
}

sub prev_mday ($$$) {
    my($year, $mon, $day) = @_;
    $day -= 1;
    if($day < 0){
        ($year, $mon) = prev_month($year, $mon);
        $day = end_of_month($year, $mon);
    }
    ($year, $mon, $day);
}

sub next_mday ($$$) {
    my($year, $mon, $day) = @_;
    $day += 1;
    if($day > end_of_month($year, $mon)){
        ($year, $mon) = next_month($year, $mon);
        $day = 1;
    }
    ($year, $mon, $day);
}

sub prev_month ($$) {
    my($year, $mon) = @_;
    $mon -= 1;
    if($mon < 1){ $mon = 12; $year -= 1; }
    ($year, $mon);
}

sub next_month ($$) {
    my($year, $mon) = @_;
    $mon += 1;
    if($mon > 12){ $mon = 1; $year += 1; }
    ($year, $mon);
}

sub end_of_month ($$) {
    my($year, $mon) = @_;
    if($mon == 2 && is_leap_year($year)){
        return (29);
    }
    (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[--$mon];
}

sub is_leap_year ($) {
    my $year = shift;
    return undef if(($year % 4) != 0);
    return undef if(($year % 100) == 0 && ($year % 400) != 0);
    1;
}

1;

__END__
