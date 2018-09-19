use strict;
use warnings;
use diagnostics;
use utf8;
use feature "5.22";
use Mojolicious::Lite;

get '/' => {
    text => 'I ♥ Mojolicious!' . $ENV{"DB_HOST"}
};

app->start;
