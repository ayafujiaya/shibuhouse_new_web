#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

if ($FORM{del}) {
    # 削除
    $objAcData->CleanDoubleOpt(\%FORM);
    $data_ref->{oktext} = "$FORM{delnum}件削除されました。";
}

# 仮登録データ取得
my @DATA = $objAcData->GetTempMailLoopData();

# ページング処理
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, "");
@DATA = $objPaging->MakePaging(\@DATA, \$data_ref);

$data_ref->{loop} = \@DATA;

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
