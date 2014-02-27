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

if ($FORM{reg}) {
	# エラーチェック
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# 改行取り除き
		$FORM{enq_data} =~ s/\r\n|\r|\n/__<<BR>>__/g;
		if ($FORM{id}) {
			# 更新
			$objAcData->UpdData('enq', 'ENQ', $FORM{id}, \%FORM);
		} else {
			# 登録
			$FORM{id} = time().$$;
			$objAcData->InsData('enq', 'ENQ', \%FORM);
		}
		# 一覧へ
		print "Location: enq_list.cgi?okedit=1 \n\n";
		exit;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} elsif ($FORM{id}) {
	# データ取得
	my $data = $objAcData->GetData('enq', 'ENQ', $FORM{id});
	$data->{enq_data} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
}

$data_ref->{oktext} = "変更されました。" if $FORM{okedit};

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;

# エラーチェック
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my @error;
	if ($FORM{enq_name} eq "") {
		push(@error, "アンケート名を入力してください。");
	}
	if ($FORM{enq_key} eq "") {
		push(@error, "アンケートキーを入力してください。");
	} elsif ($FORM{enq_key} =~ /[^a-z]/) {
		push(@error, "アンケートキーに利用できる文字は半角英字のみです。");
	}
	if ($FORM{enq_question} eq "") {
		push(@error, "アンケート内用を入力してください。");
	}
	if ($FORM{enq_data} eq "") {
		push(@error, "アンケートデータを入力してください。");
	}
	
	if ($#error >= 0) {
		$$error_message = join("<BR>", @error);
		return 0;
	}
	return 1;


}
