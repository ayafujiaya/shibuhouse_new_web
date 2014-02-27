#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

print "Content-type: text/html; charset=EUC-JP\n\n";

# 予約配信
if ($admindata->{reserve}) {
	system("./lib/reserve.pl");
	print "OK";
} else {
	print "予約配信設定が行われていません。";
}

exit;
