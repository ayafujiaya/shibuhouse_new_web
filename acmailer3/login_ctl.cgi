#!/usr/bin/perl

use lib "./lib/";
require './lib/setup.cgi';
use strict;
use MailSession;

our $SYS;

my %COOKIE = &getcookie;
my $sid = decrypt_id($COOKIE{sid});
my $session_fn = $SYS->{dir_session}.".".$sid.".cgi";

my %FORM = &form;

# ���ϥǡ��������å�
my $errordata;
$errordata .= "��������ID�����Ϥ��Ƥ���������<br>" if !$FORM{login_id};
$errordata .= "���ѥ���ɤ����Ϥ��Ƥ���������<br>" if !$FORM{login_pass};
&error("$errordata") if $errordata;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

if($admindata->{login_id} eq $FORM{login_id} && $admindata->{login_pass} eq $FORM{login_pass}){ 
}else{
	&error("ID,PW�򤴳�ǧ��������");
}


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
    if ((time - 86400) > ((stat("$SYS->{dir_session}$_"))[9])) {
        unlink "$SYS->{dir_session}$_";
    }
}



# �ե�����ǡ���������
my %S;
$S{login_id} = $FORM{login_id};
$S{login_pass} = $FORM{login_pass};

my %TIME = &getdatetime;
my %REGDATA;
foreach my $n (keys %$admindata) {
	$REGDATA{$n} = $admindata->{$n};
}
$REGDATA{last_login_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";

# �饤���󥹼���
my $li = &getlicense;
foreach my $n (keys %$li) {
	$REGDATA{$n} = $li->{$n};
}

# �����ԥǡ�������
$objAcData->UpdAdminData(\%REGDATA);



# �ե������Ȥ鷺��pid�Ǥξ��
$sid = "$TIME{sec}".$$;

my $sid_e = encrypt_id($sid);
my $sid_ec = $sid_e;
$sid_ec =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;

# ���å������¸
&setsession($sid_e,%S);

$FORM{login_id} =~ s/%([a-f\d]{2})/pack 'H2',$1/egi;

# ���å����񤭹���
if($FORM{memory}){
	my ($secg, $ming, $hourg, $mdayg, $mong, $yearg, $wdayg) = gmtime(time + (86400*30));
	my @mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @week = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my $cookieexpires = sprintf("%s\, %02d-%s-%04d %02d:%02d:%02d GMT", $week[$wdayg], $mdayg, $mons[$mong], $yearg+1900, $hourg, $ming, $secg);
	
	print "Set-Cookie: sid=$sid_ec; path=/; \n";

}else{
	
	my ($secg, $ming, $hourg, $mdayg, $mong, $yearg, $wdayg) = gmtime(time + (86400*3));
	my @mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @week = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my $cookieexpires = sprintf("%s\, %02d-%s-%04d %02d:%02d:%02d GMT", $week[$wdayg], $mdayg, $mons[$mong], $yearg+1900, $hourg, $ming, $secg);
	print "Set-Cookie: sid=$sid_ec; path=/; \n";
}


# �������
if ($admindata->{errmail}) {
	$objAcData->error_mail_work($admindata);
}

print "Location: $SYS->{homeurl_ssl}index.cgi\n\n";
exit;
