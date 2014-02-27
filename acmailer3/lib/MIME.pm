#=========================================================================
#   MIME.pm : MIME Encode and Decode module
#
#   Copyright(c) 2001-2005, Nobuchika Oishi (BSC CONSULTING).
#
#   e-mail : bigstone@my.email.ne.jp
#   support: http://www.din.or.jp/~bigstone/cgilab/index.html
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND
#   ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.
#
#   ver 1.0.9 : updated last on 2005/04/29
#
#=========================================================================
package MIME;

use strict;
use vars qw(
    @ISA @EXPORT $VERSION $DEFAULT_CHARSET %DEFAULT_ENCODING %ENCODING_METHOD
    %CONVERT_CHARSET %CONVERT_OPTION %OPTION_CHARSET %ENABLE_CONVERT $CRLF_ANY
);

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(
    encode_base64
    decode_base64
    encode_quoted
    decode_quoted
    uuencode
);

use Symbol;
use Carp;
use DATE;

require 'jcode.pl';

$VERSION  = '1.0.9';

$DEFAULT_CHARSET = 'ISO-2022-JP';

%DEFAULT_ENCODING = (
    'US-ASCII'    => '7bit',
    'ISO-2022-JP' => '7bit',
    'ISO-8859-1'  => 'quoted-printable',
    'ISO-8859-2'  => 'quoted-printable',
    'ISO-2022-KR' => '7bit',
    'BIG5'        => '8bit',
    'GB-2312'     => '8bit',
    'HZ-GB-2312'  => '7bit',
    'UTF-7'       => '7bit',
    'UTF-8'       => '8bit',
);

%ENCODING_METHOD = (
    'quoted-printable' => sub { encode_quoted($_[0]); },
    'base64'           => sub { encode_base64($_[0], "\n"); },
);

%CONVERT_CHARSET = (
    'ISO-2022-JP' => \&jis,
);

%ENABLE_CONVERT = (
    'ISO-2022-JP' => 1,
    'SHIFT_JIS'   => 1,
    'EUC_JP'      => 1,
    'US-ASCII'    => 1,
);

%CONVERT_OPTION = (
    'jis'  => \&jis,
    'euc'  => \&euc,
    'sjis' => \&sjis,
);

%OPTION_CHARSET = (
    'jis'  => 'ISO-2022-JP',
    'euc'  => 'EUC_JP',
    'sjis' => 'SHIFT_JIS',
);

$CRLF_ANY = "\015?\012";

sub jis  { jcode::jis( $_[0], $_[1], 'z'); }
sub euc  { jcode::euc( $_[0], $_[1], 'z'); }
sub sjis { jcode::sjis($_[0], $_[1], 'z'); }

sub new {
    my $class = shift;
    my $self = {};
    my($k, $v);
    while (($k, $v) = splice(@_, 0, 2)){
        $self->{lc($k)} = $v;
    }
    return bless $self, ref $class || $class;
}

#-----------------------------------------------
#   MIME encoding methods
#-----------------------------------------------
sub encode_message {
    my $self = shift;
    my($parm, $k, $v);
    if(ref($_[0]) eq 'HASH'){
        $parm = shift;
    } else {
        $parm = {};
        while (($k, $v) = splice(@_, 0, 2)){
            $parm->{lc($k)} = $v;
        }
    }
    if($v = $self->{socket}){
        *putstring = *_send_sock;
        delete $parm->{bcc};
    } elsif($v = $self->{sendmail}){
        *putstring = *_send_file;
    } elsif($v = $self->{file}){
        *putstring = *_send_file;
    } else {
        *putstring = *_send_self;
        $self->{encode} = [];
        $v = $self;
    }
    $self->_encode_message($v, $parm) || return undef;
    if(defined $self->{encode}){
        return wantarray ? @{$self->{encode}} : $self->{encode};
    }
    return $self;
}

sub _encode_message {
    my $self = shift;
    my $out  = shift;
    my $parm = shift;
    my $dotskip = $parm->{dotskip} || undef;
    my $charset = $parm->{charset} || $DEFAULT_CHARSET;
    my $convert = $CONVERT_CHARSET{uc($charset)} || undef;
    my(%header, @header, $k, $v);
    foreach $k ('From', 'To', 'Cc', 'Bcc'){
        if($v = $parm->{lc($k)}){
            $v = join(',', @{$v}) if ref $v;
            $v =~ s/[\r\n]//go;
            putstring($out, _encode_address("$k: $v", $charset, $convert)."\n");
        }
    }
    if(defined $parm->{header}){
        while (($k, $v) = splice(@{$parm->{header}}, 0, 2)){
            $v .= "\n" if $v !~ /\n$/so;
            push(@header, join(': ', $k, _encode_envelope($v, $charset, $convert)));
            $header{lc($k)} = 1;
        }
    }
    unless(exists $header{subject}){
        $v = $parm->{subject} || '(none)';
        putstring($out, _encode_envelope("Subject: $v", $charset, $convert)."\n");
    }
    unless(exists $header{date}){
        putstring($out, join('', 'Date: ', DATE::time2local(), "\n"));
    }
    unless(exists $header{'message-id'}){
        $v = _message_id($parm->{sender} || $parm->{from});
        putstring($out, "Message-Id: <$v>\n");
    }
    unless(exists $header{'mime-version'}){
        putstring($out, "MIME-Version: 1.0\n");
    }
    foreach (@header){
        putstring($out, $_);
    }
    my(@boundary, $boundary, $type, $charcd, $encode, $textcnv, $textenc);
    my $content = (defined $parm->{content}) ? scalar @{$parm->{content}} : 0;
    my $attach  = (defined $parm->{attach})  ? keys   %{$parm->{attach}}  : 0;
    if($attach > 0){
        if($content > 0 || $attach > 1){
            $boundary = _boundary(10);
            $type = 'mixed';
        }
    } elsif($content > 1){
        $boundary = _boundary(10);
        $type = $parm->{multipart} || 'alternative';
    }
    if($boundary){
        putstring($out, "Content-Type: multipart/$type;\n boundary=\"$boundary\"\n\n");
        putstring($out, "This is multi-part message in MIME format.\n");
    }
    if($type eq 'mixed' && $content > 1){
        putstring($out, "\n--$boundary\n");
        push(@boundary, $boundary);
        $boundary = _boundary(10);
        $type = $parm->{multipart} || 'alternative';
        putstring($out, "Content-Type: multipart/$type;\n boundary=\"$boundary\"\n");
    }
    if($content){
        foreach $content (@{$parm->{content}}){
            $type = $content->{type} || 'text/plain';
            unless($charcd = $content->{charset}){
                if($type =~ m!^(?:text|message)/!oi){
                    $charcd = $charset || 'us-ascii';
                }
            }
            unless($encode = $content->{encode}){
                $encode = $DEFAULT_ENCODING{uc($charcd)} || '7bit';
            }
            $textcnv = $CONVERT_CHARSET{uc($charcd)} || undef;
            $textenc = $ENCODING_METHOD{lc($encode)} || undef;
            if($v = $content->{option}){
                if($v eq 'THRU'){
                    $textcnv = undef;
                    $textenc = undef;
                } elsif($v eq 'NOCONV'){
                    $textcnv = undef;
                } elsif($v eq 'NOENC'){
                    $textenc = undef;
                }
            }
            if($encode eq '7bit' && _is_ascii($content->{message}) == 0){
                unless($textcnv || $textenc){
                    $encode  = 'base64';
                    $textenc = $ENCODING_METHOD{$encode} || undef;
                }
            }
            $type .= "; charset=$charcd" if $charcd;
            if($v = $content->{name}){
                unless(_is_ascii($v)){
                    $v = &$convert($v) if ref $convert;
                    $v = join('', "=?$charset?B?", encode_base64($v, ""), '?=');
                }
                $type .= qq(;\n name="$v");
            }
            putstring($out, "\n--$boundary\n") if $boundary;
            putstring($out, "Content-Type: $type\n");
            putstring($out, "Content-Transfer-Encoding: $encode\n");
            putstring($out, "\n");
            if(ref $content->{message}){
                foreach (@{$content->{message}}){
                    $_ = &$textcnv($_) if ref $textcnv;
                    $_ = &$textenc($_) if ref $textenc;
                    unless($dotskip){
                        s/^\./../o; s/\n\./\n../go;
                    }
                    $_ .= "\n" unless(/\n$/so);
                    putstring($out, $_);
                }
            } else {
                $_ = $content->{message};
                $_ = &$textcnv($_) if ref $textcnv;
                $_ = &$textenc($_) if ref $textenc;
                unless($dotskip){
                    s/^\./../o; s/\n\./\n../go;
                }
                $_ .= "\n" unless(/\n$/so);
                putstring($out, $_);
            }
        }
        if(@boundary > 0){
            putstring($out, "\n--$boundary--\n");
            $boundary = pop(@boundary);
        }
    }
    if($attach){
        my($fail, $buff, $len, $fh);
        while (($k, $v) = each %{$parm->{attach}}){
            $fh = Symbol::gensym();
            if(open($fh, $v)){
                $type = _guess_type($v);
                unless(_is_ascii($k)){
                    $k = &$convert($k) if ref $convert;
                    $k = join('', "=?$charset?B?", encode_base64($k, ""), '?=');
                }
                putstring($out, "\n--$boundary\n") if $boundary;
                putstring($out, "Content-Type: $type;\n name=\"$k\"\n");
                putstring($out, "Content-Transfer-Encoding: base64\n");
                putstring($out, "Content-Disposition: attachment;\n filename=\"$k\"\n");
                putstring($out, "\n");
                binmode($fh);
                while ($len = read($fh, $buff, 57)){
                    unless(putstring($out, encode_base64(substr($buff, 0, $len), "")."\n")){
                        $fail = 1; last;
                    }
                }
                close $fh;
                if($fail){
                    Carp::croak("Can't output attachment file: $v");
                }
            } else {
                Carp::croak("File does not exist: $v");
            }
        }
    }
    putstring($out, "\n--$boundary--\n") if $boundary;
    1;
}

sub _encode_address {
    my $str = shift;
    my($charset, $convert) = @_;
    my $n = $str =~ s/\n$//so;
    my $res = "";
    foreach (split(/ *[,;] */, $str)){
        next unless $_;
        $res .= join(',', _encode_envelope($_, $charset, $convert), "\n ");
    }
    $res =~ s/ *,\n +$//so;
    $res .= "\n" if $n;
    $res;
}

sub _encode_envelope {
    my $str = shift;
    my($charset, $convert) = @_;
    my $n = $str =~ s/\n$//so;
    my($res, $fold, $s);
    my $len = 0;
    $str =~ s/^ +//so;
    $str =~ s/ +$//so;
    if(uc($charset) eq 'ISO-2022-JP'){  # support japanese character code only.
        $fold = $CONVERT_OPTION{euc};
    }
    foreach (split(/( *["':()<>] *)/, $str)){
        if(_is_ascii($_)){
            if(($len + length($_)) > 72){
                if($res =~ s/ $//so || s/^ //so){
                    $res .= "\n "; $len = 1;
                }
            } elsif($res =~ /=\?[^=?]+\?B\?[^?]+\?=$/so){
                if(/^\S* (.*)$/so){
                    s/ /\n /so; $len = length($1) + 1;
                    $res .= $_; next;
                }
            }
            $res .= $_; $len += length($_);
        } else {
            if($len > 13){  # "Subject: Re: " is 13 chars...!?
                if($res =~ s/ $//so || s/^ //so){
                    $res .= "\n "; $len = 1;
                }
            }
            if($fold){
                $s = &$fold($_);
                while (1){
                    ($_, $s) = _part_string($s, 24);
                    $_ = &$convert($_, 'euc') if ref $convert;
                    $_ = join('', "=?$charset?B?", encode_base64($_, ""), '?=');
                    $res .= $_; $len += length($_);
                    if($s ne ""){
                        $res .= "\n "; $len = 1;
                    } else {
                        last;
                    }
                }
            } else {
                $_ = &$convert($_) if ref $convert;
                $_ = join('', "=?$charset?B?", encode_base64($_, ""), '?=');
                $res .= $_; $len += length($_);
            }
        }
    }
    $res .= "\n" if $n;
    $res;
}

sub _part_string {
    my $str = shift;
    my $len = shift;
    if($len < 1 || length($str) <= $len){
        return ($str, "");
    }
    my $s = substr($str, 0, $len);
    if($s =~ /\x8f$/o || $s =~ tr/\x8e\xa1-\xfe/\x8e\xa1-\xfe/ % 2){
        chop($s); $len--;
    }
    return ($s, substr($str, $len));
}

sub _guess_type {
   #---------------------
    require MTYPE;
   #---------------------
    MTYPE::guess_type(@_);
}

sub _message_id {
    my $addr = _get_addr($_[0]);
    my($host, $domain) = $addr =~ /^([^@]+)\@(.+)$/o;
    return join('', 'JD', DATE::time2date('%Y%M%D%h%m%s'), '.', sprintf("%04d", $$), '.', uc($host), '@', $domain);
}

sub _boundary {
    my $size = shift || 10;
    my $b = encode_base64(join('', map chr(rand(256)), 1..$size*3), "");
    $b =~ s/[\W]/X/go;
    return join('_', '---', uc($b), "");
}

sub _is_ascii {
    if(ref($_[0])){
        foreach (@{$_[0]}){
            return 0 if /[^\t\r\n\x20-\x7e]/o;
        }
        return 1;
    } else {
        $_[0] =~ /[^\t\r\n\x20-\x7e]/o ? 0 : 1;
    }
}

sub _get_addr {
    my $s = shift;
    $s =~ s/\n//go;
    $s =~ s/ *\"[^"]*\" *//go;
    $s =~ s/ *\([^)]*\) *//go;
    if($s =~ /< *([^>]+) *>/o){
        $s = $1;
    }
    $s =~ s/^ +//o;
    $s =~ s/ +$//o;
    $s;
}

sub get_encode {
    my $self = shift;
    return undef unless defined $self->{encode};
    return wantarray ? @{$self->{encode}} : $self->{encode};
}

#-----------------------------------------------
#   MIME decoding methods
#-----------------------------------------------
sub decode_message {
    my $self = shift;
    my(%parm, $k, $v);
    while (($k, $v) = splice(@_, 0, 2)){
        $parm{lc($k)} = $v;
    }
    if($v = $self->{socket}){
        *getstring = *_recv_sock;
    } elsif($v = $self->{file}){
        *getstring = *_recv_file;
    } else {
        *getstring = *_recv_self;
        $self->{decode} = [];
        if(ref $self->{message}){
            push(@{$self->{decode}}, @{$self->{message}});
        } else {
            foreach (split(/$CRLF_ANY/, $self->{message})){
                push(@{$self->{decode}}, "$_\n");
            }
        }
        $v = $self;
    }
    $self->{header}  = [];
    $self->{content} = {};
    $self->{charset} = {};
    $self->{attach}  = {};
    $self->{handle}  = [];
    $self->{fileno}  = 0;
    my($eof, @res) = $self->_decode_header($v, $parm{convert});
    unless($eof){
        $self->_decode_content($v, $parm{convert}, $parm{attach}, $parm{suffix}, $parm{uudecode}, @res);
    }
    $v = 0;
    foreach (keys %{$self->{attach}}){
        push(@{$self->{header}}, join('', 'X-Attach-File', ++$v, ": $_ \(", $self->{attach}->{$_}, "\)\n"));
    }
    1;
}

sub _decode_header {
    my $self = shift;
    my($in, $ocode) = @_;
    my $convert = $ocode ? $CONVERT_OPTION{lc($ocode)} : undef;
    my($eof, $type, $charset, $encode, $boundary, $name, $line, $header, $ec);
    while (1){
        $line = getstring($in);
        $line =~ s/$CRLF_ANY/\n/sgo;
        $line =~ s/^\.\././o;
        $line =~ s/\t/ /go;
        if($line =~ s/^ +/ /o){
            chomp($header); $header .= $line; next;
        }
        if($header ne ""){
            $header =~ s/([^?]+\?=)\s+(=\?[^=?]+\?[BQbq]\?)/$1$2/sgo;
            $ec = ($header =~ s/=\?([^=?]+)\?[Bb]\?([^?]+)\?=/&decode_base64($2)/esgo) ? $1 : undef;
            $ec = ($header =~ s/=\?([^=?]+)\?[Qq]\?([^?]+)\?=/&decode_quoted($2)/esgo) ? $1 : undef;
            if(ref $convert){
                $header = _convert_code($convert, $header, $ec);
            }
            push(@{$self->{header}}, $header);
            if($header =~ /^Content-Type *: *([^\n]+)/oi){
                $type = $1;
                if($type =~ m!^(?:text|message)/([^ ;]+)!oi){
                    $type = lc($1);
                    $self->{content}->{$type} = [];
                    $self->{charset}->{$type} = [];
                    $charset = ($header =~ /charset *= *\"?([^\n\s";]+)/oi) ? $1 : 'us-ascii';
                } elsif($type =~ m!^multipart/.+?boundary *= *\"?([^";]+)!oi){
                    $type = 'multipart'; $boundary = $1;
                } else {
                    $type = 'binary';
                    if($header =~ /name *= *\"?([^\n";]+)/oi || $header =~ m!^Content-Type *: *[^/]+/([^\n\s;]+)!oi){
                        $name = $1;
                    }
                }
            } elsif($header =~ /^Content-Transfer-Encoding *: *([^\n\s;]+)/oi){
                $encode = lc($1);
            } elsif($header =~ /^Content-Disposition *: *attachment/oi){
                $type = 'binary';
                $name = $1 if $header =~ /filename *= *\"?([^\n";]+)/oi;
            }
        }
        last if($line eq "" || $line =~ /^\n$/so);
        if($line =~ /^\.\n$/so){
            $eof = 1; last;
        }
        $header = $line;
    }
    return ($eof, $type, $charset, $encode, $boundary, $name);
}

sub _decode_content {
    my $self = shift;
    my($in, $ocode, $attach, $suffix, $uudecode, $type, $charset, $encode, $boundary, $name) = @_;
    my $convert = $ocode ? $CONVERT_OPTION{lc($ocode)} : undef;
    my($line, $ec, $fh, $file, @boundary);
    if($type eq 'binary' && $attach){
        ($fh, $file, $name) = $self->_open_file($attach, $name, $suffix);
        $self->{attach}->{$name} = $file;
    }
    my $mode = 'C';
    my($header, $content);
    while ($line = getstring($in)){
        last if($line =~ /^\.$CRLF_ANY$/so);
        next if $mode eq 'E';
        $line =~ s/$CRLF_ANY$/\n/so;
        $line =~ s/^\.\././o;
        if($mode eq 'H'){
            $line =~ s/\t/ /go;
            if($line =~ s/^ +/ /o){
                chomp($header); $header .= $line; next;
            }
            if($header ne ""){
                $header =~ s/([^?]+\?=)\s+(=\?[^=?]+\?[BQbq]\?)/$1$2/sgo;
                $ec = ($header =~ s/=\?([^=?]+)\?[Bb]\?([^?]+)\?=/&decode_base64($2)/esgo) ? $1 : undef;
                $ec = ($header =~ s/=\?([^=?]+)\?[Qq]\?([^?]+)\?=/&decode_quoted($2)/esgo) ? $1 : undef;
                if(ref $convert){
                    $header = _convert_code($convert, $header, $ec);
                }
                if($header =~ /^Content-Type *: *([^\n]+)/oi){
                    $type = $1;
                    if($type =~ m!^(?:text|message)/([^ ;]+)!oi){
                        $type = lc($1);
                        unless(exists $self->{content}->{$type}){
                            $self->{content}->{$type} = [];
                            $self->{charset}->{$type} = [];
                        }
                        $charset = ($header =~ /charset *= *\"?([^\n\s";]+)/oi) ? $1 : 'us-ascii';
                    } elsif($type =~ m!^multipart/.+?boundary *= *\"?([^";]+)!oi){
                        $type = 'multipart';
                        push(@boundary, $boundary) if $boundary;
                        $boundary = $1;
                    } else {
                        $type = 'binary';
                        if($header =~ /name *= *\"?([^\n";]+)/oi || $header =~ m!^Content-Type *: *[^/]+/([^\n\s;]+)!oi){
                            $name = $1;
                        }
                    }
                } elsif($header =~ /^Content-Transfer-Encoding *: *([^\n\s]+)/oi){
                    $encode = lc($1);
                } elsif($header =~ /^Content-Disposition *: *attachment/oi){
                    $type = 'binary';
                    $name = $1 if $header =~ /filename *= *\"?([^\n";]+)/oi;
                }
            }
            $header = $line;
            if($line =~ /^\n$/so){
                $mode = 'C';
                if($type eq 'binary' && $attach){
                    ($fh, $file, $name) = $self->_open_file($attach, $name, $suffix);
                    $self->{attach}->{$name} = $file;
                }
            }
        } else {
            if($boundary ne ""){
                if(index($line, "--$boundary--") == 0){
                    $boundary = @boundary > 0 ? pop(@boundary) : undef;
                    if($content ne ""){
                        chomp($content); $type ||= 'plain';
                        if(ref $convert){
                            $content = _convert_code($convert, $content, $charset);
                        }
                        push(@{$self->{content}->{$type}}, $content);
                        push(@{$self->{charset}->{$type}}, $charset);
                    }
                    $header = $content = $type = $encode = $name = "";
                    $mode = $boundary ? 'H' : 'E';
                    next;
                } elsif(index($line, "--$boundary") == 0){
                    if($content ne ""){
                        chomp($content); $type ||= 'plain';
                        if(ref $convert){
                            $content = _convert_code($convert, $content, $charset);
                        }
                        push(@{$self->{content}->{$type}}, $content);
                        push(@{$self->{charset}->{$type}}, $charset);
                    }
                    $header = $content = $type = $encode = $name = "";
                    $mode = 'H';
                    next;
                }
            }
            if($encode eq 'quoted-printable'){
                $line =~ s/=\n//o;
                $line = decode_quoted($line);
            } elsif($encode eq 'base64'){
                $line = decode_base64($line);
            } elsif($encode eq 'x-uuencode'){
                next if $line =~ /^(begin|\`|end|$)/o;
                $line = unpack('u', $line);
            }
            if($type eq 'binary'){
                print $fh $line if $fh;
            } elsif($type eq 'multipart'){
                # ignore multipart notice
            } else {
                $content .= $line;
            }
        }
    }
    $self->_close_file();
    if($content ne ""){
        $type ||= 'plain';
        if(ref $convert){
            $content = _convert_code($convert, $content, $charset);
        }
        push(@{$self->{content}->{$type}}, $content);
        push(@{$self->{charset}->{$type}}, $charset);
    }
    if(defined $self->{content}->{html} && $ocode){
        if($charset = $OPTION_CHARSET{lc($ocode)}){
            foreach (@{$self->{content}->{html}}){
                s/(<META +http-equiv *= *Content-Type[^>]+?charset) *= *[^ ";>]+/$1=$charset/si;
            }
        }
    }
    if($uudecode && $attach){
        foreach $content (@{$self->{content}->{plain}}){
            if($uudecode == 2){
                $content = $self->_decode_uuencode($content, $attach, $suffix);
            } else {
                $self->_decode_uuencode($content, $attach, $suffix);
            }
        }
    }
    1;
}

sub _convert_code {
    my($f, $s, $c) = @_;
    if($c){
        return $s unless exists $ENABLE_CONVERT{uc($c)};
    }
    $s = &$f($s);
}

sub _decode_uuencode {
    my $self = shift;
    my $str  = shift;
    my($dir, $suffix) = @_;
    return $str unless $dir;
    my($line, $fh, $file, $name);
    pos($str) = 0;
    while ($str =~ s/begin +\d+ +(.+?) *\n(.+?)\n\`\nend\n//so){
        $name = $1;
        $line = $2;
        next if(exists $self->{attach}->{$name});
        ($fh, $file, $name) = $self->_open_file($dir, $name, $suffix);
        foreach (split(/\n/, $line)){
            print $fh unpack('u', $_);
        }
        $self->{attach}->{$name} = $file;
    }
    $self->_close_file();
    $str;
}

sub _open_file {
    my $self = shift;
    my($dir, $name, $suffix) = @_;
    $self->{fileno}++;
    $name ||= join('', 'attach', $self->{fileno});
    my($ext) = $name =~ /\.([^.]+)$/o;
    if($ext && ref $suffix){
        $ext = lc($ext);
        $ext = undef unless grep($ext eq $_, @{$suffix});
    } else {
        $ext = undef;
    }
    $ext ||= 'bin';
    my $file = join('.', time, $$, $self->{fileno}, $ext);
    my $fh = Symbol::gensym();
    unless(open($fh, "> $dir/$file")){
        $self->_close_file();
        Carp::croak("File can not open: $dir/$file");
    }
    binmode($fh);
    push(@{$self->{handle}}, $fh);
    return ($fh, $file, $name);
}

sub _close_file {
    my $self = shift;
    while (my $fh = pop(@{$self->{handle}})){
        close $fh;
    }
}

sub header {
    my $self = shift;
    my $name = shift;
    if($name){
        $name =~ s/(\W)/\\$1/go;
        foreach (@{$self->{header}}){
            return $1 if(/^$name *: *(.+)$/i);
        }
        return undef;
    }
    return wantarray ? @{$self->{header}} : $self->{header};
}

sub content {
    my $self = shift;
    my($type, $seq) = @_;
    my $content = $self->{content};
    if(defined $type){
        if(defined $content->{$type}){
            if(defined $seq){
                return $content->{$type}->[$seq];
            }
            return wantarray ? @{$content->{$type}} : $content->{$type};
        }
        return undef;
    }
    return wantarray ? %{$content} : $content;
}

sub charset {
    my $self = shift;
    my($type, $seq) = @_;
    my $charset = $self->{charset};
    if(defined $type){
        if(defined $charset->{$type}){
            if(defined $seq){
                return $charset->{$type}->[$seq];
            }
            return wantarray ? @{$charset->{$type}} : $charset->{$type};
        }
        return undef;
    }
    return wantarray ? %{$charset} : $charset;
}

sub attach {
    my $self = shift;
    my $name = shift;
    return $name ? $self->{attach}->{$name} : %{$self->{attach}};
}

#-----------------------------------------------
#   Alias functions for input/output data
#-----------------------------------------------
sub _send_sock {
    my $sock = shift;
    unless($sock->write(@_)){
        Carp::croak("Can't send message to socket.");
    }
    1;
}

sub _send_file {
    my $fh = shift;
    unless(print $fh @_){
        Carp::croak("Can't write to file or pipe: $!");
    }
    1;
}

sub _send_self {
    my $self = shift;
    push(@{$self->{encode}}, @_);
    1;
}

sub _recv_sock {
    shift->read();
}

sub _recv_file {
    my $fh = shift;
    scalar <$fh>;
}

sub _recv_self {
    my $self = shift;
    shift(@{$self->{decode}});
}

#-----------------------------------------------
#   Base64/QuotedPrintable/uuencode functions
#-----------------------------------------------
#
#   Load Base64 XS module, if MIME::Base64 module Installed.
#
eval {
    require MIME::Base64; MIME::Base64->import(qw(encode_base64 decode_base64));
};
if($@){
    *encode_base64 = \&perl_encode_base64;
    *decode_base64 = \&perl_decode_base64;
}

sub perl_encode_base64 ($;$) {
    my $str = shift;
    my($eol) = @_;
    $eol = "\n" unless defined $eol;
    my $res = "";
    pos($str) = 0;
    while ($str =~ /(.{1,45})/gso){
        $res .= substr(pack('u', $1), 1);
        chop($res);
    }
    $res =~ tr|` -_|AA-Za-z0-9+/|;
    if(my $pad = (3 - length($str) % 3) % 3){
        $res =~ s/.{$pad}$/'=' x $pad/e;
    }
    if(length($eol)){
        $res =~ s/(.{1,76})/$1$eol/g;
    }
    $res;
}

sub perl_decode_base64 ($) {
    my $str = shift;
    local($^W) = 0;
    $str =~ tr|A-Za-z0-9+=/||cd;
    if(length($str) % 4){
        return $_[0];
    }
    $str =~ s/=+$//o;
    $str =~ tr|A-Za-z0-9+/| -_|;
    my $res = "";
    my $len;
    while ($str =~ /(.{1,60})/gso){
        $len = chr(32 + int(length($1) * 3 / 4));
        $res .= unpack("u", $len . $1);
    }
    $res;
}

sub encode_quoted ($) {
    my $str = shift;
    $str =~ s/([^ \t\n!-<>-~])/sprintf("=%02X", ord($1))/ego;
    $str =~ s/([ \t]+)$/join('', map { sprintf("=%02X", ord($_)) } split('', $1))/egmo;
    my $break = "";
    while ($str =~ s/(.*?^[^\n]{73}(?:[^=\n]{2}(?![^=\n]{0,1}$)|[^=\n](?![^=\n]{0,2}$)|(?![^=\n]{0,3}$)))//xsmo){
        $break .= "$1=\n";
    }
    return join('', $break, $str);
}

sub decode_quoted ($) {
    my $str = shift;
    $str =~ s/[ \t]+?(\r?\n)/$1/go;
    $str =~ s/=\r?\n//go;
    $str =~ s/=([\da-fA-F]{2})/pack("C", hex($1))/ego;
    $str;
}

sub uuencode ($$) {
    my($dir, $file) = @_;
    my $fh = Symbol::gensym();
    open($fh, "< $dir/$file") or return undef;
    my $str = "begin 666 $file\n";
    my($len, $buff);
    while ($len = read($fh, $buff, 45)){
        $str .= pack("u", substr($buff, 0, $len));
    }
    close $fh;
    $str .= "\x60\nend\n";
    $str;
}

1;

__END__
