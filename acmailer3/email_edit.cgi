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

if(!$FORM{id}){
	&error("不正なアクセスです。");
}



if ($FORM{'edit'}) {
	my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
	# エラーチェック
	if (&error_check(\%FORM, \$data_ref->{error_message}, $freecol, $admindata, $objAcData)) {
		# 更新日時挿入
		my %TIME = &getdatetime();
		$FORM{'edit_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
		
		# データ更新
		$objAcData->UpdData('mail', 'MAIL', $FORM{id}, \%FORM);
		
		# 一覧へ
		my $sid = "";
		if ($FORM{sid}) { $sid = "&sid=".$FORM{sid}; }
		print "Location: email_list.cgi?back=1&okedit=1$sid \n\n";
		exit;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} elsif ($FORM{del} && $FORM{id}) {
	# 削除
	$objAcData->DelData('mail', 'MAIL', $FORM{id});
	
	# 一覧へ
	my $sid = "";
	if ($FORM{sid}) { $sid = "&sid=".$FORM{sid}; }
	print "Location: email_list.cgi?back=1&okdel=1$sid \n\n";
	exit;
} else {
	# 対象のデータ取得
	$data_ref = $objAcData->GetMailData($FORM{id});
	$data_ref->{email_org} = $data_ref->{email};
}

if(!$data_ref->{email}){
	&error("該当するデータは存在しません。");
}

# 自由項目取得
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
my $i = 1;
foreach my $row (@freecol) {
	# メール情報挿入
	$row->{col} = $data_ref->{"col".$i};
	$i++;
}
$data_ref->{freecol_list} = \@freecol;

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
	my $freecol = shift;
	my $admindata = shift;
	my $objAcData = shift;
	my %FORM = %$p_FORM;
	my @error;

	#エラーチェック
	if(!$FORM{email}){
		push(@error, "メールアドレスを入力してください。");
	}
	#エラーチェック
	if(!CheckMailAddress($FORM{email})){
		push(@error, "メールアドレスを正しく入力してください。");
	}
	
	# 重複登録がOKじゃない場合
	if (!$admindata->{double_reg} && $FORM{email} ne $FORM{email_org}) {
		my $buf = $objAcData->GetMailData("", $FORM{email});
		if ($buf->{id}) {
			push(@error, "同じメールアドレスが既に登録されています。");
		}
	}
	
	$$p_FORM{email} = lc $$p_FORM{email};
	
	my $colsdata;
	foreach(1..$SYS->{max_colnum}){
		my $col = "col".$_;
		if($freecol->{$col."checked"} && ($FORM{$col} eq "")){
			push(@error, "「".$freecol->{$col."name"}."」は必須項目です");
		}
		$FORM{$col} =~ s/,/，/g;
		$colsdata .= "\t$FORM{$col}";
	}
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;;
}
