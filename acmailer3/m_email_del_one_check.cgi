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
my @DATA = &openfile2array("$SYS->{data_dir}hist.cgi");

if ($FORM{id} =~ /[^0-9]/ || !$FORM{id}) { &error("パラメータエラーです。"); }

# 対象データ取得
my $email = $objAcData->GetMailData($FORM{id});

print "Content-type: text/html; charset=EUC-JP\n\n";
print '

<span style="font-size:small">
<font size="1">
以下のメールを削除してもよろしいですか？
<br>
'.$email->{email}.'
<br>
<a href="email_list.cgi?back=1&sid='.$FORM{sid}.'">いいえ</a>
&nbsp;&nbsp;
<a href="email_edit.cgi?del=1&id='.$FORM{id}.'&sid='.$FORM{sid}.'">はい</a>
</font></span>
';
exit;
