#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";

# クッキーよりセッションデータ取得
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
#my $LOGIN = logincheck($S{login_id},$S{login_pass});

# クッキー書き込み
print "Set-Cookie:"."sid=;"."path=/;"."\n";

# ページジャンプ
print "Location: $SYS->{homeurl_ssl}m_login.cgi" .'?'. "\n\n";
exit;
