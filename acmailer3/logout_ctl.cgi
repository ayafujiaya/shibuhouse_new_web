#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# クッキーよりセッションデータ取得
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

# クッキー書き込み
print "Set-Cookie:"."sid=;"."path=/;"."\n";

# ページジャンプ
print "Location: $SYS->{homeurl_ssl}login.cgi" .'?'. "\n\n";
exit;
