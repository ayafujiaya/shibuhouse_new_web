#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
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


my $data_ref;

# ����������
for (1..5) {
    # �ʹ��ߥ����
    $FORM{"search".$_} .= $mail_session->get("search".$_);

    # �ʹ��ߥƥ�����
    $FORM{"search_text".$_} .= $mail_session->get("search_text".$_);
    $FORM{"searchlike".$_} = $mail_session->get("searchlike".$_);
}
$FORM{'search_domain'} = $mail_session->get('search_domain');
$FORM{'andor'} = $mail_session->get('andor');


$FORM{mail_title} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_body} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_title} =~ s/__<<semicolon>>__/;/gi;
$FORM{mail_body} =~ s/__<<semicolon>>__/;/gi;

$data_ref = $admindata;

# �������̤����꤬�Ԥ��Ƥ��뤫�ɤ���
&CheckAdminData_MailSend($admindata);

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

#��̾
$data_ref->{mail_title} = $FORM{mail_title};
my $session_mail_title = $FORM{mail_title};

#��ʸ
$data_ref->{mail_body} = $FORM{mail_body};
my $session_mail_body = $FORM{mail_body};

# ���å����˳�Ǽ
$mail_session->set('mail_title', $session_mail_title);
$mail_session->set('mail_body', $session_mail_body);

# ɽ����
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
$S{sender_data} = "";
my $sendertotal = 0;
foreach my $row (@DATA){
	
	# �ۿ���ߤξ���NEXT
	if (!$row->{status}) { next; }
	
	$row->{i} = $i+1;
	
	my %TIME = &getdatetime();
	
	# �����������
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
	push(@predata, $row);
	
	$ZYU{$row->{email}}++;
	$i++;
	$sendertotal++;
	
}
$data_ref->{pre_list} = \@predata;

# CSV����
if ($FORM{'down_mode'} eq "csv") {
	my @CSV;
	push(@CSV, @predata);
	
	my $mail = "E-MAIL\n";
	my @col = ('email');
	&DownloadCSV(\@CSV, \@col, 'email_data', ',');
	exit;
}

if ($sendertotal == 0) { &error("�����褬����ޤ���"); }
$data_ref->{sender_total} = $sendertotal;

# ��ͳ���ܼ���
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
