package MailSession;
use strict;
BEGIN {
    require './lib/common.pm';
};


sub new {
    my $class = shift;
    my %args = @_ == 1 ? %{$_[0]} : @_;

    # init
    %args = (
	session_dir => './session_mail',
	session     => {},
	%args
    );

    my $self = bless \%args, $class;

    if ( $self->{mail_id} ) {
	$self->load();
    }
    else {
	$self->{mail_id} = time.$$;
    }

    return $self;
}

sub mail_id {
    return shift->{mail_id};
}

sub session {
    return shift->{session};
}

sub set {
    my ($self, $col, $val) = @_;
    $self->{session}->{$col} = $val;
    return $self;
}

sub get {
    my ($self, $col) = @_;
    return $self->{session}->{$col};
}

sub save {
    my ($self) = @_;

    # sessionデータを整形
    my $data ='';
    for my $k ( keys %{$self->{session}} ) {
	my $v = $self->{session}->{$k};
	$data .= "$k=$v;";
    }

    # ファイルに書き込み
    my $filepath = $self->_build_session_file_path();
    open my $fh, '>', $filepath or syserror("データファイルのオープンに失敗しました。");
    flock($fh, 2);
    print {$fh} $data;
    close($fh);
    chmod(0666, $filepath);

}

sub load {
    my ($self) = @_;

    # セッションファイルへのパス
    my $filepath = $self->_build_session_file_path();
    return {} unless -f $filepath;

    # セッションファイルからデータを読み込み
    open my $fh, '<', $filepath or syserror("データファイルのオープンに失敗しました。");
    flock($fh, 1);
    my @lines = <$fh>;
    close($fh);
    my $data = join('', @lines);
    &jcode::convert(\$data, "euc");

    # データを整形
    my @datas = split(/;/, $data);
    my %session;
    for my $d (@datas) {
	my ($k, $v) = split(/=/, $d);
	if ( $k ) {
	    $session{$k} = $v;
	}
    }
    $self->{session} = \%session;

    return $self->session;
}

sub clear {
    my $self = shift;
    my $filepath = $self->_build_session_file_path();
    unlink($filepath);
}

sub _build_session_file_path {
    my $self = shift;
    return $self->{session_dir} . '/' . $self->{mail_id} . '.' . $self->ext;
}

sub delete_old_session_file {
    my $self = shift;

    my $ext = $self->ext;
    my $dir = $self->{session_dir};
    opendir my $dh, $self->{session_dir} or die "";
    my @files = grep(/\.$ext$/, readdir($dh));
    closedir $dh;

    my $sec = 3 * 24 * 60 * 60;
    for my $file (@files) {
        my $filepath = "$dir/$file";
        if ( (time - $sec) > ((stat($filepath))[9]) ) {
            unlink $filepath;
        }
    }
}

sub ext {
    my $self = shift;
    return 'cgi';
}

1;
