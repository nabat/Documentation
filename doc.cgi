#!/usr/bin/perl
=head1 Documentation
 Abills Documentation
=cut

use strict;
use warnings;

BEGIN {
  our $libpath = '../';
  my $sql_type = 'mysql';
  
  unshift(@INC,
    $libpath . "Abills/$sql_type/",
    $libpath . "Abills/modules/",
    $libpath . '/lib/',
    $libpath . '/Abills/',
    $libpath
  );
}

our (
  $libpath,
  %conf,
  %FORM,
  %functions,
  %permissions
);


do "$libpath/libexec/config.pl";

use Abills::HTML;
use Abills::Defs;

require Abills::Misc;

my $html = Abills::HTML->new(
  {
    NO_PRINT => 1,
    CONF     => \%conf,
    CHARSET  => $conf{default_charset},
  }
);

use Abills::SQL;

my $db = Abills::SQL->connect(
  $conf{dbtype},
  $conf{dbhost},
  $conf{dbname},
  $conf{dbuser},
  $conf{dbpasswd}, {
    CHARSET => ($conf{dbcharset}) ? $conf{dbcharset} : undef
});

print $html->header();

if ($FORM{url}) {
  use Documentation::db::Documentation;
  
  my $Doc = Documentation->new($db, undef, \%conf);
  
  my $url = $Doc->list({
    WIKI       => $FORM{url},
    CONFLUENCE => '_SHOW',
    VERIF      => 1,
    COLS_NAME  => 1
  });

  $url = $url->[0]->{confluence} if($url);

  if (!$url) {
    my $no_url = $SELF_URL;
    if ($no_url =~ /doc.cgi/) {
      $no_url =~ s/doc.cgi/admin\/index.cgi/g
    }

    my $index = get_function_index('doc_list');
    $html->redirect($no_url . '?header=1&get_index=doc_list&add_form=1&ex_param=' . $FORM{url});
  }
  else {
    $html->redirect($url);
    return 1;
  }
}


1;