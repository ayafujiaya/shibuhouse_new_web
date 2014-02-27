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
if ($FORM{sid}) { $COOKIE{sid} = $FORM{sid}; }

my $data_ref;

if ($FORM{back_number_add}) {
	# バックナンバーに追加
	$objAcData->UpdBacknumberAdd(\%FORM);
	$FORM{'back'} = 1;
	$data_ref->{backnumberok} = 1;
} elsif ($FORM{hist_del} && $FORM{id}) {
	# 履歴削除
	$objAcData->DelData('hist', 'HIST', $FORM{id});
	$FORM{'back'} = 1;
	$data_ref->{delok} = 1;
} elsif ($FORM{reserve_cancel} && $FORM{id}) {
	# 予約キャンセル
	$objAcData->HistReserveCancel($FORM{id});
	$FORM{'back'} = 1;
	$data_ref->{cancelok} = 1;
}

# 検索項目復元
if ($FORM{'back'}) {
	foreach my $n (keys %S) {
		my $form_name = $n;
		if ($form_name =~ /^hist_list_.*/) {
			$form_name =~ s/^hist_list_//g;
			$FORM{$form_name} = $S{$n};
		}
	}
}

# 履歴データ取得
my @DATA = $objAcData->GetHistLoopData();

my @HISTDATA;
my $i = 0;

foreach my $row (@DATA) {
	
	# 絞込み
	my $sdate;
	if ($FORM{s_year} && $FORM{s_mon} && $FORM{s_day}) { $sdate = sprintf("%04d", $FORM{s_year}).sprintf("%02d", $FORM{s_mon}).sprintf("%02d", $FORM{s_day}); }
	my $edate;
	if ($FORM{e_year} && $FORM{e_mon} && $FORM{e_day}) { $edate = sprintf("%04d", $FORM{e_year}).sprintf("%02d", $FORM{e_mon}).sprintf("%02d", $FORM{e_day}); }
	my $stdate = substr($row->{start_send_date}, 0, 8);
	# 年月日
	if ($sdate && $edate && ($stdate < $sdate || $stdate > $edate)) {
		next;
	} elsif ($sdate && !$edate && $stdate < $sdate) {
		next;
	} elsif ($edate && !$sdate && $stdate > $edate) {
		next;
	}
	$row->{start_send_date} = substr($row->{start_send_date}, 0, 4)."/".substr($row->{start_send_date}, 4, 2)."/".substr($row->{start_send_date}, 6, 2)." ".substr($row->{start_send_date}, 8, 2).":".substr($row->{start_send_date}, 10, 2).":".substr($row->{start_send_date}, 12, 2);
	if ($row->{end_send_date}) {
		$row->{end_send_date} = substr($row->{end_send_date}, 0, 4)."/".substr($row->{end_send_date}, 4, 2)."/".substr($row->{end_send_date}, 6, 2)." ".substr($row->{end_send_date}, 8, 2).":".substr($row->{end_send_date}, 10, 2).":".substr($row->{end_send_date}, 12, 2);
	} else {
		$row->{end_send_date} = '';
	}
	
	$row->{mail_body} =~ s/__<<BR>>__/\n/gi;
	
	if (length($row->{mail_title}) > 36) {
		$row->{mail_title} = &z_substr($row->{mail_title}, 0, 36)."…";
	}

	
	push (@HISTDATA,$row);
	
	$i++;
}


# ページング機能
foreach my $n (qw(s_year s_mon s_day e_year e_mon e_day)) {
	$data_ref->{$n} = $FORM{$n};
	$data_ref->{search_url} .= "&$n=".$FORM{$n};
}
# 携帯の場合はSIDを入れる
if (&isMobile()) {
	$data_ref->{search_url} .= "&sid=".$FORM{sid};
}
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, $data_ref->{search_url});
@HISTDATA = $objPaging->MakePaging(\@HISTDATA, \$data_ref);

# 送信先一覧
$data_ref->{hist_list} = \@HISTDATA;

# 戻る用に検索保持
foreach my $n (keys %S) {
	if ($n =~ /^hist_list_.*/) {
		$S{$n} = "";
	}
}
foreach my $n (keys %FORM) {
	$S{'hist_list_'.$n} = $FORM{$n};
}
#******************#
# セッションに保存 #
#******************#
&setsession($COOKIE{sid}, %S);

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
