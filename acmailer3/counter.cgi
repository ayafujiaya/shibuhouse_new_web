#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
require "./lib/gifcat.pl";
use strict;

our $SYS;

# ŠÇ—ŽÒ‚Ìƒf[ƒ^Žæ“¾
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

if (!$admindata->{counter_disp}) {
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat'gifcat(("./img/no.gif"));
	exit;
}

my %FORM = &form("noexchange");
my $data_ref;
my @DATA = $objAcData->GetData("mail", "MAIL");

my $num = sprintf("%05d", ($#DATA + 1));
my @gif;
for (1..5) {
	my $ref = substr($num, ($_ - 1), 1);
	my $data = "./img/$ref.gif";
	push(@gif, $data);
}

print "Content-type: image/gif\n\n";
binmode(STDOUT);
print &gifcat'gifcat(@gif);
exit;
