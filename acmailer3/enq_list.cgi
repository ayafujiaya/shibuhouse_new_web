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

# 削除
if ($FORM{del} && $FORM{id}) {
	$objAcData->DelData('enq', 'ENQ', $FORM{id});
}

# アンケートデータ取得
my @DATA = $objAcData->GetData('enq', 'ENQ');
foreach my $row (@DATA) {
	$row->{enq_data} =~ s/__<<BR>>__/\n/g;
}
$data_ref->{list} = \@DATA;

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
