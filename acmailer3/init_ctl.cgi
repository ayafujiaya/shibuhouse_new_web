#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
use MailSession;
our $SYS;

my $objAcData = new clsAcData($SYS->{data_dir});

my %COOKIE = &getcookie;
my $sid = decrypt_id($COOKIE{sid});
my $session_fn = $SYS->{dir_session}.".".$sid.".cgi";
my %FORM = &form;

my $data_ref;

# ���顼�����å�
if (&error_check(\%FORM, \$data_ref->{error_message})) {
	# ���������
	# �����ȥ�
	$FORM{title} = 'ACMAILER3.8';
	# �����󥿡�ɽ��
	$FORM{counter_disp} = 1;
	# �Хå��ʥ�С�ɽ��
	$FORM{backnumber_disp} = 1;
	# �Хå��ʥ�С�ɽ�����
	$FORM{backnumber_num} = 10;
	# ��Ͽ�桼���˼�ư�ֿ��᡼�������
	$FORM{merumaga_usermail} = 1;
	# �����Ԥ˥᡼�������
	$FORM{merumaga_adminmail} = 1;
	# ���֥륪�ץȥ���
	$FORM{double_opt} = "";
	# �������ư��
	$FORM{delmode} = "del";
	# ��ʣ�ǡ�������Ͽ
	$FORM{double_reg} = "";
	# �����¸ʸ�������å�
	$FORM{str_check} = 1;
	# �����⡼��(�Ρ��ޥ�)
	$FORM{send_type} = "0";
	# �����륵���С�
	$FORM{relay_use} = "";
	# �������¸���
	$FORM{errmail_log_num} = 10;
	# �����ǧ�ϥǥե����ON
	$FORM{delconfirm} = 1;
        # sendmail��i���ץ����
        $FORM{sendmail_i_option} = 1;
	# �ȥåץڡ������
	$FORM{free_memo} = '<img src="img/acgirl_top.jpg" />

��������ϥ������ˤ�Ȥ���褦�ˡֳƼ�����ע��֥ȥåץڡ������פˤ��Խ����Ǥ��ޤ���



ver.3.8.15 �С�����󥢥å����� 2014/02/12
������
�᡼���ۿ�������Υڡ������ܤ��Զ�����



ver.3.8.14 �С�����󥢥å����� 2013/03/21
������
Return-Path����������Զ�����



ver.3.8.13 �С�����󥢥å����� 2012/08/02
������
CSV��Ͽ�˥��ץ������ɲ�



ver.3.8.12 �С�����󥢥å����� 2011/11/15
������
�᡼�륢�ɥ쥹�˲��Ԥ����äƤ����硢��Ͽ�������˵������Զ�����



ver.3.8.11 �С�����󥢥å����� 2011/10/20
������
��˥塼ɽ�����Զ�����



ver.3.8.10 �С�����󥢥å����� 2011/10/18
������
�᡼����Ͽ����ʸ���������Ѵ��������Զ�����



ver.3.8.9 �С�����󥢥å����� 2011/09/21
������
���Ӥ���Υ᡼���ۿ��������Զ�����
HTML/�ǥ��᡼��ץ�ӥ塼��ǽ���Զ�����
����ξ��ǥ᡼����ʸ�����ڤ�Ƥ��ޤ��Զ�����

���ɲõ�ǽ
�᡼�륳�ޥ�ɥ��ץ���������ɲ�


ver.3.8.8 �С�����󥢥å����� 2011/07/08
������
ͽ���ۿ������ե����å����Զ�罤��
�᡼�륢�ɥ쥹�����ڡ����Υڡ����󥰽������Զ�罤��
Softbank�Τ��˺¤γ�ʸ�������ɤ���
�᡼���ۿ����å������Զ�罤��

ver.3.8.7 �С�����󥢥å����� 2011/03/10
������
Ĺʸ�������������˵����¸ʸ�����ʤ��Ƥ�����å��˰��ä������Զ�罤��

ver.3.8.6 �С�����󥢥å����� 2011/01/25
���ɲõ�ǽ
ͽ���Խ���ǽ���ɲ�

ver.3.8.5 �С�����󥢥å����� 2010/12/27
������
����Ͽ�ɻߵ�ǽ����ܡ�

ver.3.8.4 �С�����󥢥å����� 2010/12/17
������
�����Ǵ������̤��DOCOMOü����������Ԥ��ȼ��Ԥ����Զ�罤��

ver.3.8.3 �С�����󥢥å����� 2010/12/01
������
�ƥ��ȥ᡼�������ǿ�����Υǡ�������¸����Ƥ�����˥����ॢ���Ȥˤʤ��Զ�罤��
�᡼�륢�ɥ쥹�����Ͽ�κݤ���ʸ����ʸ�����Ѵ�����ʤ��Զ�罤��

ver.3.8.2 �С�����󥢥å����� 2010/10/18
������
PC�Ǥ�ͽ���ۿ���λ���̤�ɽ������ʤ��Զ�罤��

ver.3.8.1 �С�����󥢥å����� 2010/10/14
������
���Ӵ������̤�ͽ���ۿ���λ���̤�PC�Υ⡼�ɤ�ɽ��������Զ�罤��


';
	# ���ӥɥᥤ��
	$FORM{mobiledomain} = 'docomo.ne.jp
ezweb.ne.jp
softbank.ne.jp
vodafone.ne.jp
disney.ne.jp';
	
	# sendmailpath�����qmail���ޤޤ�Ƥ������qmail�˥����å�
	my $qmailpath = `ls -l $FORM{sendmail_path}`;
	if ($qmailpath =~ /qmail/) {
		$FORM{qmail} = 1;
	}
	
	# �����ԥǡ�������
	$objAcData->UpdAdminData(\%FORM);
	# ��ͳ���ܹ���
	$objAcData->UpdFreeColData(\%FORM);
	
	# ����ϴ����ԤΥ᡼�륢�ɥ쥹
	$FORM{email} = $FORM{admin_email};
	# ������Ͽ�������ե��å�
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	$objAcData->RegEmail(\%FORM);

        # �᡼�륻�å����
        my $mail_session = MailSession->new(
            session_dir => $SYS->{dir_session_mail}
        );

        # �Ť��᡼�륻�å����ǡ������
        $mail_session->delete_old_session_file();

	# �Ť����å����ǡ��������
	my @temp_files;
	opendir(DIR, $SYS->{dir_session});
	@temp_files = (grep !/^\.\.?$/,readdir DIR);
	closedir(DIR);
	foreach(@temp_files){
            next if $_ eq '.htaccess';
            if((time - 86400) > ((stat("$SYS->{dir_session}$_"))[9])){
                unlink "$SYS->{dir_session}$_";
            }
	}
	# �ե�����ǡ���������
	my %S;
	$S{login_id} = $FORM{login_id};
	$S{login_pass} = $FORM{login_pass};

	my %TIME = &getdatetime;
	# �ե������Ȥ鷺��pid�Ǥξ��
	$sid = "$TIME{sec}".$$;

	my $sid_e = encrypt_id($sid);
	my $sid_ec = $sid_e;
	$sid_ec =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;

	# ���å������¸
	&setsession($sid_e,%S);
	
	my ($secg, $ming, $hourg, $mdayg, $mong, $yearg, $wdayg) = gmtime(time + (86400*3));
	my @mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @week = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my $cookieexpires = sprintf("%s\, %02d-%s-%04d %02d:%02d:%02d GMT", $week[$wdayg], $mdayg, $mons[$mong], $yearg+1900, $hourg, $ming, $secg);
	print "Set-Cookie: sid=$sid_ec; path=/; \n";

	print "Location: $SYS->{homeurl_ssl}index.cgi\n\n";
	exit;


} else {
	foreach my $n (keys %FORM) {
		$data_ref->{$n} = $FORM{$n};
	}
	
	# �ե��������
	$data_ref->{form} = \%FORM;

	# HTMLɽ��
	&printhtml_tk($data_ref, "tmpl/init.tmpl");
	exit;

}

# ���顼�����å�
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	#���顼�����å�
	if (!$FORM{admin_name}) {
		push(@error, "�����п�̾�����Ϥ��Ƥ���������");
	#} elsif ($FORM{admin_name} =~ /[\"\'\@\;\:\,\.\<\>\\\[\]]/) {
	} elsif ($FORM{admin_name} =~ /[\"\'\<\>]/) {
		# ���ѤǤ��ʤ�ʸ���� "'<>���ѹ�
		push(@error, "���п�̾����ˡ�'�ס�\"�ס�<�ס�>�פϻ��ѤǤ��ޤ���");
	}
	push(@error, "���᡼�뺹�пͥ᡼�륢�ɥ쥹�����Ϥ��Ƥ���������") if !$FORM{admin_email};
	if (!CheckMailAddress($FORM{admin_email})) {
		push(@error, "���᡼�뺹�пͥ᡼�륢�ɥ쥹�����������Ϥ��Ƥ���������");
	}
	push(@error, "��������ID�����Ϥ��Ƥ���������") if !$FORM{login_id};
	push(@error, "���ѥ���ɤ����Ϥ��Ƥ���������") if !$FORM{login_pass};
	if($FORM{login_id} && ($FORM{login_id} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_id}) > 12)){
		push(@error, "��ID��Ⱦ�ѱѿ�����12�����Ǥ����겼������");
	}
	if($FORM{login_pass} && ($FORM{login_pass} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_pass}) > 12)){
		push(@error, "���ѥ���ɤ�Ⱦ�ѱѿ�����12�����Ǥ����겼������");
	}

	if ($FORM{homeurl} && $FORM{homeurl} !~ /^http\:\/\/.*/) {
		push(@error, "��CGI����URL��https://www.acmailer.jp/acmailer/�Τ褦�ʷ��������Ϥ��Ƥ���������");
	} elsif ($FORM{homeurl} !~ /^.*\/$/) {
		$$p_FORM{homeurl} .= "/";
	}

	if ($FORM{mypath} && $FORM{mypath} !~ /\/$/) {
		$$p_FORM{mypath} .= "/";
	}
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}
