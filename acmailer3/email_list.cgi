#!/usr/bin/perl
use strict;
BEGIN {
    use lib "./lib/";
    require "./lib/setup.cgi";
};


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

# 配信フラグ更新
if ($FORM{mode} eq "cng_send_flg") {
    # データ更新
    $objAcData->UpdMailStatus(\%FORM);
    $FORM{'back'} = 1;
}

# 検索項目復元
if ($FORM{'back'}) {
    foreach my $n (keys %S) {
	my $form_name = $n;
	if ($form_name =~ /^email_list.*/) {
	    $form_name =~ s/^email_list_//g;
	    if ($form_name eq "okedit") { next; }
	    $FORM{$form_name} = $S{$n};
	}
    }
}
$FORM{sendstopnum} = 0;

# パラメータ作成
$data_ref->{para} = &MakePara(\%FORM);
$data_ref->{allhidden} = &MakePara(\%FORM, "post");
$data_ref->{search_url} = $data_ref->{para};

my $para_non_order = $data_ref->{para};
$para_non_order =~ s/&order\=.*?(&?)/$1/;
$data_ref->{para_non_order} = $para_non_order;


# 検索項目作成
my @search = $objAcData->MakeSearchCol(\%FORM, $SYS->{max_colnum});
$data_ref->{search} = \@search;

# メールアドレス取得
my @DATA = $objAcData->GetData('mail', 'MAIL');

# 検索
my @DATA = $objAcData->SearchEmail(\@DATA, \%FORM, $SYS->{max_colnum});

# CSV出力
if ($FORM{csv}) {
    my @CSV;

    # 自由項目取得
    my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
    my $colname;
    $colname->{email} = "E-MAIL";
    my $i = 1;
    foreach my $ref (@freecol) {
	$colname->{"col".$i} = $ref->{"colname"};
	$i++;
    }
    $colname->{status} = "ステータス";
    push @CSV, $colname;
    push @CSV, @DATA;

    my $mail = "ID,E-MAIL,$colname\n";

    my @col = @{$objAcData->{MAIL_COL}};
    my @col2;
    foreach my $ref (@col) {
	if ($ref eq "id") { next; }
	push(@col2, $ref);
    }

    &DownloadCSV(\@CSV, \@col2, 'email_data', ',');

    exit;
}

# 表示設定取得
my $dispcol = $objAcData->GetRowData('dispcol', 'DISPCOL');
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
foreach my $ref (@DATA) {
    my $i = 1;
    # 表示設定
    my @col = @{$objAcData->{DISPCOL_COL}};
    foreach my $n (@col) {
	if ($dispcol->{$n} eq "email") {
	    # メールアドレス
	    $ref->{"dispdata".$i} = $ref->{email};
	    $data_ref->{"dispcolname".$i} = "メールアドレス";
	} elsif ($dispcol->{$n} eq "add_date") {
	    # 登録日時
	    $ref->{"dispdata".$i} = $ref->{add_date};
	    $data_ref->{"dispcolname".$i} = "登録日時";
	} elsif ($dispcol->{$n} eq "edit_date") {
	    # 更新日時
	    $ref->{"dispdata".$i} = $ref->{edit_date};
	    $data_ref->{"dispcolname".$i} = "更新日時";
	} else {
	    # 表示データ
	    $ref->{"dispdata".$i} = $ref->{"col".$dispcol->{$n}};
	    # 表示カラム
	    $data_ref->{"dispcolname".$i} = $freecol->{"col".$dispcol->{$n}."name"};
	}
	$i++;
    }
}

# 表示順番
@DATA = &SortData(\@DATA, $FORM{order});

# ページング処理
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, $data_ref->{para});
@DATA = $objPaging->MakePaging(\@DATA, \$data_ref);
$data_ref->{loop} = \@DATA;

# 上部カウント処理
$data_ref->{zyunum} = $FORM{zyunum} || 0;
$data_ref->{errornum} = $FORM{errornum} || 0;

$data_ref->{sendstopnum} = $FORM{sendstopnum};
if (!$data_ref->{sendstopnum}) { $data_ref->{sendstopnum} = 0; }
if ($admindata->{double_reg}) {
	$data_ref->{emailnum} = $data_ref->{totalnum} - $data_ref->{errornum} - $data_ref->{sendstopnum};
} else {
	$data_ref->{emailnum} = $data_ref->{totalnum} - $data_ref->{zyunum} - $data_ref->{errornum} - $data_ref->{sendstopnum};
}

# 登録メッセージ
$data_ref->{oktext} = "新規登録されました。" if $FORM{okadd};
$data_ref->{oktext} = "変更されました。" if $FORM{okedit};
$data_ref->{oktext} = "削除されました。" if $FORM{okdel};
$data_ref->{oktext} = "重複メールが一括削除されました。" if $FORM{okzyudel};
$data_ref->{oktext} = "エラーメールが一括削除されました。" if $FORM{okerrordel};
$data_ref->{oktext} = "メールアドレスが完全削除されました。" if $FORM{okalldel};

# 戻る用に検索保持
foreach my $n (keys %S) {
    if ($n =~ /^email_list_.*/) {
	$S{$n} = "";
    }
}
foreach my $n (keys %FORM) {
    $S{'email_list_'.$n} = $FORM{$n};
}


# セッションに保存
&setsession($COOKIE{sid}, %S);

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;

# 表示順番
sub SortData() {
    my $DATA = shift;
    my $sort = shift;
    my @DATA = @$DATA;

    return @DATA if(!$sort);

    for(1..3) {
	if ($sort eq "disp".$_."_asc") {
	    # 昇順
	    @DATA = sort { $b->{"dispdata".$_} cmp $a->{"dispdata".$_} } @DATA;
	} elsif ($sort eq "disp".$_."_desc") {
	    # 降順
	    @DATA = sort { $a->{"dispdata".$_} cmp $b->{"dispdata".$_} } @DATA;
	}
    }

    # 番号を振り直す
    my $i = 1;

    foreach my $ref (@DATA) {
	$ref->{i} = $i;
	$i++;
    }

    return @DATA;
}

# パラメータ作成
sub MakePara() {
    my $p_FORM = shift;
    my $opt = shift;
    my %FORM = %$p_FORM;
    my $para = "";

    if ($opt eq "post") {
	for(1..5) {
	    $para .= '<input type="hidden" name="search'.$_.'" value="'.&urlencode($FORM{"search".$_}).'">';
	    $para .= '<input type="hidden" name="search_text'.$_.'" value="'.&urlencode($FORM{"search_text".$_}).'">';
	    $para .= '<input type="hidden" name="searchlike'.$_.'" value="'.&urlencode($FORM{"searchlike".$_}).'">';
	}
	foreach my $n (qw(sendstatus search_text_free search_domain andor disp_id order)) {
	    $para .= '<input type="hidden" name="'.$n.'" value="'.&urlencode($FORM{$n}).'">';
	}
	# 携帯の場合はSIDを付加
	if (&isMobile()) {
	    $para .= '<input type="hidden" name="sid" value="'.$FORM{sid}.'">';
	}
    }
    else {
	for(1..5) {
	    $para .= "&search$_=".&urlencode($FORM{"search".$_})."&search_text$_=".&urlencode($FORM{"search_text".$_})."&searchlike$_=".&urlencode($FORM{"searchlike".$_});
	}
	foreach my $n (qw(sendstatus search_text_free search_domain andor disp_id order)) {
	    $para .= "&$n=".&urlencode($FORM{$n});
	}
	# 携帯の場合はSIDを付加
	if (&isMobile()) {
	    $para .= "&sid=".$FORM{sid};
	}
    }
    return $para;
}
