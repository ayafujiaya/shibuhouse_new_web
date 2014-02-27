#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

my %FORM = &form("noexchange");
my $data_ref;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

if (!$admindata->{backnumber_disp}) {
	&error("バックナンバーは非表示に設定されています。");
}

# 履歴データ取得
my @DATA = $objAcData->GetHistLoopData();
my @BACKDATA;

my $count = 0;
my ($next_flg, $back_flg);
foreach my $row (@DATA) {
	
	# バックナンバー表示のもの
	if (!$row->{backnumber}) { next; }
	
	# バラバラ表記
	$row->{send_year} = substr($row->{start_send_date}, 0, 4);
	$row->{send_mon} = substr($row->{start_send_date}, 4, 2);
	$row->{send_day} = substr($row->{start_send_date}, 6, 2);
	$row->{send_hour} = substr($row->{start_send_date}, 8, 2);
	$row->{send_min} = substr($row->{start_send_date}, 10, 2);
	$row->{send_sec} = substr($row->{start_send_date}, 12, 2);
	$row->{send_date} = substr($row->{start_send_date}, 0, 4)."/".substr($row->{start_send_date}, 4, 2)."/".substr($row->{start_send_date}, 6, 2)." ".substr($row->{start_send_date}, 8, 2).":".substr($row->{start_send_date}, 10, 2).":".substr($row->{start_send_date}, 12, 2);
	
	# 表示日付
	$row->{start_send_date} = substr($row->{start_send_date}, 0, 4)."/".substr($row->{start_send_date}, 4, 2)."/".substr($row->{start_send_date}, 6, 2)." ".substr($row->{start_send_date}, 8, 2).":".substr($row->{start_send_date}, 10, 2).":".substr($row->{start_send_date}, 12, 2);
	$row->{end_send_date} = substr($row->{end_send_date}, 0, 4)."/".substr($row->{end_send_date}, 4, 2)."/".substr($row->{end_send_date}, 6, 2)." ".substr($row->{end_send_date}, 8, 2).":".substr($row->{end_send_date}, 10, 2).":".substr($row->{end_send_date}, 12, 2);
	
	$row->{mail_body} =~ s/__<<BR>>__/\n/gi;
	
	if ($FORM{id} eq "") { $FORM{id} = $row->{id}; $next_flg = 1; }
	
	# 前のデータ
	if ($back_flg) {
		$data_ref->{'back_id'} = $row->{id};
		$back_flg = 0;
	}
	
	# 次のデータ
	if ($FORM{id} == $row->{id}) { $next_flg = 1; $back_flg = 1;}
	if (!$next_flg) { $data_ref->{'next_id'} = $row->{id}; }
	
	# 詳細データ
	if ($FORM{id} eq $row->{id}) {
		my $col = $objAcData->{HIST_COL};
		my @col = @$col;
		foreach my $n (@col) {
			$data_ref->{$n} = $row->{$n};
		}
		foreach my $n (qw(send_year send_mon send_day send_hour send_min send_sec send_date)) {
			$data_ref->{$n} = $row->{$n};
		}
		if ($data_ref->{mail_type} eq "html") {
			# タグを取り除く
			$data_ref->{mail_body} =~ s/<.*?>//gi;
		}
	}
	
	push(@BACKDATA, $row);
	$count++;
	if ($count >= $admindata->{backnumber_num}) { last; }
}

my $template = "";
if ($FORM{mobile}) { $template = "tmpl/m_backnumber.tmpl"; }

# 送信先一覧
$data_ref->{backnumber_list} = \@BACKDATA;

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref, $template);
exit;
