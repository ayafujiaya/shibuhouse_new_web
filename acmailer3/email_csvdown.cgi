#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

# 自由項目取得
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
my $colname;
foreach my $ref (@freecol) {
	$colname .= $ref->{"colname"}.",";
}
$colname .= "ステータス,";

my $mail = "E-MAIL,$colname\n";

# メールデータ全取得
my @DATA = $objAcData->GetData('mail', 'MAIL');

my $col = $objAcData->{MAIL_COL};
my @col = @$col;
foreach my $row (@DATA){
	foreach my $n (@col) {
		if ($n eq "id") { next; }
		$mail .= $row->{$n}.",";
	}
	$mail .= "\n";
}

&jcode::convert(\$mail, "sjis", "euc");
my %DATE = &getdatetime;

my $size = length $mail;
print "Content-Type: application/octet-stream\n"; 
print "Content-Disposition: attachment; filename=maildata$DATE{year}$DATE{mon}$DATE{mday}.csv\n"; 
print "Content-Length: $size\n\n"; 

print $mail;
exit;
