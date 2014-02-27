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
if ($FORM{id}) {
	# データ取得
	my $data = $objAcData->GetData('enq', 'ENQ', $FORM{id});
	$data->{enq_data} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
}

# 回答データ取得
my @ans = $objAcData->GetData($FORM{id}, 'ENQANS');
$data_ref->{total_count} = ($#ans + 1);

# 項目の配列作成
my %ANS;
foreach my $v (@ans) {
	if ($v->{mail_id} && $v->{answer} == $FORM{answer_id}) {
		$ANS{"mail".$v->{mail_id}} = 1;
	}
}

# 会員データ取得
my @mail = $objAcData->GetData('mail', 'MAIL');
my @list;
foreach my $row (@mail) {
	if ($ANS{"mail".$row->{id}}) {
		push(@list, $row);
	}
}

# 表示設定取得
my $dispcol = $objAcData->GetRowData('dispcol', 'DISPCOL');
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
foreach my $ref (@list) {
	my $i = 1;
	# 表示設定
	my @col = @{$objAcData->{DISPCOL_COL}};
	foreach my $n (@col) {
		if ($dispcol->{$n} eq "email") {
			# メールアドレス
			$ref->{"dispdata".$i} = $ref->{email};
			$data_ref->{"dispcolname".$i} = "メールアドレス";
		} else {
			# 表示データ
			$ref->{"dispdata".$i} = $ref->{"col".$dispcol->{$n}};
			# 表示カラム
			$data_ref->{"dispcolname".$i} = $freecol->{"col".$dispcol->{$n}."name"};
		}
		$i++;
	}
}
$data_ref->{list} = \@list;


# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
