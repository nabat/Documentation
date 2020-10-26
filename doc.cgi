#!/usr/bin/perl
=head1 Documentation

 Abills Documentation

=cut

use strict;
use warnings;

BEGIN {
  our $libpath  = '../';
  our $sql_type = 'mysql';
  unshift(@INC, $libpath . "Abills/$sql_type/", $libpath . 'lib/', $libpath . 'Abills/modules/', $libpath . 'Abills/',);

  eval { require Time::HiRes; };
  our $begin_time = 0;
  if (!$@) {
    Time::HiRes->import(qw(gettimeofday));
    $begin_time = Time::HiRes::gettimeofday();
  }
}


use Abills::Defs;
our (%OUTPUT, %lang, %LANG, $base_dir, $CONTENT_LANGUAGE);
do "../libexec/config.pl";

use Abills::Base qw(sendmail in_array load_pmodule);
use Abills::Fetcher;
use Users;
use Admins;
use Documentation::db::Documentation;

our $html = Abills::HTML->new({ CONF => \%conf, NO_PRINT => 1, });
our $db   = Abills::SQL->connect($conf{dbtype}, $conf{dbhost}, $conf{dbname}, $conf{dbuser}, $conf{dbpasswd}, { CHARSET => ($conf{dbcharset}) ? $conf{dbcharset} : undef });

if ($conf{LANGS}) {
  $conf{LANGS} =~ s/\n//g;
  my (@lang_arr) = split(/;/, $conf{LANGS});
  %LANG = ();
  foreach my $l (@lang_arr) {
    my ($lang, $lang_name) = split(/:/, $l);
    $lang =~ s/^\s+//;
    $LANG{$lang} = $lang_name;
  }
}

my %INFO_HASH   = ();

our $admin = Admins->new($db, \%conf);
$admin->info($conf{SYSTEM_ADMIN_ID}, { IP => '127.0.0.1' });

our $users = Users->new($db, $admin, \%conf);

if($html->{language} ne 'english') {
  do $libpath . "/language/english.pl";
}

if(-f $libpath . "/language/$html->{language}.pl") {
  do $libpath."/language/$html->{language}.pl";
}

require Abills::Templates;
require Abills::Misc;

$INFO_HASH{SEL_LANGUAGE} = $html->form_select(
  'language',
  {
    EX_PARAMS => 'onChange="selectLanguage()"',
    SELECTED  => $html->{language},
    SEL_HASH  => \%LANG,
    NO_ID     => 1
  }
);

my $Doc = Documentation->new($db, undef, \%conf);

if ($FORM{ex_param}) {
  $html->tpl_show(_include('documentation_add', 'Documentation'), {
      WIKI   => $FORM{ex_param} || '',
      SUBMIT =>  "<input type=\"submit\" name=\"add\" value=\"Добавить\" class=\"btn btn-primary\" id=\"add\">",
      TITLE  => $lang{ADD}
  });
}

if ($FORM{add}) {
  $Doc->add({
    WIKI       => $FORM{WIKI},
    CONFLUENCE => $FORM{CONFLUENCE}
  });
  if (!$Doc->{errno}) {
    $html->message('info', $lang{SUCCESS});
  }
  else {
    $html->message('err', $lang{ERROR}, $Doc->{errno} . " : " . $Doc->{errstr});
  }
}

if (!($FORM{header} && $FORM{header} == 2)) {
  print $html->header();

  my $doc_url = 'http://abills.net.ua:8090';

  my $button_wiki_doc = "<ul class='sidebar-menu tree' data-widget='tree'>";
  $button_wiki_doc .= "<li><a href='$doc_url'><span>ABillS Documentation</span></a></li>";
  $button_wiki_doc .= "</ul>";
  
  $OUTPUT{HTML_STYLE} = 'lte_adm';
  $OUTPUT{CONTENT_LANGUAGE} = lc $CONTENT_LANGUAGE;
  $OUTPUT{INDEX_NAME} = 'doc.cgi';
  $OUTPUT{TITLE}      = "$conf{WEB_TITLE} - WIKI";
  $OUTPUT{SELECT_LANGUAGE}   = $INFO_HASH{SEL_LANGUAGE};
  $OUTPUT{REG_LOGIN} = "style='display:none;'";
  $OUTPUT{REG_STATE} = "style='display:none;'";
  $OUTPUT{REG_IP} = "style='display:none;'";
  $OUTPUT{DATE} = $DATE;
  $OUTPUT{TIME} = $TIME;
  $OUTPUT{IP} = $ENV{'REMOTE_ADDR'};
  $OUTPUT{BODY} = $html->{OUTPUT};
  $OUTPUT{SKIN} = 'skin-yellow';
  $OUTPUT{MENU} = $button_wiki_doc,
  $OUTPUT{BODY} = $html->tpl_show(templates('form_client_main'), \%OUTPUT);

  print $html->tpl_show(templates('registration'), { %OUTPUT, TITLE_TEXT => $lang{REGISTRATION} });
  print $html->tpl_show(templates('form_client_start'), { %OUTPUT });
}
else {
  print "Content-Type: text/html\n\n";
  print $html->{OUTPUT};
}

if ($FORM{url}) {
  my $url = $Doc->list({
    WIKI       => $FORM{url},
    CONFLUENCE => '_SHOW',
    VERIF      => 1,
    COLS_NAME  => 1
  });

  $url = $url->[0]->{confluence} if($url);

  if (!$url) {
    my $no_url = "https://support.abills.net.ua/doc.cgi";
    $html->redirect($no_url . '?add_form=1&ex_param=' . $FORM{url});
  }
  else {
    $html->redirect($url);
  }
}

1;
