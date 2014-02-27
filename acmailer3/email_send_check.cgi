#!/usr/bin/perl
use strict;
BEGIN {
    use lib "./lib/";
    require "./lib/setup.cgi";
};
use MailSession;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange", "noencode");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
if ($FORM{sid}) { $COOKIE{sid} = $FORM{sid}; }


# �᡼�륻�å����
my $mail_session = MailSession->new(
    mail_id     => $FORM{mail_session_id},
    session_dir => $SYS->{dir_session_mail},
);


# ���ꥸ�ʥ���ʸ�ȷ�̾����¸
my $body_org = $FORM{mail_body};
my $subject_org = $FORM{mail_title};

# ���å��������
foreach my $n (qw(mail_title mail_body sender_mail email_send_id)) {
    $S{$n} = "";
}

# body �� subject�ʳ��򥨥󥳡���
foreach my $n (keys %FORM) {
    if ($n ne "mail_body" && $n ne "mail_title") {
	my $value = $FORM{$n};
	$FORM{$n} = $value;
    }
}


my $data_ref = $admindata;


# �������̤����꤬�Ԥ��Ƥ��뤫�ɤ���
&CheckAdminData_MailSend($admindata);

# ���顼�����å�
&error_check(\%FORM, \$data_ref);

# �������ܺ���
my @search = $objAcData->MakeSearchCol(\%FORM, $SYS->{max_colnum});
$data_ref->{search} = \@search;

# �᡼��ǡ�������
my @DATA = $objAcData->GetData('mail', 'MAIL');

# ��ʣ�����å�
&CheckDoubleData(\@DATA, $admindata);

$data_ref->{totalnum} = $#DATA+1;

# �طʿ�
if ($FORM{bgcolor}) {
    # BODY������������ִ�
    if ($FORM{mail_body} =~ s/\<BODY(.*)?\>/\<BODY$1 bgcolor\=\"$FORM{bgcolor}\"\>/i) {
    } else {
	$FORM{mail_body} = '<body bgcolor="'.$FORM{bgcolor}.'">'.$FORM{mail_body}.'</body>';
    }
}

# ��̾
$data_ref->{mail_title} = $FORM{mail_title};
my $session_mail_title = $FORM{mail_title};


# ��ʸ
$data_ref->{mail_body} =$FORM{mail_body};
my $session_mail_body = $FORM{mail_body};


# �᡼�����򥻥å����˳�Ǽ
$session_mail_title =~ s/;/__<<semicolon>>__/gi;
$session_mail_body  =~ s/;/__<<semicolon>>__/gi;
$session_mail_title =~ s/=/__<<equal>>__/gi;
$session_mail_body  =~ s/=/__<<equal>>__/gi;
$session_mail_title =~ s/\t//gi;
$session_mail_body  =~ s/\t//gi;

$mail_session->set('mail_title', $session_mail_title);
$mail_session->set('mail_body', $session_mail_body);



$data_ref->{'mail_title'} = &plantext2html($data_ref->{'mail_title'});
$data_ref->{'mail_body'} = &plantext2html($data_ref->{'mail_body'});

foreach my $n (qw(EMAIL REGURL DELURL YEAR MONTH DAY HOUR MINUTE SECOND WEEK WEEK-JP MONTH-00 DAY-00 HOUR-00 MINUTE-00 SECOND-00)) {
    $data_ref->{mail_title} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
    $data_ref->{mail_body} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
}

# ��ʸ���Ȳ����������ߤ����
$data_ref->{mail_body} =~ s/(\{e_.*?\})/<font color=\"blue\"><b>$1<\/b><\/font>/g;
$data_ref->{mail_title} =~ s/(\{e_.*?\})/<font color=\"blue\"><b>$1<\/b><\/font>/g;
$data_ref->{mail_body} =~ s/(\{img_.*?\})/<font color=\"blue\"><b>$1<\/b><\/font>/g;

for(1..$SYS->{max_colnum}) {
	my $n = "COL$_";
	$data_ref->{mail_title} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
	$data_ref->{mail_body} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
}
$data_ref->{mail_title} =~ s/\t/ /gi;
$data_ref->{mail_body} =~ s/\t/ /gi;

# ���������
my @DATA = $objAcData->GetData('mail', 'MAIL');

# �����ʤ����
my @DATA = $objAcData->SearchEmail(\@DATA, \%FORM, $SYS->{max_colnum});
my @predata;
my (%ZYU, $zyunum, $errornum, $i);
my $sender_data = "";
my $sendertotal = 0;
foreach my $row (@DATA){

    # �ۿ���ߤξ���NEXT
    next if(!$row->{status});

    $row->{i} = $i+1;

    my %TIME = &getdatetime();

    # �ץ�ӥ塼��10�����
    if (($i + 1) <= 10) {
	$row->{subject} = $objAcData->ReplaceMailBody($FORM{mail_title}, $admindata, $row, $SYS->{max_colnum});
	$row->{body} = $objAcData->ReplaceMailBody($FORM{mail_body}, $admindata, $row, $SYS->{max_colnum});

	$row->{subject} =~ s/\t/ /gi;
	$row->{body} =~ s/\t/ /gi;
	$row->{body} =~ s/'/��/gi;
	$row->{num} = ($i + 1);

	# �ץ�ӥ塼����ʸ��1000ʸ������
	$row->{body} = z_substr($row->{body}, 0, 1000);

	# ��ʸ��
	$row->{body} = &ReplaceEmojiDisp($row->{body});
	$row->{subject} = &ReplaceEmojiDisp($row->{subject});

	# ����������
	$row->{body} = &ReplaceImageDisp($row->{body});
	push @predata, $row;
    }

    $ZYU{$row->{email}}++;
    $i++;
    $sendertotal++;

    # ���å�����ѥǡ���
    my $emaildata = "";
    my $col = $objAcData->{MAIL_COL};
    my @col = @$col;
    foreach my $n (@col) {
	$emaildata .= $row->{$n}."\t";
    }
    $emaildata =~ s/;/__<<semicolon>>__/gi;
    $emaildata =~ s/=/__<<equal>>__/gi;
    $sender_data .= $emaildata."\n";

}
$data_ref->{pre_list} = \@predata;

if ($sendertotal == 0) { &error("�����褬����ޤ���"); }
$data_ref->{sender_total} = $sendertotal;

# ͽ���Խ��⡼�ɤξ���ͽ����񤭤���
if ($FORM{'id'} && $FORM{'regmode'} eq "hist") {
    $FORM{mail_body} = &sessionStrDecode($mail_session->get('email_send_mail_body'));
    $FORM{mail_title} = &sessionStrDecode($mail_session->get('email_send_mail_title'));
    $FORM{start_send_date} = sprintf("%04d%02d%02d%02d%02d%02d", $FORM{send_year}, $FORM{send_mon}, $FORM{send_day}, $FORM{send_hour}, $FORM{send_min}, 0);
    $FORM{status} = 3;
    $FORM{send_type} = $admindata->{send_type};
    $FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
    $FORM{deco_mode} = $mail_session->get('email_send_mode');
    for(1..5) {
	# �ʹ��ߥ����
	$FORM{"search".$_} .= $mail_session->get("search".$_);

	# �ʹ��ߥƥ�����
	$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);
	$FORM{"searchlike".$_} = $mail_session->get("searchlike".$_);
    }
    $FORM{'search_domain'} = $mail_session->get('search_domain');
    $FORM{'andor'} = $mail_session->get('andor');

    $objAcData->UpdData('hist', 'HIST', $FORM{'id'}, \%FORM);

    $mail_session->clear();

    print "Location: hist_detail.cgi?editok=1&sid=".$FORM{'sid'}."&id=".$FORM{'id'}."\n\n";
    exit;
}



# ��ͳ���ܼ���
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');

# ���å������¸�ѹʹ��ߥƥ�����
for(1..5) {
    $mail_session->set("search".$_     , $FORM{"search".$_});
    $mail_session->set("search_text".$_, $FORM{"search_text".$_});
    $mail_session->set("searchlike".$_ , $FORM{"searchlike".$_});
}

$mail_session->set('search_domain', $FORM{'search_domain'});
$mail_session->set('andor', $FORM{'andor'});


# �����
$FORM{mail_body} = $mail_session->get('mail_body');
$FORM{mail_subject} = $mail_session->get('mail_title');
foreach my $n (keys %FORM) {
    $mail_session->set('email_send_'.$n, &sessionStrEncode($FORM{$n}));
}

# ���å�������¸
&setsession($COOKIE{sid}, %S);
$mail_session->save();

# �����ѥǡ������ݻ�
my $objAcDataSender = new clsAcData($SYS->{dir_session});
$objAcDataSender->setSenderData($mail_session->mail_id(), $sender_data);

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;

# ���顼�����å�
sub error_check() {
    my $p_FORM = shift;
    my $data_ref = shift;
    my %FORM = %$p_FORM;

    # ���顼�����å�
    if (!$FORM{mail_title}) { &error("��̾�����Ϥ��Ƥ���������"); }
    if (!$FORM{mail_body})  { &error("��ʸ�����Ϥ��Ƥ���������"); }

    # ͽ���ۿ��ξ��
    if ($FORM{reserve_mode}) {
	# ͽ����֥����å�
	my %TIME = &getdatetime();
	if (!$FORM{send_year} || !$FORM{send_mon} || !$FORM{send_day} || $FORM{send_hour} eq "" || $FORM{send_min} eq "") { &error("ͽ���ۿ�������ξ����ۿ����������򤷤Ƥ���������"); }
	# ���ߤ����֤���ξ��
	if ("$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}" > sprintf("%04d%02d%02d%02d%02d", $FORM{send_year}, $FORM{send_mon}, $FORM{send_day}, $FORM{send_hour}, $FORM{send_min})) {
	    &error("�ۿ����������꤬���ߤ����ˤʤäƤ��ޤ���");
	}
	# ���դ�¸�ߤ��Ƥ��뤫�ɤ��������å�
	if ( !day_exists($FORM{send_year}, $FORM{send_mon}, $FORM{send_day}) ) {
	    &error("¸�ߤ��Ƥ��ʤ����դǤ���");
	}

	foreach my $n (qw(send_year send_mon send_day send_hour send_min reserve_mode)) {
	    if ($n eq "send_year") {
		$$data_ref->{$n} = sprintf("%04d", $FORM{$n});
	    } else {
		$$data_ref->{$n} = sprintf("%02d", $FORM{$n});
	    }
	}
    }

    # �����¸�����å�
    if ($admindata->{str_check}) { &kisyuizon_check($FORM{mail_title}); }
    if ($admindata->{str_check}) { &kisyuizon_check($FORM{mail_body}); }

    return 1;

}
