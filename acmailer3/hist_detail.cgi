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


if ($FORM{id} =~ /[^0-9]/ || !$FORM{id}) { &error("パラメータエラーです。"); }

my $data_ref = $objAcData->GetData('hist', 'HIST', $FORM{id});

$data_ref->{start_send_date} = substr($data_ref->{start_send_date}, 0, 4)."/".substr($data_ref->{start_send_date}, 4, 2)."/".substr($data_ref->{start_send_date}, 6, 2)." ".substr($data_ref->{start_send_date}, 8, 2).":".substr($data_ref->{start_send_date}, 10, 2).":".substr($data_ref->{start_send_date}, 12, 2);

if ($data_ref->{end_send_date}) {
	$data_ref->{end_send_date} = substr($data_ref->{end_send_date}, 0, 4)."/".substr($data_ref->{end_send_date}, 4, 2)."/".substr($data_ref->{end_send_date}, 6, 2)." ".substr($data_ref->{end_send_date}, 8, 2).":".substr($data_ref->{end_send_date}, 10, 2).":".substr($data_ref->{end_send_date}, 12, 2);
	$data_ref->{bgcolor} = "#FFFFFF";
} else {
	$data_ref->{end_send_date} = '&nbsp;';
	$data_ref->{bgcolor} = "#FFCCCC";
}
if ($data_ref->{status} == 1 || !$data_ref->{status}) {
	$data_ref->{fail} = "1";
	$data_ref->{bgcolor} = "#FFCCCC";
} elsif ($data_ref->{status} == 3) {
	$data_ref->{reserve} = "1";
	$data_ref->{bgcolor} = "#CCFFFF";
} elsif ($data_ref->{status} == 4) {
	$data_ref->{reserve_cancel} = "1";
	$data_ref->{bgcolor} = "#FFCCCC";
}

$data_ref->{mail_body} =~ s/__<<BR>>__/\n/gi;

if ($data_ref->{mail_type} eq "html") {
	# タグ抜き取り
	$data_ref->{mail_body} =~ s/<.*?>//gi;
}

# 自由項目取得
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
for(1..5) {
	my $num = $_;
	# 表示カラム
	$data_ref->{"dispcolname".$num} = $freecol->{"col".$data_ref->{'search'.$num}."name"};
	if ($data_ref->{'search'.$num} eq "email") {
		$data_ref->{"dispcolname".$num} = "メールアドレス";
	}
}

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
