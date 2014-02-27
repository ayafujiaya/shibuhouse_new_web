#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;
# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $data_ref;
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);


my $regcgi = $ENV{REQUEST_URI};
$data_ref->{form_url} = $admindata->{homeurl}."reg.cgi";
$data_ref->{counter_url} = $admindata->{homeurl}."counter.cgi";


# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
