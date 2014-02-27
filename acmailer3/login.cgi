#!/usr/bin/perl

our $SYS;
use lib "./lib/";
require "./lib/setup.cgi";
use clsMail;
use strict;

# �����������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my $data_ref = $admindata;
my %FORM = &form();
my $template;


if ($FORM{mode} eq "forget") {
	if ($FORM{send}) {
		if (!$FORM{email}) {
			$data_ref->{error_message} = "�᡼�륢�ɥ쥹�����Ϥ��Ƥ���������";
		} elsif ($FORM{email} ne $admindata->{admin_email}) {
			$data_ref->{error_message} = "�᡼�륢�ɥ쥹�����פ��ޤ���";
		} else {
			# �᡼�������
			my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

			my $subject = "�ѥ���ɺ�����";
			my $body = "�ѥ���ɤ���������ޤ���
���ʤ�����Ͽ����Ƥ���ѥ���ɤ� ".$admindata->{login_pass}."�Ǥ���";
			my $objMail = new clsMail();
			$objMail->send($admindata->{sendmail_path},$FORM{email},$subject,$body,$sendername,$admindata->{admin_email},'',$admindata->{admin_email}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
			$data_ref->{sendok} = 1;
		}
	}
	# �ѥ���ɺ��������̤�ɽ��
	$template = "tmpl/forget.tmpl";
} elsif ($data_ref->{login_id} && $data_ref->{login_pass}) {

} else {
	# SENDMAIL�ѥ���õ��
	if (-e "/usr/sbin/sendmail") {
		$data_ref->{sendmail_path} = "/usr/sbin/sendmail";
	} elsif (-e "/usr/lib/sendmail") {
		$data_ref->{sendmail_path} = "/usr/lib/sendmail";
	}
	# CGI����URL�����
	my $regcgi = $ENV{REQUEST_URI};
	if ($regcgi =~ /(.*)\/[^\/]*login\.cgi.*$/) {
		$regcgi = $1;
		if ($data_ref->{ssl}) {
			$data_ref->{homeurl} = "https://".$ENV{HTTP_HOST}.$1."/";
		} else {
			$data_ref->{homeurl} = "http://".$ENV{HTTP_HOST}.$1."/";
		}
	}
	
	# pwd���ޥ�ɤ�CGI���־������
	my $path = `pwd`;
	$path =~ s/(.*)[\s]*$/$1/;
	$data_ref->{mypath} = $path;
	
	# HTML�ƥ�ץ졼�ȥ����ץ�
	$template = "tmpl/init.tmpl";
}

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref, $template);
exit;
