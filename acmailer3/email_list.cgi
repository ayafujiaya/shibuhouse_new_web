#!/usr/bin/perl
use strict;
BEGIN {
    use lib "./lib/";
    require "./lib/setup.cgi";
};


our $SYS;


# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
if ($FORM{sid}) { $COOKIE{sid} = $FORM{sid}; }


my $data_ref;

# �ۿ��ե饰����
if ($FORM{mode} eq "cng_send_flg") {
    # �ǡ�������
    $objAcData->UpdMailStatus(\%FORM);
    $FORM{'back'} = 1;
}

# ������������
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

# �ѥ�᡼������
$data_ref->{para} = &MakePara(\%FORM);
$data_ref->{allhidden} = &MakePara(\%FORM, "post");
$data_ref->{search_url} = $data_ref->{para};

my $para_non_order = $data_ref->{para};
$para_non_order =~ s/&order\=.*?(&?)/$1/;
$data_ref->{para_non_order} = $para_non_order;


# �������ܺ���
my @search = $objAcData->MakeSearchCol(\%FORM, $SYS->{max_colnum});
$data_ref->{search} = \@search;

# �᡼�륢�ɥ쥹����
my @DATA = $objAcData->GetData('mail', 'MAIL');

# ����
my @DATA = $objAcData->SearchEmail(\@DATA, \%FORM, $SYS->{max_colnum});

# CSV����
if ($FORM{csv}) {
    my @CSV;

    # ��ͳ���ܼ���
    my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
    my $colname;
    $colname->{email} = "E-MAIL";
    my $i = 1;
    foreach my $ref (@freecol) {
	$colname->{"col".$i} = $ref->{"colname"};
	$i++;
    }
    $colname->{status} = "���ơ�����";
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

# ɽ���������
my $dispcol = $objAcData->GetRowData('dispcol', 'DISPCOL');
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
foreach my $ref (@DATA) {
    my $i = 1;
    # ɽ������
    my @col = @{$objAcData->{DISPCOL_COL}};
    foreach my $n (@col) {
	if ($dispcol->{$n} eq "email") {
	    # �᡼�륢�ɥ쥹
	    $ref->{"dispdata".$i} = $ref->{email};
	    $data_ref->{"dispcolname".$i} = "�᡼�륢�ɥ쥹";
	} elsif ($dispcol->{$n} eq "add_date") {
	    # ��Ͽ����
	    $ref->{"dispdata".$i} = $ref->{add_date};
	    $data_ref->{"dispcolname".$i} = "��Ͽ����";
	} elsif ($dispcol->{$n} eq "edit_date") {
	    # ��������
	    $ref->{"dispdata".$i} = $ref->{edit_date};
	    $data_ref->{"dispcolname".$i} = "��������";
	} else {
	    # ɽ���ǡ���
	    $ref->{"dispdata".$i} = $ref->{"col".$dispcol->{$n}};
	    # ɽ�������
	    $data_ref->{"dispcolname".$i} = $freecol->{"col".$dispcol->{$n}."name"};
	}
	$i++;
    }
}

# ɽ������
@DATA = &SortData(\@DATA, $FORM{order});

# �ڡ����󥰽���
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, $data_ref->{para});
@DATA = $objPaging->MakePaging(\@DATA, \$data_ref);
$data_ref->{loop} = \@DATA;

# ����������Ƚ���
$data_ref->{zyunum} = $FORM{zyunum} || 0;
$data_ref->{errornum} = $FORM{errornum} || 0;

$data_ref->{sendstopnum} = $FORM{sendstopnum};
if (!$data_ref->{sendstopnum}) { $data_ref->{sendstopnum} = 0; }
if ($admindata->{double_reg}) {
	$data_ref->{emailnum} = $data_ref->{totalnum} - $data_ref->{errornum} - $data_ref->{sendstopnum};
} else {
	$data_ref->{emailnum} = $data_ref->{totalnum} - $data_ref->{zyunum} - $data_ref->{errornum} - $data_ref->{sendstopnum};
}

# ��Ͽ��å�����
$data_ref->{oktext} = "������Ͽ����ޤ�����" if $FORM{okadd};
$data_ref->{oktext} = "�ѹ�����ޤ�����" if $FORM{okedit};
$data_ref->{oktext} = "�������ޤ�����" if $FORM{okdel};
$data_ref->{oktext} = "��ʣ�᡼�뤬���������ޤ�����" if $FORM{okzyudel};
$data_ref->{oktext} = "���顼�᡼�뤬���������ޤ�����" if $FORM{okerrordel};
$data_ref->{oktext} = "�᡼�륢�ɥ쥹�������������ޤ�����" if $FORM{okalldel};

# ����Ѥ˸����ݻ�
foreach my $n (keys %S) {
    if ($n =~ /^email_list_.*/) {
	$S{$n} = "";
    }
}
foreach my $n (keys %FORM) {
    $S{'email_list_'.$n} = $FORM{$n};
}


# ���å�������¸
&setsession($COOKIE{sid}, %S);

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;

# ɽ������
sub SortData() {
    my $DATA = shift;
    my $sort = shift;
    my @DATA = @$DATA;

    return @DATA if(!$sort);

    for(1..3) {
	if ($sort eq "disp".$_."_asc") {
	    # ����
	    @DATA = sort { $b->{"dispdata".$_} cmp $a->{"dispdata".$_} } @DATA;
	} elsif ($sort eq "disp".$_."_desc") {
	    # �߽�
	    @DATA = sort { $a->{"dispdata".$_} cmp $b->{"dispdata".$_} } @DATA;
	}
    }

    # �ֹ�򿶤�ľ��
    my $i = 1;

    foreach my $ref (@DATA) {
	$ref->{i} = $i;
	$i++;
    }

    return @DATA;
}

# �ѥ�᡼������
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
	# ���Ӥξ���SID���ղ�
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
	# ���Ӥξ���SID���ղ�
	if (&isMobile()) {
	    $para .= "&sid=".$FORM{sid};
	}
    }
    return $para;
}
