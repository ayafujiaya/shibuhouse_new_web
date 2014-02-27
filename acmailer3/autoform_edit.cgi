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

if ($FORM{'edit'}) {
	
	my %REGDATA;
	foreach my $n (keys %$admindata) {
		$REGDATA{$n} = $admindata->{$n};
	}
	foreach my $n (keys %FORM) {
		$REGDATA{$n} = $FORM{$n};
	}
	# ライセンス取得
	my $li = &getlicense;
	foreach my $n (keys %$li) {
		$REGDATA{$n} = $li->{$n};
	}
	
	$REGDATA{'autoform_use'} = $FORM{'autoform_use'};
	
	# エラーチェック
	if (&error_check(\%REGDATA, \$data_ref->{error_message})) {
		# 自動フォーム設定
		# 改行を置換
		for(1..$SYS->{max_colnum}) {
			$FORM{"col".$_."text"} =~ s/\r\n|\r|\n/__<<BR>>__/g;
		}
		$objAcData->ResetData("autoform", "AUTOFORM", \%FORM);

		# 管理者データ更新
		$objAcData->UpdAdminData(\%REGDATA);
		
		# 自由項目更新
		$objAcData->UpdFreeColData(\%REGDATA);
		
		# 管理者データを再取得
		$admindata = $objAcData->GetAdminData();
		$data_ref = $admindata;
		$data_ref->{okedit} = 1;
	} else {
		foreach my $n (keys %REGDATA) {
			$data_ref->{$n} = $REGDATA{$n};
		}
	}
} else {
	# 管理者データを取得
	$data_ref = $admindata;
}

# 自由項目
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

# チェックボックスのものはあらかじめ文字列を作成
foreach my $n (@freecol) {
	if ($n->{coltype} eq "checkbox") {
		$data_ref->{checkbox_list} .= ",col".$n->{num};
	}
}

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# フォームの値
$data_ref->{form} = \%FORM;

# HTML表示
&printhtml_tk($data_ref);
exit;

# エラーチェック
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}
