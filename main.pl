use strict;
use warnings;
use diagnostics;
use Mojolicious::Lite;

get '/' => {
    text => 'I ♥ Mojolicious!' . $ENV{"DB_HOST"}
};

app->start;
